'''
To connect to postgresql database as defined in oli.config
Read subjects and write subjects
Created on 14 apr. 2017

@author: GerbenRienk
'''
import psycopg2
from utils.dictfile import readDictFile

class ConnToOliDB(object):
    '''Class for connecting to the postgresql database as defined in oli.config
    Methods implemented now are read subjects and add subjects '''
    def __init__(self):
        'let us create the connection to use multiple times'
        config=readDictFile('oli.config')
        conn_string = "host='" + config['dbHost'] + "' dbname='" + config['dbName'] + "' user='" + config['dbUser'] + "' password='" + config['dbPass'] + "'"
        self.init_result = ''
        
        # get a connection, if a connect cannot be made an exception will be raised here
        try:
            self._conn = psycopg2.connect(conn_string)
        except:
            print('unable to class connect with %s' %  (conn_string))
        
        self.init_result = 'class connected '

    def ReadSubjectsFromDB(self):
        'method to read table subjects into a list'
        cursor = self._conn.cursor()  
        try:
            cursor.execute("""SELECT * from subjects""")
        except:
            print ("not able to execute the select")
        results = cursor.fetchall()
        return results

    def AddSubjectsToDB(self, dict_of_subjects):
        """ Method to add a dictionary of subjects to the table subjects
        It is made to handle multiple inserts
        """
        cursor = self._conn.cursor()  
        print("in AddSubjects: ", dict_of_subjects)
        try:
            cursor.executemany("""INSERT INTO subjects(study_subject_oid,study_subject_id) VALUES (%s, %s)""", dict_of_subjects)
        except:
            print ("not able to execute the insert")
        self._conn.commit()
        return None
    
    def WriteLSDataToDB(self, ssoid, ls_data, ws_import_response):
        """ Method to write already imported data the table subjects
        For subject with this StudySubjectOID, including the response of the web-service
        """
        cursor = self._conn.cursor()  
        
        try:
            cursor.execute("UPDATE subjects set ls_data='%s', ws_import_response='%s' where study_subject_oid='%s'" % (ls_data, ws_import_response, ssoid))
        except:
            print ("not able to execute the update")
        self._conn.commit()
        return None

    def DLookup(self, field_name, table_name, where_clause):
        '''Method to read one field of a table with certain criteria
        If no result, then a list containing an empty string is returned
        '''
        cursor = self._conn.cursor()  
        sql_statement = "SELECT " + field_name + " from " + table_name + " where " + where_clause
        try:
            cursor.execute(sql_statement)
        except:
            print ("not able to execute the select")
        results = cursor.fetchone()
        if not results:
            results = ['']
        return results[0]
        

class PGSubject(object):
    '''to get the study subject oid from the study subject id
    by calling the rest-webservice
    Only parameter is study subject id
    Connection info is read from oli.config
    '''
    def __init__(self, PGStudySubjectID):
        self._studysubjectid = PGStudySubjectID
        return
    
    def GetSSOID(self):
        'method to get the StudySubjectOID using rest'
        import requests
        import xml.etree.ElementTree as ET
        config=readDictFile('oli.config')
        
        login_url = config['baseUrlRest'] + '/j_spring_security_check'
        login_action = {'action':'submit'}
        login_payload = {
            'j_username': config['userName'],
            'j_password': config['password'],
            'submit':"Login"
                        }
        mySession = requests.Session()
        mySession.post(login_url,params=login_action,data=login_payload)
        cd_url = config['baseUrlRest'] + '/rest/clinicaldata/xml/view/' + config['studyOid'] + '/'
        cd_url = cd_url + self._studysubjectid + '/*/*'
        print(cd_url)
        clinical_data = mySession.get(cd_url)
        
        document = clinical_data.content
        root = ET.fromstring(document)
                    
        for clinical_data in root.findall('{http://www.cdisc.org/ns/odm/v1.3}ClinicalData/'):
            subject_info = clinical_data.attrib
            if subject_info['{http://www.openclinica.org/ns/odm_ext_v130/v3.1}StudySubjectID'] == self._studysubjectid:
                return subject_info['SubjectKey']



if __name__ == "__main__":
    pass    