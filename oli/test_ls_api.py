'''
Created on 9 apr. 2017

@author: GerbenRienk
'''
import time
import datetime
import json
import base64
from utils.logmailer import MailThisLogFile
from utils.dictfile import readDictFile
from utils.limesurveyrc2api import LimeSurveyRemoteControl2API
from utils.pg_api import ConnToOliDB
from utils.reporter import Reporter

def cycle_through_syncs():
    my_report = Reporter()
    start_time = datetime.datetime.now()
    my_report.append_to_report('cycle started at ' + str(start_time))
    # read configuration file for usernames and passwords and other parameters
    config=readDictFile('oli.config')
    
    # create a connection to the postgresql database
    conn = ConnToOliDB()
    my_report.append_to_report(conn.init_result)
    
    #start the cycling here
    while True:
        # get the resposnes as a list
        responses_list = read_ls_responses(config)
        # process the responses one by one
        for one_response in responses_list:
            for response_data in one_response:
                print(type(one_response[response_data]), one_response[response_data])    
        
        
        # some book keeping to check if we must continue looping, or break the loop
        # first sleep a bit, so we do not eat up all CPU
        time.sleep(int(config['sleep_this_long']))
        current_time = datetime.datetime.now()
        difference = current_time - start_time
        loop_this_long = config['loop_this_long']
        max_diff_list = loop_this_long.split(sep=':') 
        max_difference = datetime.timedelta(hours=int(max_diff_list[0]), minutes=int(max_diff_list[1]), seconds=int(max_diff_list[2]))
        if difference > max_difference:
            break
    
    my_report.append_to_report('finished looping from %s till %s.' % (start_time, current_time))
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
