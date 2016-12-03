Tuition-Bot-NTU
===================
Telegram Bot that helps matching student and teacher for coursework dobuts, while keeping all their information secure.  
[Bot Link](https://telegram.me/TutoRoBot)

### Procedures: 
Admin password(case sensitive) set to: q 

 1. Count=0:
Checks whether the folder TuitionBot_Users exist in directory where the python file is stored.If folder is not there then the said folder is made.If the folder already exist,then the information are loaded in form of nested list with each element as list of legth 2(file no,course content).The info is then stored in the appropriate list (student_list or teacher_list) .Just file number and course content chosen are stored in runtime to prevent leak of information like name and phone number.

 2. Count=1:
	Prints to the user to input their name
	
 3. Count=2:
	Name is stored in variable name.Prints to the user to input if they are admin,student or teacher.

 4. Count=3:
    The input entered is checked whether it was for-
    a) student :  by checking whether the input was one of "1" or "1." or "student" or "1.student" or any other combination of uppercase or lowercase letters .If they are student then they are asked in which they are in.
    b) teacher : by checking whether the input was one of "2" or "2." or "teacher" or "2.teacher" or any other combination of uppercase or lowercase letters .If they are teacher then they are asked which year students they would like to teach.
    c) admin : by checking whether the input was one of "3" or "3." or "admin" or "3.admin" or any other combination of uppercase or lowercase letters.If they are identified as admin,the user are then asked to enter password which we have set to 'q'(The admin identified is directly directed to count=11)

 5. Count=4:
	The year number entered is stored in variable year.The user is then prompted to enter their phone number.

 6. Count=5:
	The phone number enterd entered is stored in private variable called phone. The user is then promptedd to enter the course they have problem by appropriatly prompting them to choose from course regarding the year they chose.

 7. Count=6:
	The course they chose is stored in the form of integer in the variable course_study .According to the year and course the user chose,the user is prompted to choose the particular content they have problem in or they want to teach.

 8. Count=7:
	The course content chosen is stored in the variable first as integer then as string in content_study. Then content chosen is displayed to the user and the user is asked to confirm whether it was correct or not.

 9. Count=8:
	If the user indicate that content chosen is correct,then the program makes the folder TuitionBot_Users if already not made,then the program uses that folder and creates a file storing information entered by user-name,year,teacher/student,phone no,content and course chosen.The new file made has extension .tuitionBotNTU and prefix is user number seen by the program by checking in folder how much files already exist,so the file made cant be accessed by any other program ,only by the file made by us and that too by the admin only.So the details entered especially the phone number is secure.
    Then if the user is student/teacher the info like studen nested list with each element as list of length2(file no,content)
	The user is then told that if any match is found ,the user will be informed.

 10. Count=9:
	The program then finds for match from the list that was made earlier and if course content chosen by the user matches (if student,check teacher_list and if user teacher,check student_list).If match found,then the program gives details to the user so that they can contact their respective student/teacher(only name and phone number disclosed).
	If match found,the file of student and teacher are deleted from the computer so that no one can access it anymore.
	

 11. Count=10(for students only):
	 According to tear chosen,course chosen,content chosen ;the student user is provided with a video file (if available)for that topic for reference. 
	
 12. Count=11(Admin functions)
	Checks whether the password input is same as password stored in program(stored as private variable).If it is correct then admin is asked to input which file to read by displaying all the files that are present on the computer.

 13. Count=12(admin functions)
	 Opens the file chosen by the admin and displays their details.
	