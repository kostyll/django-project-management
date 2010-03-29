-- Database script to upgrade pre-ExtJS application to current version

ALTER TABLE "wbs_projectphase" ADD COLUMN "description" text NOT NULL;
ALTER TABLE "wbs_projectphase" ADD COLUMN "stage_number" integer NOT NULL;
ALTER TABLE "deliverables_deliverable" CHANGE COLUMN "method" "testing_method" text NOT NULL;
ALTER TABLE "projects_project" ADD COLUMN "quality_plan" text NOT NULL;
ALTER TABLE "projects_project" ADD COLUMN "communications_plan" text NOT NULL;




