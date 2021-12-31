------------- SQLite3 Dump File -------------

-- ------------------------------------------
-- Dump of "EmergencyContactsOfStu"
-- ------------------------------------------

CREATE TABLE "EmergencyContactsOfStu"(
	"phone" Numeric NOT NULL,
	"studentEmail" Text NOT NULL,
	"firstName" Text NOT NULL,
	"middleName" Text,
	"lastName" Text NOT NULL,
	CONSTRAINT "EmergencyContactsOfStu_Student_CASCADE_NO ACTION_studentEmail_email_0" FOREIGN KEY ( "studentEmail" ) REFERENCES "Student"( "email" )
		ON DELETE Cascade
,
PRIMARY KEY ( "phone", "studentEmail" ) );


-- ------------------------------------------
-- Dump of "EmergencyContactsOfTA"
-- ------------------------------------------

CREATE TABLE "EmergencyContactsOfTA"(
	"TAEmail" Text NOT NULL,
	"phoneNum" Numeric NOT NULL,
	"firstName" Text NOT NULL,
	"middleName" Text,
	"lastName" Text NOT NULL,
	CONSTRAINT "EmergencyContactsOfTA_TA_CASCADE_NO ACTION_TAEmail_email_0" FOREIGN KEY ( "TAEmail" ) REFERENCES "TA"( "email" )
		ON DELETE Cascade
,
PRIMARY KEY ( "phoneNum", "TAEmail" ) );


-- ------------------------------------------
-- Dump of "Guardian"
-- ------------------------------------------

CREATE TABLE "Guardian"(
	"guardianEmail" Text NOT NULL,
	"studentEmail" Text NOT NULL,
	"firstName" Text NOT NULL,
	"lastName" Text NOT NULL,
	"guardianPhoneNumber" Text,
	CONSTRAINT "Guardian_Student_CASCADE_NO ACTION_studentEmail_email_0" FOREIGN KEY ( "studentEmail" ) REFERENCES "Student"( "email" )
		ON DELETE Cascade
,
PRIMARY KEY ( "guardianEmail", "studentEmail" ) );


-- ------------------------------------------
-- Dump of "Manager"
-- ------------------------------------------

CREATE TABLE "Manager"(
	"email" Text NOT NULL PRIMARY KEY,
	"DOB" Integer NOT NULL,
	"firstName" Text NOT NULL,
	"middleName" Text,
	"lastName" Text NOT NULL,
	"phone" Integer NOT NULL );


BEGIN;

INSERT INTO "Manager" ("email","DOB","firstName","middleName","lastName","phone") VALUES 
( 'NAnobody@gmail.com', 0, 'N', 'N', 'N', 0 ),
( 'dilrajb98@hotmail.com', 19980417, 'Dilraj', '', 'Bhandal', 7786785421 );



COMMIT;

-- ------------------------------------------
-- Dump of "PaidTA"
-- ------------------------------------------

CREATE TABLE "PaidTA"(
	"TAEmail" Text NOT NULL,
	"GPAInPostSec" Numeric NOT NULL,
	CONSTRAINT "PaidTA_TA_CASCADE_NO ACTION_TAEmail_email_0" FOREIGN KEY ( "TAEmail" ) REFERENCES "TA"( "email" )
		ON DELETE Cascade
 );


-- ------------------------------------------
-- Dump of "Price"
-- ------------------------------------------

CREATE TABLE "Price"(
	"price" Numeric NOT NULL,
	"grade" Integer NOT NULL,
	"type" Text NOT NULL,
PRIMARY KEY ( "grade", "type" ) );


BEGIN;

