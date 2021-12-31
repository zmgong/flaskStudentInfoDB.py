# TEMPLATE FOR RUNNING SQL COMMANDS
import sqlite3

conn = sqlite3.connect('blog.db')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect('blog.db')
# Display all blogs from the 'blogs' table
conn.row_factory = dict_factory
c = conn.cursor()

create_student_table = """
CREATE TABLE InPersonTutorial
(
	time_Stamp	 varchar(50) NOT NULL,
	studentEmail varchar(50) NOT NULL,
	TAEmail		 varchar(50) NOT NULL,
	tStatus		 varchar(20) NOT NULL,
	tType 		 varchar(50) NOT NULL,
	grade		 int(2)		 NOT NULL,
	tSubject	 varchar(50) NOT NULL,
	PRIMARY KEY(time_Stamp),
	FOREIGN KEY(TAEmail) REFERENCES TA(TAEmail),
	FOREIGN KEY(studentEmail) REFERENCES Student(email)
);
"""

create_student_entry = """Insert into Student values ('fake123@hotmail.com','Fake', 'Singh', 'Dhami', 5, '6043232323','Surrey', 'Fake St.', 123, 656, 09171992, 'false')
"""

dropBlogs = """'DROP TABLE blogs'"""
dropUsers = """'DROP TABLE users'"""
# c.execute(create_student_entry)
create_student_table = "CREATE TABLE Student(	email		CHAR(255)	NOT NULL,	firstName	CHAR(255)	NOT NULL,	middleName	CHAR(255),	lastName	CHAR(255)	NOT NULL,	grade		CHAR(255),		cellPhone	CHAR(255)	NOT NULL,	address CHAR(255), DOB INT(8)	,UnpaidFee	DECIMAL(255)	NOT NULL,	PRIMARY KEY (email));"
drop_student = 'DROP TABLE Student'

order = "DELETE FROM Student WHERE email = 'asd12@hotmail.com'"

create_emergency_contact_of_student = "CREATE TABLE EmergencyContactsOfStu(phone	DECIMAL NOT NULL,	studentEmail " \
                                      "CHAR(39)	NOT NULL,firstName	CHAR(20)	NOT NULL,middleName	CHAR(20),	" \
                                      "lastName	CHAR(20)	NOT NULL,PRIMARY KEY(phone, studentEmail),FOREIGN KEY(" \
                                      "studentEmail ) REFERENCES Student(email)ON DELETE CASCADE); "

create_guardian_table = "CREATE TABLE Guardian(	guardianEmail	CHAR(255)	NOT NULL,   studentEmail CHAR(255) NOT " \
                        "NULL,	firstName	CHAR(" \
                        "255)	NOT NULL, lastName			CHAR(255)	NOT NULL,guardianPhoneNumber		CHAR(255), " \
                        "PRIMARY KEY(guardianEmail, studentEmail), FOREIGN KEY(studentEmail) REFERENCES Student(" \
                        "email) ON DELETE CASCADE); "

create_TA_table = 'CREATE TABLE TA ( email		CHAR(255)	NOT NULL, managerEmail	CHAR(255), firstName	CHAR(' \
                  '255)	NOT NULL, middleName	CHAR(255), lastName	CHAR(255)	NOT NULL, DOB		INTEGER(8)	NOT ' \
                  'NULL, homePhoneNum	INTEGER(255), cellPhoneNum	INTEGER(255)	NOT NULL, highSchAvg		' \
                  'INTEGER(3), collegeName		TEXT, graduateDate		INTEGER(8), PRIMARY KEY(email), FOREIGN KEY(' \
                  'managerEmail) REFERENCES Manager(email) ); '

create_emergency_contact_of_TA = 'CREATE TABLE EmergencyContactsOfTA ( TAEmail		CHAR(255)	NOT NULL, phoneNum	' \
                                 'DECIMAL NOT NULL, firstName	CHAR(255)	NOT NULL, middleName	CHAR(255), ' \
                                 'lastName	CHAR(255)	NOT NULL, PRIMARY KEY(phoneNum, TAEmail), FOREIGN KEY(TAEmail) ' \
                                 'REFERENCES TA(email) ON DELETE CASCADE ) '

create_Manager_table = 'CREATE TABLE Manager ( email		CHAR(255)	NOT NULL, DOB		INTEGER(8)	NOT NULL, ' \
                       'firstName	CHAR(255)	NOT NULL, middleName	CHAR(255), lastName	CHAR(255)	NOT NULL, ' \
                       'phone		INTEGER(255)	NOT NULL, PRIMARY KEY(email) ); '

create_Non_manager = "insert into Manager VALUES('nobody@non.com', 00000000, 'N', 'N', 'N', 0000000000)"

# check tables SELECT name FROM sys.Tables;

create_paid_TA = 'CREATE TABLE PaidTA ( TAEmail		CHAR(255)	NOT NULL, GPAInPostSec	DECIMAL	NOT NULL, FOREIGN KEY(' \
                 'TAEmail) REFERENCES TA(email) ON DELETE CASCADE) '

create_volunteerTA = 'CREATE TABLE VolunteerTA ( TAEmail		CHAR(255)	NOT NULL, FOREIGN KEY(TAEmail) REFERENCES ' \
                     'TA(email) ON DELETE CASCADE ) '

create_tutorial = 'CREATE TABLE Tutorial ( date		INTEGER, startTime	INTEGER, TAEmail	CHAR(255)	NOT NULL, ' \
                  'type		TEXT	NOT NULL, addressOrLink		TEXT, grade		INTEGER(2)	NOT NULL, ' \
                  'status		TEXT		NOT NULL, PRIMARY KEY(date, startTime, TAEmail), FOREIGN KEY(TAEmail) ' \
                  'REFERENCES TA(email) ON DELETE CASCADE ); '

create_student_attend_tutorial_table = 'CREATE TABLE studentAttendTutorial ( date		INTEGER	NOT NULL, startTime	' \
                                       'INTEGER	NOT NULL, TAEmail	CHAR(255)	NOT NULL, studentEmail	CHAR(255)	' \
                                       'NOT NULL, price DECIMAL, PRIMARY KEY(date, startTime, TAEmail, studentEmail), ' \
                                       'FOREIGN KEY(studentEmail) REFERENCES Student(email) ON DELETE CASCADE, ' \
                                       'FOREIGN KEY(TAEmail, date, startTime) REFERENCES Tutorial(TAEmail, date, ' \
                                       'startTime) ON DELETE CASCADE ); '

create_student_in_tutorial_name_and_email_view = 'CREATE VIEW studentNameAndEmailInTutorial as SELECT studentEmail, ' \
                                                 'TAEmail, date, startTime,' \
                                                 'firstName, middleName, lastName FROM studentAttendTutorial, Student'

create_price_table = 'CREATE TABLE Price ( price	DECIMAL NOT NULL, grade  INTEGER NOT NULL, type 	CHAR(255) NOT ' \
                     'NULL, PRIMARY KEY(grade , type) ) '


# The assertion of project
create_assertion = 'CREATE ASSERTION gradeCheck ' \
                   'CHECK(' \
                   'NOT EXISTS (	SELECT * FROM Student WHERE grade < ' \
                   '1 OR grade > 12))'


order = "DROP TABLE Tutorial;"

query = "SELECT COUNT(*) AS NumberOFStudent FROM Student"
c.execute(create_tutorial)
conn.commit()
result = c.fetchall()

print(result)
