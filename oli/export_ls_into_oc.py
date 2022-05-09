'''
Created November and December 2018

@author: GerbenRienk
'''
import time
import datetime
import json
import base64
from utils.logmailer import MailThisLogFile
from utils.dictfile import readDictFile
from utils.fam_por import compose_odm
from utils.limesurveyrc2api import LimeSurveyRemoteControl2API
from utils.ocwebservices import dataWS
from utils.pg_api import ConnToOliDB, PGSubject
from utils.reporter import Reporter

def cycle_through_syncs():
    my_report = Reporter()
    
    start_time = datetime.datetime.now()
    my_report.append_to_report('INFO: cycle started at ' + str(start_time))
    # read configuration file for usernames and passwords and other parameters
    config=readDictFile('oli.config')
    # set from this config the sid, because it used everywhere
    sid = int(config['sid'])
    
    # create a connection to the postgresql database
    conn = ConnToOliDB()
    my_report.append_to_report(conn.init_result)

    # initialize the oc-webservice
    myDataWS = dataWS(config['userName'], config['password'], config['baseUrl'])
    
    #start the cycling here
    while True:
        # get the responses as a list
        responses_list = read_ls_responses(config)
        # process the responses one by one
        for one_response in responses_list:
            #print(one_response)           
            # get the response_id, for administrative purposes
            response_id = one_response['id']
            # check if this combination sid-response-id already exists and if not, add it
            conn.TryToAddSubjectToDB(sid, response_id)
            # now see if we can do something with the data: start with the child code
            # reset study_subject_id and study_subject_oid
            study_subject_id = None 
            study_subject_oid = None
            if (one_response['ChildCode'] is None):
                # write this to error report
                my_report.append_to_report('ERROR: Missing ChildCode for resp.id. %i' % response_id )
            else:
                # add leading zero's and the study prefix
                study_subject_id = config['childcode_prefix'] + ('0000' + str(int(float(one_response['ChildCode']))))[-8:]
                if (len(study_subject_id) != 13):
                    # write this to error report 
                    my_report.append_to_report('ERROR: Incorrect ChildCode for resp.id. %i: %i' % (response_id, int(float(one_response['ChildCode']))))
                else:
                    # write the child-code / study subject id to the database
                    if (conn.DLookup('study_subject_id', 'ls_responses', 'sid=%i and response_id=%i' % (sid, response_id)) is None):
                        conn.WriteStudySubjectID(sid, response_id, study_subject_id)
                        
                    # check if we already have a valid study subject oid
                    study_subject_oid = conn.DLookup('study_subject_oid', 'ls_responses', 'sid=%i and response_id=%i' % (sid, response_id))
                    if (study_subject_oid is None or study_subject_oid =='None'):
                        # try to get a valid study subject oid
                        study_subject_oid = PGSubject(study_subject_id).GetSSOID()
                        # we don't know if we now have study_subject_oid,
                        # but the procedure only writes the study subject oid to the database for later use
                        # if it is not null
                        conn.WriteStudySubjectOID(sid, response_id, study_subject_oid)
                    
                    
                    # only continue if we have both study subject id and study subject oid
                    if (study_subject_oid is None):
                        # write this to error report
                        my_report.append_to_report('ERROR: missing OID for resp.id. %i : ChildCode %s' % (response_id, study_subject_id))
                    else:
                        # only compose the odm and try to import the result
                        # if this wasn't done before, so look at date_completed
                        if(conn.DLookup('date_completed', 'ls_responses', 'sid=%i and response_id=%i' % (sid, response_id)) is None):
                            #print(one_response)
                            print('resp.id. %i' % response_id)
                            # we try to compose the request, but if we can't convert an item to the correct data type
                            # then we put that in the report
                            ws_request = compose_odm(study_subject_oid, one_response)
                            if (ws_request.find('CONVERSION-ERROR') != -1):
                                #print(ws_request)
                                item_starts_at = ws_request.find('CONVERSION-ERROR')
                                my_report.append_to_report('ERROR: conversion for resp.id. %i %s failed with message "%s" and more' % (response_id, study_subject_id, ws_request[item_starts_at:item_starts_at + 100]))
                            else:
                                #print(ws_request)
                                conn.WriteDataWSRequest(sid, response_id, ws_request)
                                import_result = myDataWS.importData(ws_request)
                                #print(import_result)
                                import_result = import_result.replace("'", "")
                                conn.WriteDataWSResponse(sid, response_id, import_result)
                                if (import_result.find('Success') == 0):
                                    my_report.append_to_report('INFO: Successfully imported data for %s (%s)' % (study_subject_id, study_subject_oid))
                                    conn.SetResponseComplete(sid, response_id)
                                else:
                                    item_starts_at = import_result.find('I_')
                                    my_report.append_to_report('ERROR: import for resp.id %i %s failed with message "%s" and more' % (response_id, study_subject_id, import_result[item_starts_at:]))
                                    
            # move on with the next response 
                                
        # check if we must continue looping, or break the loop
        # first sleep a bit, so we do not eat up all CPU
        time.sleep(int(config['sleep_this_long']))
        current_time = datetime.datetime.now()
        difference = current_time - start_time
        loop_this_long = config['loop_this_long']
        max_diff_list = loop_this_long.split(sep=':') 
        max_difference = datetime.timedelta(hours=int(max_diff_list[0]), minutes=int(max_diff_list[1]), seconds=int(max_diff_list[2]))
        if difference > max_difference:
            break
    
    my_report.append_to_report('INFO: finished looping from %s till %s.' % (start_time, current_time))
    # close the file so we can send it
    my_report.close_file()
    MailThisLogFile('logs/report.txt')
    
def read_ls_responses(config):
    """
    function to use the ls api and read all responses into a dictionary
    parameters
    config is the dictionary with all configuration elements
    """
    # collecting LimeSurvey data
    # Make a session, which is a bit of overhead, but the script will be running for hours.
    # get the survey id of the one survey we're interested in and cast it into an integer
    sid = int(config['sid'])
    api = LimeSurveyRemoteControl2API(config['lsUrl'])
    session_req = api.sessions.get_session_key(config['lsUser'], config['lsPassword'])
    session_key = session_req.get('result')
    # now get all responses of our survey
    api_response2 = api.responses.export_responses(session_key, sid)
    responses_b64 = base64.b64decode(api_response2['result'])
    responses_dict = json.loads(responses_b64)   #this is a dictionary
    return responses_dict['responses']
    
if __name__ == '__main__':
    cycle_through_syncs()
