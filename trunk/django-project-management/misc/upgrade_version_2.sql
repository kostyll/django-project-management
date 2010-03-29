-- Database script to upgrade pre-ExtJS application to current version

ALTER TABLE wbs_projectphase ADD COLUMN description text NOT NULL;
ALTER TABLE wbs_projectphase ADD COLUMN stage_number integer NOT NULL;
ALTER TABLE deliverables_deliverable CHANGE COLUMN method testing_method text NOT NULL;
ALTER TABLE projects_project ADD COLUMN quality_plan text NOT NULL;
ALTER TABLE wbs_workitem ADD COLUMN project_stage_id integer NOT NULL;
ALTER TABLE projects_project ADD COLUMN communications_plan text NOT NULL;
INSERT INTO wbs_project_stage ( stage, description, id ) VALUES ( "Default", "", 1 );
UPDATE wbs_workitem SET project_stage_id = 1;
ALTER TABLE wbs_workitem DROP COLUMN project_phase_id;