INSERT INTO "Price" ("price","grade","type") VALUES 
( 24, 8, 'Group' ),
( 26, 9, 'Group' ),
( 28, 10, 'Group' ),
( 30, 11, 'Group' ),
( 32, 12, 'Group' ),
( 27, 8, 'One to one' ),
( 28, 9, 'One to one' ),
( 29, 10, 'One to one' ),
( 30, 11, 'One to one' ),
( 31, 12, 'One to one' ),
( 22, 1, 'Group' ),
( 22, 2, 'Group' ),
( 22, 3, 'Group' ),
( 22, 4, 'Group' ),
( 22, 5, 'Group' ),
( 22, 6, 'Group' ),
( 26, 1, 'One to one' ),
( 26, 2, 'One to one' ),
( 26, 3, 'One to one' ),
( 26, 4, 'One to one' ),
( 26, 5, 'One to one' ),
( 26, 6, 'One to one' ),
( 26, 7, 'One to one' ),
( 39, 8, 'N/A' ),
( 22, 7, 'Group' );



COMMIT;

-- ------------------------------------------
-- Dump of "Student"
-- ------------------------------------------

CREATE TABLE "Student"(
	"email" Text NOT NULL PRIMARY KEY,
	"firstName" Text NOT NULL,
	"middleName" Text,
	"lastName" Text NOT NULL,
	"grade" Text,
	"cellPhone" Text NOT NULL,
	"address" Text,
	"DOB" Integer,
	"UnpaidFee" Numeric NOT NULL );


-- ------------------------------------------
-- Dump of "TA"
-- ------------------------------------------

CREATE TABLE "TA"(
	"email" Text NOT NULL PRIMARY KEY,
	"managerEmail" Text,
	"firstName" Text NOT NULL,
	"middleName" Text,
	"lastName" Text NOT NULL,
	"DOB" Integer NOT NULL,
	"homePhoneNum" Integer,
	"cellPhoneNum" Integer NOT NULL,
	"highSchAvg" Integer,
	"collegeName" Text,
	"graduateDate" Integer,
	CONSTRAINT "TA_Manager_NO ACTION_NO ACTION_managerEmail_email_0" FOREIGN KEY ( "managerEmail" ) REFERENCES "Manager"( "email" )
 );


-- ------------------------------------------
-- Dump of "Tutorial"
-- ------------------------------------------

CREATE TABLE "Tutorial"(
	"date" Integer,
	"startTime" Integer,
	"TAEmail" Text NOT NULL,
	"type" Text NOT NULL,
	"addressOrLink" Text,
	"grade" Integer NOT NULL,
	"status" Text NOT NULL,
	CONSTRAINT "Tutorial_TA_CASCADE_NO ACTION_TAEmail_email_0" FOREIGN KEY ( "TAEmail" ) REFERENCES "TA"( "email" )
		ON DELETE Cascade
,
PRIMARY KEY ( "date", "startTime", "TAEmail" ) );


-- ------------------------------------------
-- Dump of "VolunteerTA"
-- ------------------------------------------

CREATE TABLE "VolunteerTA"(
	"TAEmail" Text NOT NULL,
	CONSTRAINT "VolunteerTA_TA_CASCADE_NO ACTION_TAEmail_email_0" FOREIGN KEY ( "TAEmail" ) REFERENCES "TA"( "email" )
		ON DELETE Cascade
 );


-- ------------------------------------------
-- Dump of "studentAttendTutorial"
-- ------------------------------------------

CREATE TABLE "studentAttendTutorial"(
	"date" Integer NOT NULL,
	"startTime" Integer NOT NULL,
	"TAEmail" Text NOT NULL,
	"studentEmail" Text NOT NULL,
	"price" Numeric,
	CONSTRAINT "studentAttendTutorial_Student_CASCADE_NO ACTION_studentEmail_email_0" FOREIGN KEY ( "studentEmail" ) REFERENCES "Student"( "email" )
		ON DELETE Cascade,
	CONSTRAINT "studentAttendTutorial_Tutorial_CASCADE_NO ACTION_TAEmail_date_startTime_TAEmail_date_startTime_0" FOREIGN KEY ( "TAEmail", "date", "startTime" ) REFERENCES "Tutorial"( "TAEmail", "date", "startTime" )
		ON DELETE Cascade
,
PRIMARY KEY ( "date", "startTime", "TAEmail", "studentEmail" ) );


