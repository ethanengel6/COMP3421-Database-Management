import numpy as np

np.random.seed(1)



# create the students data
numStudents = 100
outfile = open("data_students.txt","w")
for i in range(1,numStudents+1):
	outString = ''
	outString += str(i)   # id
	outString += ','
	grade = str(np.random.randint(4)+9)
	outString += grade
	outString += ','
	outString += 'student'
	outString += str(i)   # name
	outString += ','
	email = 'student'+str(i)+'@medford.student.edu'
	outString += email
	outString += ','
	house_num = ( np.random.randint(999) + 1 )
	outString += str(house_num)+" Stuyvestant Avenue"  #address
	outString += "\n"
	outfile.write(outString)
outfile.close()

# create the course data
numCourses = 100
outfile = open("data_courses.txt","w")
for i in range(101,numCourses+101):
	outString = ''
	outString += str(i)   # course_Id
	outString += ','
	outString += 'course'
	outString += str(i)   #course_name
	outString += ','
	credits= str( np.random.randint(2) + 3)
	outString += credits
	outString += "\n"
	outfile.write(outString)
outfile.close()



# create the enrolled data
numEnrolled = 1000
outfile = open("data_enrolled_in.txt","w")
for i in range(1,numEnrolled+1):
	outString = ''
	sid = str( np.random.randint(numStudents) + 1)
	outString += str(sid)   # sid
	outString += ','
	cid = str( np.random.randint(numCourses) + 101)
	outString += cid   # cid
	outString += ','
	termSeason=np.random.randint(2)
	if termSeason == 0:
		term = "Fall"+str(np.random.randint(4)+2020)
	else:
		term = "Spring"+str(np.random.randint(4)+2020)

	outString += term
	outString += "\n"
	outfile.write(outString)
outfile.close()
