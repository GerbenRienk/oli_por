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

from utils.reporter import Reporter
#from _operator import itemgetter

def cycle_through_syncs():
    my_report = Reporter()
    start_time = datetime.datetime.now()
    my_report.append_to_report('cycle started at ' + str(start_time))
    # read configuration file for usernames and passwords and other parameters
    config=readDictFile('oli.config')
    sid = int(config['sid'])
    print(sid)
    while True:
        # collecting LimeSurvey data
        # Make a session, which is a bit of overhead, but the script will be running for hours.
        api = LimeSurveyRemoteControl2API(config['lsUrl'])
        session_req = api.sessions.get_session_key(config['lsUser'], config['lsPassword'])
        session_key = session_req.get('result')
        api_response = api.surveys.list_surveys(session_key, config['lsUser'])
        print("surveys: ")
        all_surveys = api_response['result']
        
        for one_survey in all_surveys:
            if (one_survey['sid'] == sid):
                print(one_survey['surveyls_title'])
        # now get all responses of our survey
        api_response2 = api.responses.export_responses(session_key, sid)
        responses_b64 = base64.b64decode(api_response2['result'])
        responses_dict = json.loads(responses_b64)   #this is a dictionary
        responses_list = responses_dict['responses']
        
        for one_response in responses_list:
            for response_data in one_response:
                print(type(one_response[response_data]), one_response[response_data])
            
        
        
               
            #print(one_survey['sid'])           
        # examples of using the api
        # api.tokens.add_participants(session_key, event_survey_pairs[studysubject_event[1]], participant_data)
        #participants_req = api.tokens.list_participants(session_key, sid)
        #participants = participants_req.get('result')
        
        
        
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
    
    
if __name__ == '__main__':
    cycle_through_syncs()
