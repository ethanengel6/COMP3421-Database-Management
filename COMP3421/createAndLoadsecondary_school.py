
import mysql.connector


mydb = mysql.connector.connect(
  user='ethan1',    # could be root, or a user you created, I created 'testuser'
  passwd='',  # the password for that use
  database='secondary_school',   # the database to connect to
  host='127.0.0.1',   # localhost
  allow_local_infile='1'  # needed so can load local files
)

print(mydb)
myc = mydb.cursor()   # myc name short for "my cursor"

myc.execute('set global local_infile = 1;')

myc.execute ("use secondary_school")

myc.execute("drop table if exists temp_enrolled_in;")
myc.execute("drop table if exists enrolled_in;")
myc.execute("drop table if exists courses;")
myc.execute("drop table if exists students;")

myc.execute("""
create table students(
  sid int,
  grade int,
  name varchar(25),
  contact_info varchar(50),
  address varchar(50),
  Primary Key (sid) ) ;
""")

myc.execute("""
create table courses (
  course_id int,
  name varchar(25),
  credits float,
  PRIMARY KEY (course_id) ) ;
""")

myc.execute("""
create table enrolled_in (
  sid int,
  course_id int,
  term varchar(20),
  FOREIGN KEY(sid) references students(sid),
  FOREIGN KEY(course_id) references courses(course_id))
  ;
""")


myc.execute("""
  load data local infile '/Users/elain/Desktop/COMP3421/data_students.txt' into table students
  fields terminated by ','
  lines terminated by '\n' ;
""")


myc.execute("""
load data local infile '/Users/elain/Desktop/COMP3421/data_courses.txt' into table courses
  fields terminated by ','
  lines terminated by '\n' ;
""")

myc.execute("""
load data local infile '/Users/elain/Desktop/COMP3421/data_enrolled_in.txt' into table enrolled_in
  fields terminated by ','
  lines terminated by '\n' ;
""")

myc.execute('select count(*) from enrolled_in;')
before = myc.fetchone()
print("\n Before deletions total enrolled_in count= ")
print(before)

myc.execute('set @freshmax=120')
myc.execute("""
Select E.sid, E.course_id from students S, enrolled_in E
where S.sid=E.sid and S.grade=9 and E.course_id>@freshmax
""")
overmax = myc.fetchall()
print ("\n These are the student id's of freshmen that have registered for a course over the allowable course id maximum.  The corresponding course id is also listed.  \n")
print (overmax)
print("\n Total enrollment violations = ", len(overmax))


myc.execute("""
create table temp_enrolled_in as
(Select E.sid, E.course_id, E.term from students S, enrolled_in E
where S.sid=E.sid and S.grade=9 and E.course_id>@freshmax)
""")

print("\n Now deleting:")
myc.execute("""
DELETE FROM enrolled_in
WHERE EXISTS (
SELECT *
FROM temp_enrolled_in
where temp_enrolled_in.sid=enrolled_in.sid
and temp_enrolled_in.course_id=enrolled_in.course_id
and temp_enrolled_in.term= enrolled_in.term)
""")

myc.execute("""
Select E.sid, E.course_id from students S, enrolled_in E
where S.sid=E.sid and S.grade=9 and E.course_id>@freshmax
""")
newovermax = myc.fetchall()
print (newovermax)

myc.execute('select count(*) from enrolled_in;')
after = myc.fetchone()
print("\n After deletions total enrolled_in count= ")
print (after)

mydb.commit()
mydb.close()
