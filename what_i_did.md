- in eclipse: file - import - Project from Git (with smart import) - clone URI

- to install packages zeep and lxml:  go to Window -> Preferences and in the pop-up window, navigate to PyDev -> Interpreters -> Python Interpreter
- click Manage with pip
- enter install zeep
- lxml is installed as part of zeep
- create a db-user for administrative purposes:
CREATE USER oli WITH LOGIN UNENCRYPTED PASSWORD 'xxx'
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
- create database
CREATE DATABASE oli_por OWNER oli;

CREATE TABLE ls_responses
(
  sid integer NOT NULL, -- survey id, as is used in LimeSurvey
  response_id integer NOT NULL,
  study_subject_id character varying(32),
  study_subject_oid character varying(32),
  data_ws_request character varying(10000),
  data_ws_response character varying(4000),
  date_completed date,
  CONSTRAINT pk_ls_responses PRIMARY KEY (sid, response_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ls_responses
  OWNER TO oli;
COMMENT ON COLUMN ls_responses.sid IS 'survey id, as is used in LimeSurvey';

We should do something with 
select study_subject_id, count(*) from ls_responses
group by study_subject_id
having count(*) > 1
order by study_subject_id;
