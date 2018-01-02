/*

Synergetic Lite

script.js

All web functionality required for all webpages.

*/


function redirectOnLogin(userType, username) {
    // Function to redirect the user to their page after logging in.
    // Written on 13DEC17/14DEC

    if (userType == 'student') {

        console.log('Logging in as student.')
        localStorage.setItem('currentStudent', username)
        window.location.href = 'studentHomepage.py?studentID=' + username

    } else if (userType == 'teacher') {

        console.log('Logging in as teacher.')
        localStorage.setItem('currentTeacher', username)
        localStorage.setItem('isAdmin', JSON.stringify(false))
        window.location.href = 'teacherHomepage.py?teacherID=' + username

    } else if (userType == 'parent') {

        console.log('Logging in as parent.')
        localStorage.setItem('currentParent', username)
        // window.location.href = blah

    } else if (userType == 'admin') {

        console.log('Logging in as admin.')
        localStorage.setItem('currentTeacher', username)
        localStorage.setItem('isAdmin', JSON.stringify(true))
        window.location.href = 'adminHomepage.html'
        console.log('a!')

    } else if (userType == 'failedLogin') {
        alert('Invalid username or password.')
        window.location.href = 'index.html'
    }
}

function setCurrentCourse(ID) {
    // Sets the currentCourse in localStorage to the given ID
    // Used for redirecting to editCourse.html
    // Written 15DEC17

    localStorage.setItem('currentCourse', ID)
}

function setCurrentClass(ID) {
    // Sets the currentClass in localStorage to the given ID
    // Used for redirecting to addEnrolment.html
    // Written 19DEC17

    localStorage.setItem('currentClass', ID)
}

function setupEditCoursePage() {
    // Sets up the edit course page form with values

    currentCourse = localStorage.getItem('currentCourse')
    document.changeCourseIDForm.oldCourseID.value = currentCourse
    document.changeCourseIDForm.newCourseID.value = currentCourse
}

function setupAddEnrolmentPage() {
    // Sets up the add Enrolment page form with values
    // Written 21DEC17

    currentClass = localStorage.getItem('currentClass')
    document.addEnrolmentForm.classID.value = currentClass
}

function setupChangeTeacherPasswordPage() {
    // Sets up the change Teacher password page with the Teacher_ID

    currentTeacher = localStorage.getItem('currentTeacher')
    document.changePasswordForm.teacherID.value = currentTeacher
}

function coursesRedirect(succeeded) {
    // Redirects the user to coursesManage.py after modifying/adding Courses
    // Alerts the user if the ID is already in use
    // Written 15DEC17

    if (succeeded == 0) {
        alert('That ID is used by an existing course.')
    } else if (succeeded == 1) {
        alert('The ID cannot be blank.')
    }
    window.location.href = 'coursesManage.py'
}

function teachersRedirect(succeeded) {
    // Redirects the user to teachersManage.py after adding Teachers
    // Alerts the user if the ID is already in use
    // Written 17DEC17

    if (succeeded == 0) {
        alert('That ID is used by an existing teacher.')
    } else if (succeeded == 1) {
        alert('The ID cannot be blank.')
    }
    window.location.href = 'teachersManage.py'
}

function classesRedirect(succeeded) {
    // Redirects the user to classesManage.py after adding Classes
    // Alerts the user if the ID is already in use
    // Written 17DEC17

    if (succeeded == 0) {
        alert('That ID is used by an existing class.')
    } else if (succeeded == 1) {
        alert('The ID cannot be blank.')
    }
    window.location.href = 'classesManage.py'
}

function enrolmentsRedirect(succeeded, classID) {
    // Redirects the user to manageClass.py after adding Classes
    // Alerts the user if the ID is already in use
    // Written 17DEC17

    if (succeeded == 0) {
        alert('That student is already in the class.')
    } else if (succeeded == 1) {
        alert('The ID cannot be blank.')
    }
    window.location.href = 'manageClass.py?classID=' + classID
}

function studentsRedirect(succeeded) {
    // Redirects the user to studentsManage.py after adding Classes
    // Alerts the user if the ID is already in use
    // Written 17DEC17

    if (succeeded == 0) {
        alert('That ID is used by an existing student.')
    } else if (succeeded == 1) {
        alert('The ID cannot be blank.')
    }
    window.location.href = 'studentsManage.py'
}

function timetableRedirect(succeeded, classID) {
    // Redirects the user to manageClassTimetable.py after reserving periods.
    // Alerts the user if the period is otherwise occupied
    // Written 22DEC17

    if (succeeded == 0) {
        alert('The Period is already reserverd by another class for the teacher or students.')
    }
    window.location.href = 'manageClassTimetable.py?classID=' + classID
}

function passwordRedirect(succeeded) {
    // Redirects the user to teacherHomepage.py after attempt at changing passwords
    // Alerts the user if the old password was wrong or new&verify did not match
    // Written 02JAN18

    if (succeeded == 0) {
        alert('Old password invalid.')
    } else if (succeeded == 1) {
        alert('New password did not match with verification.')
    }
    redirectToTeacherHomepage()
}

function redirectToTeacherHomepage() {
    // Redirects a user from any place to their teacher Homepage
    // Written 02JAN18
    currentTeacher = localStorage.getItem('currentTeacher')
    window.location.href = 'teacherHomepage.py?teacherID=' + currentTeacher
}
