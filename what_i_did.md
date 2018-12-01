- created empty repository on github with only readme.md
- in eclipse: file - import - Project from Git (with smart import) - clone URI
- mind that the correct folder is selected: C:\Users\Gerben Rienk\Documents\GitHub
- right click on project, select PyDev - Set as PyDev Project
- create source-folder oli
- copy package config from oli3.1
- put oli.config in .gitignore by right-clicking on it and choosing Team - Ignore; commit and push and it works (!)
- put an example oli_example.config next to it, so others understand how it works

- create a db-user for administrative purposes:
CREATE USER oli WITH LOGIN
  UNENCRYPTED PASSWORD 'xxx'
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
- create database
CREATE DATABASE oli_por OWNER oli;

CREATE TABLE ls_responses
(
  study_subject_id character varying(32) NOT NULL,
  study_subject_oid character varying(32) NOT NULL,
  sid integer, -- survey id, as is used in LimeSurvey...
  response_id integer,
  CONSTRAINT pk_study_subject_oc PRIMARY KEY (study_subject_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ls_responses
  OWNER TO oli;
COMMENT ON COLUMN ls_responses.sid IS 'survey id, as is used in LimeSurvey for oli_por this will always be the same: 620620 still it feels like a good idea';
