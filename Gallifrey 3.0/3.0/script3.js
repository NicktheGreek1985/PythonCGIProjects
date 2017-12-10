/* GALLIFREY 3.0 CODE
Developed By Nick Patrikeos
*/


//====OBJECT DEFINITIONS====//

Student = function(name, id, password) {
    this.id = id
    this.password = password
    this.enrolments = []
    this.name = name
}

Teacher = function(username, password, name) {
    this.username = username
    this.password = password
    this.name = name
    this.classes = []
}

Enrolment = function(classref) {
    this.classref = classref
    this.submissions = []
}

Submission = function(filename, topic, taskgroup, task) {
    this.file = filename
    this.state = 'unmarked'
    this.comment = ''
    this.topic = topic
    this.taskgroup = taskgroup
    this.task = task
    this.isObsolete = false
}

Course = function(name, year) {
    this.name = name
    this.year = year
    this.description = ''
    this.files = []
    this.links = []
    this.topics = []
    this.classes = []
}

Class = function(name, year, course) {
    this.name = name
    this.year = year
    this.course = course
    this.teachers = []
    this.students = []
}

CourseTopic = function(covername, topicname) {
    this.covername = covername
    this.topicname = topicname
}

Topic = function(name) {
    this.name = name
    this.filetypes = []
    this.taskgroups = []
    this.totalNumberOfActivities = 0
    this.courses = []
}

Taskgroup = function(name) {
    this.name = name
    this.filetypes = []
    this.tasks = []
}

Task = function(name, difficulty, description, hint, solution) {
    this.name = name
    this.difficulty = difficulty
    this.description = description
    this.hint = hint
    this.attachments = []
    this.filetypes = []
    this.taskimage = ''
    this.solutionimage = ''
    this.solution = solution
}

Attachment = function(covername, filename) {
    this.covername = covername
    this.filename = filename
}

//====DATA STORAGE AND VARIABLE PREPARATION====//

var students, teachers, courses, classes, topics, tempClasses
var cT, cS, cCL, cC, cTP, cTG, cTK
var firstClickOutsideDiv = true
var dragSrcEl, tableRows

function setStoreToData(courses, teachers, students, classes, topics) {
    localStorage.setItem('teachers', teachers)
    localStorage.setItem('students', students)
    localStorage.setItem('classes', classes)
    localStorage.setItem('courses', courses)
    localStorage.setItem('topics', topics)
    window.location.href = 'teacherDashboard.html'
}

function extractLSData() {
    students = JSON.parse(localStorage.getItem('students'))
    teachers = JSON.parse(localStorage.getItem('teachers'))
    courses = JSON.parse(localStorage.getItem('courses'))
    classes = JSON.parse(localStorage.getItem('classes'))
    topics = JSON.parse(localStorage.getItem('topics'))
    
    courses.sort(function compareCourseYears(a, b) {
                    if (a.year < b.year) {
                        return -1
                    }
                    if (b.year < a.year) {
                        return 1
                    }
                    return 0
                })
    
    
    
    classes.sort( function compareNames(a, b) {
                    if (a.name < b.name) {
                        return -1
                    }
                    if (b.name < a.name) {
                        return 1
                    }
                    return 0
                })
    topics.sort( function compareNames(a, b) {
                    if (a.name < b.name) {
                        return -1
                    }
                    if (b.name < a.name) {
                        return 1
                    }
                    return 0
                })

    cT = getTeacherByUsername(localStorage.getItem('currentTeacher'))
    cS = JSON.parse(localStorage.getItem('currentStudent'))
    cC = localStorage.getItem('currentCourse')
    cCL = localStorage.getItem('currentClass')
    cTP = localStorage.getItem('currentTopic')
    cTG = localStorage.getItem('currentTaskGroup')
    cTK = localStorage.getItem('currentTask')

    try {
        setupFooter()
    } catch (err) {}
}

function setupFooter() {
    document.getElementsByClassName('footer')[0].innerHTML = 'Gallifrey 3.1.0<br>Developed By \
    <a href="mailto:nick.p@iinet.net.au">Nick Patrikeos</a>.'
}

function redirectToLocation(location) {
    window.location.href = location
}

function checkChangesAreSaved() {}

//====WEBSITE SETUP >>>

function redirectToLocation(location) {
    window.location.href = location
}

//====LOGIN====//

function setupLoginPage() {
    // Checks if login has failed (set into local storage by the verification python program)
    // If so, alert the user
    var loginFailed = JSON.parse(localStorage.getItem('failedLogin'))

    if (loginFailed != null && loginFailed) {
        document.getElementById('failedAlert').style.display = 'block'
    } else {
        document.getElementById('failedAlert').style.display = 'none'
    }

    // Sets current identifiers to null
    localStorage.setItem('currentTeacher', null)
    localStorage.setItem('currentStudent', null)
    localStorage.setItem('currentCourse', null)
    localStorage.setItem('currentClass', null)
    localStorage.setItem('currentTopic', null)

    setupFooter()
}

function setupStudentLogin(studentID) {
    // Sends the window to the student dashboard and sets the current student
    localStorage.setItem('currentStudent', studentID)
    localStorage.setItem('failedLogin', false)
    window.location.href = 'studentDashboard.html'
}

function setupTeacherLogin(teacherID) {
    // Sends the window to the teacher dashboard and sets the current teacher
    localStorage.setItem('currentTeacher', teacherID)
    localStorage.setItem('failedLogin', false)
    window.location.href = 'refreshData.py'
}

function handleFailedLogin() {
    // Sets failedLogin to true in local storage and sends window back to login page
    localStorage.setItem('failedLogin', true)
    window.location.href = 'login3.html'
}

//====TEACHER DASHBOARD & NAVBAR====//

function setupTeacherDashboard() {
    // Sets up the Teacher Dashboard

    extractLSData()
    setupTeacherNavbar('teacherDashboard.html')

    var classesTable = document.getElementById('myClasses')
    var teacherClasses = teachers[cT].classes

    localStorage.setItem('currentStudent', null)

    var altGrey = true

    for (var cl = 0; cl < classes.length; cl++) {
        if (classes[cl].teachers.indexOf(teachers[cT].name) != -1) {
            if (altGrey) {
                classesTable.innerHTML += '<tr class="altGrey"><td>' + classes[cl].name + '</td>\
                <td><a href="manageClass.html" onclick="localStorage.setItem(\'currentClass\',\''+ classes[cl].name +'\')">Manage</a></td>'
                altGrey = false
            } else {
                classesTable.innerHTML += '<tr><td>' + classes[cl].name + '</td>\
                <td><a href="manageClass.html" onclick="localStorage.setItem(\'currentClass\',\''+ classes[cl].name +'\')">Manage</a></td>'
                altGrey = true
            }
        }
    }
}

function setupTeacherNavbar(location) {
    // Sets up the navigation bar for a teacher

    var dashboardHTML = '<h4><a href="teacherDashboard.html">Dashboard</a></h4>'
    var courseHTML = '<h4><a href="courseList.html">Courses</a></h4>'
    var classHTML = '<h4><a href="classList.html">Classes</a></h4>'
    var topicHTML = '<h4><a href="topicList.html">Topics</a></h4>'
    var logoutLink = '<div name="logout"><a href="login3.html">Logout</a></div>'

    var saveForm = '<form action="saveData.py" id="logout_form" method="POST">\
               <input type="text" value=\'' + JSON.stringify(courses) + '\' name="courses" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(teachers) + '\' name="teachers" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(students) + '\' name="students" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(classes) + '\' name="classes" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(topics) + '\' name="topics" style="display: none"/>\
               <input type="text" value=\'' + location + '\' name="location" style="display: none" />\
               <input type="submit" value="Save Changes">\
               </form>'

    var navbar = dashboardHTML + courseHTML + topicHTML + classHTML + logoutLink + saveForm
    document.getElementById('navbar').innerHTML += navbar
}

//====STUDENT DASHBOARD & NAVBAR ====//

function setupStudentDashboard(location) {
    extractLSData()
    setupStudentNavbar('studentDashboard.html')
    var s = getCurrentStudent()

    var enrolments = students[s].enrolments
    var enrolmentsDiv = document.getElementById('enrolments')
    console.log(enrolmentsDiv)
    for (var e = 0; e < enrolments.length; e++) {
        var cl = getClassByName(enrolments[e].classref)

        var completion = getCompletionForCourse(getCourseByName(classes[getClassByName(enrolments[e].classref)].course)) // '<div class="unmarkedDash"></div>'
        var unmarked = completion[0]
        var correct = completion[1]
        var incorrect = completion[2]
        var fillBar = completion[3]

        var enrolmentBox = '<div class="enrolmentBox"><h3>' + enrolments[e].classref + '</h3> \
        with ' + classes[cl].teachers.join(', ') + '<br><div class="progressDash">\
        <div class="unmarkedDash" style="width: ' + unmarked + '%;"></div>\
        <div class="correctDash" style="width: ' + correct + '%;"></div>\
        <div class="incorrectDash" style="width: ' + incorrect + '%;"></div>\
        <div class="fillBar"></div></div>\
        <div class="studentButton"><a href="viewCourseStudent.html" onclick="localStorage.setItem(\'currentCourse\', \'' + classes[cl].course + '\')">View Class</a></div></div>'
        enrolmentsDiv.innerHTML += enrolmentBox
    }


}

function setupStudentNavbar(location) {
    var s = getCurrentStudent()
    var dashboardHTML = '<h4><a href="studentDashboard.html">Dashboard</a></h4>'
    var enrolments = students[s].enrolments
    var enrolmentList = []
    for (var e = 0; e < enrolments.length; e++) {
        var course = classes[getClassByName(enrolments[e].classref)].course
        var link = '<a href="viewCourseStudent.html" onclick="localStorage.setItem(\'currentCourse\', \'' + course + '\')">' + enrolments[e].classref + '</a>'
        enrolmentList.push('<h4>' + link + '</h4>')
    }
    var enrolmentHTML = enrolmentList.join('')
    var logoutLink = '<div name="logout"><a href="login3.html">Logout</a></div>'

    var saveForm = '<form action="saveData.py" id="logout_form" method="POST">\
               <input type="text" value=\'' + JSON.stringify(courses) + '\' name="courses" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(teachers) + '\' name="teachers" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(students) + '\' name="students" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(classes) + '\' name="classes" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(topics) + '\' name="topics" style="display: none"/>\
               <input type="text" value=\'' + location + '\' name="location" style="display: none" />\
               <input type="submit" value="Save Changes">\
               </form>'

    // var classHTML = '<h4><a href="classListStudent.html">All Classes</a></h4>'

    document.getElementById('navbar').innerHTML += dashboardHTML + enrolmentHTML + logoutLink + saveForm
}

//====CLASS LIST PAGES====//

function setupTeacherClassListPage() {
    extractLSData()
    setupTeacherNavbar('classList.html')

    // classes.sort(compareClassYears)
    // localStorage.setItem('classes', JSON.stringify(classes))

    localStorage.setItem('currentClass', null)
    var classList = document.getElementById('classList')
    var altGrey = true
    for (var cl = 0; cl < classes.length; cl++) {
        if (altGrey) {
            var row = '<tr class="altGrey"><td>' + classes[cl].name + '</td>\
            <td>' + classes[cl].year + '</td>\
            <td>' + classes[cl].course + '</td>\
            <td>' + classes[cl].teachers.join(', ') + '</td>\
            <td>\
            <a href="manageClass.html" onclick="localStorage.setItem(\'currentClass\',\''+ classes[cl].name +'\')">Manage</a> \
            <a href="editClass.html" onclick="localStorage.setItem(\'currentClass\',\'' + classes[cl].name +'\')">Edit</a> \
            <a href="#" onclick="deleteClass(' + cl + ')">Delete</a>\
            </td></tr>'
            altGrey = false
        } else {
            var row = '<tr><td>' + classes[cl].name + '</td>\
            <td>' + classes[cl].year + '</td>\
            <td>' + classes[cl].course + '</td>\
            <td>' + classes[cl].teachers.join(', ') + '</td>\
            <td>\
            <a href="manageClass.html" onclick="localStorage.setItem(\'currentClass\',\''+ classes[cl].name +'\')">Manage</a> \
            <a href="editClass.html" onclick="localStorage.setItem(\'currentClass\',\'' + classes[cl].name +'\')">Edit</a> \
            <a href="#" onclick="deleteClass(' + cl + ')">Delete</a>\
            </td></tr>'
            altGrey = true
        }
        classList.innerHTML += row
    }
}

function setupAddClassPage() {
    extractLSData()
    setupTeacherNavbar('addClass.html')

    document.addClassForm.year.value = '2017'

    var coursesSelect = document.getElementById('courses')
    for (var c = 0; c < courses.length; c++) {
        var option = '<option value="' + c + '">' + courses[c].name + '</option>'
        coursesSelect.innerHTML += option
    }
}

function setupEditClassPage() {
    classes = JSON.parse(localStorage.getItem('classes'))
    extractLSData()
    setupTeacherNavbar('editClass.html')
    var cl = getCurrentClass()

    document.editClassForm.className.placeholder = ''
    document.editClassForm.className.value = classes[cl].name
    document.editClassForm.year.value = classes[cl].year

    var coursesSelect = document.getElementById('courses')
    for (var c = 0; c < courses.length; c++) {
        var option = '<option value="' + c + '">' + courses[c].name + '</option>'
        coursesSelect.innerHTML += option
    }
    var teachers = document.getElementById('teachers')
    for (var tch = 0; tch < classes[cl].teachers.length; tch++) {
        teachers.innerHTML += createTeacherDiv(classes[cl].teachers[tch])
    }
}

function createTeacherDiv(teacher) {
    // Creates a teacher div
    var select = '<select id="teacherName" value="' + teacher + '">'
    for (var tch = 0; tch < teachers.length; tch++) {
        select += '<option value="' + teachers[tch].name + '">' + teachers[tch].name + '</option>'
    }
    select += '</select>'

    var teacherDiv = '<div class="teacher">\
    <h4>Teacher</h4>' + select + '<br>\
    <a onclick="removeTeacherDiv(this.parentElement)">Remove Teacher</a></div>'
    return teacherDiv
}

function addTeacherDiv() {
    // Allows another teacher to be selected and added
    var select = '<select id="teacherName">'
    for (var tch = 0; tch < teachers.length; tch++) {
        select += '<option value="' + teachers[tch].name + '">' + teachers[tch].name + '</option>'
    }
    select += '</select>'

    var teacherDiv = '<div class="teacher">\
    <h4>Teacher</h4>' + select + '<br>\
    <a onclick="removeTeacherDiv(this.parentElement)">Remove Teacher</a></div>'
    document.getElementById('teachers').innerHTML += teacherDiv
}


function showAttachments(t, tg, tk) {
    for (var a = 0; a < topics[t].taskgroups[tg].tasks[tk].attachments.length; a++) {
        var attachmentDiv = '<div class="attachment"><h4>Attachment</h4> \
        ' + topics[t].taskgroups[tg].tasks[tk].attachments[a].covername + ' <a href="Attachments/' + topics[t].taskgroups[tg].tasks[tk].attachments[a].filename + '">Download</a><br>\
        <a href="#" onclick="removeAttachmentFromTask('+t+','+tg+','+tk+','+a+'); removeTeacherDiv(this.parentElement)">Remove Attachment</a>'

        document.getElementById('attachments').innerHTML += attachmentDiv
    }
}

function removeAttachmentFromTask(t, tg, tk, a) {
    topics[t].taskgroups[tg].tasks[tk].attachments.splice(a,1)
    localStorage.setItem('topics', JSON.stringify(topics))
}

function addAttachmentDiv() {
    // Allows an attachment to be added
    var attachmentDiv = '<div class="attachment">\
    <form name="addAttachment" action="addAttachment.py" method="POST" enctype="multipart/form-data"> \
    <h4>Attachment</h4> \
    <input type="text" name="attachmentName" /><br> \
    <input type="file" name="attachment" /><br> \
    <input name="topic" style="display: none" value="' + getCurrentTopic() +'" /> \
    <input name="taskgroup" style="display: none"  value="' + getCurrentTaskGroup() + '" /> \
    <input name="task" style="display: none" value="' + getCurrentTask() + '" /> \
    <input type="submit" value="Add Attachment" /><br> \
    <a onclick="removeTeacherDiv(this.parentElement)">Remove Attachment</a>\
        </form></div>'

    document.getElementById('attachments').innerHTML += attachmentDiv
}


function updateClass() {
    var cl = getCurrentClass()
    classes[cl].name = document.editClassForm.className.value
    classes[cl].year = document.editClassForm.year.value
    var teachersList = document.getElementById('teachers')

    var classTeachers = []
    for (var e = 1; e < teachersList.childElementCount+1; e++) {
        if (teachersList.childNodes[e].style.display != 'none') {
            var t = teachersList.childNodes[e].childNodes[2].value
            classTeachers.push(t)
            if (teachers[getTeacherByName(t)].classes.indexOf(classes[cl].name) == -1) {
                teachers[getTeacherByName(t)].classes.push(classes[cl].name)
            }
        }
    }

    classes[cl].teachers = classTeachers


    localStorage.setItem('classes', JSON.stringify(classes))
    localStorage.setItem('teachers', JSON.stringify(teachers))
    window.location.href = 'classList.html'
}

function removeTeacherDiv(element) {
    element.style.display = 'none'
}

function createClass() {
    var name = document.addClassForm.className.value
    var year = document.addClassForm.year.value
    var courseSelect = parseInt(document.getElementById('courses').value)
    var courseName = courses[courseSelect].name
    var newClass = new Class(name, year, courseName)
    courses[courseSelect].classes.push(name)
    classes.push(newClass)

    localStorage.setItem('courses', JSON.stringify(courses))
    localStorage.setItem('classes', JSON.stringify(classes))
    window.location.href = 'classList.html'
}


//====COURSE LIST PAGE====//

function setupTeacherCourseListPage() {
    // Sets up the page of list of courses for a teacher
    extractLSData()
    setupTeacherNavbar('courseList.html')
    // courses.sort(compareCourseYears)
    // localStorage.setItem('courses', JSON.stringify(courses))

    var courseList = document.getElementById('courseList')

    var altGrey = true
    for (var c = 0; c < courses.length; c++) {
        if (altGrey) {
            var row = '<tr class="altGrey"><td>' + courses[c].name + '</td>\
            <td>' + courses[c].year + '</td>\
            <td>\
            <a href="manageCourse.html" onclick="localStorage.setItem(\'currentCourse\', \'' + courses[c].name + '\')">Manage</a>\
            <a href="editCourse.html" onclick="localStorage.setItem(\'currentCourse\', \'' + courses[c].name + '\')">Edit</a>\
            <a href="viewCourseStudent.html" onclick="localStorage.setItem(\'currentCourse\', \'' + courses[c].name + '\')">Student View</a>\
            <a onclick="deleteCourse(' + c + ')">Delete</a>'
            altGrey = false
        } else {
            var row = '<tr><td>' + courses[c].name + '</td>\
            <td>' + courses[c].year + '</td>\
            <td>\
            <a href="manageCourse.html" onclick="localStorage.setItem(\'currentCourse\', \'' + courses[c].name + '\')">Manage</a>\
            <a href="editCourse.html" onclick="localStorage.setItem(\'currentCourse\', \'' + courses[c].name + '\')">Edit</a>\
            <a href="viewCourseStudent.html" onclick="localStorage.setItem(\'currentCourse\', \'' + courses[c].name + '\')">Student View</a>\
            <a onclick="deleteCourse(' + c + ')">Delete</a>'
            altGrey = true
        }
        courseList.innerHTML += row
    }
    console.log(courses)
}

function setupAddCoursePage() {
    // Sets up the page to add a Course
    extractLSData()
    setupTeacherNavbar('addCourse.html')
}

function setupEditCoursePage() {
    // Sets up the page to edit a specific course
    extractLSData()
    setupTeacherNavbar('editCourse.html')
    document.editCourseForm.courseName.placeholder = ''
    document.editCourseForm.year.placeholder = ''
    document.editCourseForm.courseName.value = cC
    var c = getCurrentCourse()
    document.editCourseForm.year.value = courses[c].year
}

function updateCourse() {
    // Updates a course's details
    var name = document.editCourseForm.courseName.value
    var year = document.editCourseForm.year.value

    var c = getCurrentCourse()
    courses[c].name = name
    courses[c].year = year
    localStorage.setItem('courses', JSON.stringify(courses))
    window.location.href = 'courseList.html'
}

function createCourse() {
    // Creates a new course
    var name = document.addCourseForm.courseName.value
    var year = document.addCourseForm.year.value

    var newCourse = new Course(name, year)
    courses.push(newCourse)
    localStorage.setItem('courses', JSON.stringify(courses))
    window.location.href = 'courseList.html'
}

function setupManageCoursePage() {
    // Sets up the page to manage a course
    extractLSData()
    setupTeacherNavbar('manageCourse.html')

    var c = getCurrentCourse()

    topicList = document.getElementById('topicList')

    var altGrey = true
    for (var t = 0; t < courses[c].topics.length; t++) {
        var name = '<td>' + courses[c].topics[t].covername + '</td>'
        var topic = '<td>' + courses[c].topics[t].topicname + '</td>'
        var actions = '<td><a href="renameCourseTopic.html" onclick="localStorage.setItem(\'currentTopic\',\''
                        + courses[c].topics[t].topicname +'\')">Rename</a> \
                       <a href="manageTopic.html" onclick="localStorage.setItem(\'currentTopic\',\''
                        + courses[c].topics[t].topicname +'\')">Manage</a> <a onclick="removeTopic(' + t + ')">Remove</a></td>'
        if (altGrey) {
            var row = '<tr class="altGrey">' + name + topic + actions + '</tr>'
            altGrey = false
        } else {
            var row = '<tr>' + name + topic + actions + '</tr>'
            altGrey = true
        }
        topicList.innerHTML += row
    }

    var classList = []
    for (var cl = 0; cl < courses[c].classes.length; cl++) {
        classList.push('<a href="manageClass.html" onclick="localStorage.setItem(\'currentClass\',\'' + courses[c].classes[cl] + '\')">' + courses[c].classes[cl] + '</a>')
    }

    document.getElementById('courseClasses').innerHTML = classList.join(', ')
    document.getElementById('courseTitle').innerHTML = courses[c].name
}

function setupAddTopicToCoursePage() {
    // Sets up the page to add a topic to a course
    extractLSData()
    setupTeacherNavbar('addTopicToCourse.html')
    var c = getCurrentCourse()

    for (var t = 0; t < topics.length; t++) {
        var option = '<option value=' + t + '>' + topics[t].name + '</option>'
        document.getElementById('topic').innerHTML += option
    }
}

function addTopicToCourse() {
    // Adds a topic to a course
    var c = getCurrentCourse()
    var name = document.addTopicToCourseForm.coverName.value
    var topicRef = parseInt(document.addTopicToCourseForm.topic.value)
    var topic = topics[topicRef].name

    var courseTopic = new CourseTopic(name, topic)
    courses[c].topics.push(courseTopic)
    topics[topicRef].courses.push(courses[c].name)

    localStorage.setItem('courses', JSON.stringify(courses))
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageCourse.html'
}

function setupRenameCourseTopicPage() {
    // Sets up the page to rename a course-topic
    extractLSData()
    setupTeacherNavbar('renameCourseTopic.html')
    var c = getCurrentCourse()
    var t = getCurrentCourseTopic()
    document.renameCourseTopicForm.coverName.placeholder = ''
    document.renameCourseTopicForm.coverName.value = courses[c].topics[t].covername
}

function renameCourseTopic() {
    // Renames a course-topic
    var c = getCurrentCourse()
    var t = getCurrentCourseTopic()
    courses[c].topics[t].covername = document.renameCourseTopicForm.coverName.value
    localStorage.setItem('courses', JSON.stringify(courses))
    window.location.href = 'manageCourse.html'
}

//====TOPIC LIST PAGE====//

function setupTeacherTopicListPage() {
    // Sets up the page with the list of topics for a teacher
    extractLSData()
    setupTeacherNavbar('topicList.html')

    var topicList = document.getElementById('topicList')
    var altGrey = true
    for (var t = 0; t < topics.length; t++) {
        if (altGrey) {
            var row = '<tr class="altGrey"><td>' + topics[t].name + '<td>' + genLinksToCoursesForTopic(t) +'</td>\
            <td>\
            <a href="manageTopic.html" onclick="localStorage.setItem(\'currentTopic\', \'' + topics[t].name +'\')">Manage</a>\
            <a href="editTopic.html" onclick="localStorage.setItem(\'currentTopic\', \'' + topics[t].name + '\')">Edit</a>\
            <a href="duplicateTopic.html" onclick="localStorage.setItem(\'currentTopic\', \'' + topics[t].name + '\')">Duplicate</a>\
            <a onclick="deleteTopic(' + t + ')">Delete</a>'
            altGrey = false
        } else {
            var row = '<tr><td>' + topics[t].name + '<td>' + genLinksToCoursesForTopic(t) +'</td>\
            <td>\
            <a href="manageTopic.html" onclick="localStorage.setItem(\'currentTopic\', \'' + topics[t].name +'\')">Manage</a>\
            <a href="editTopic.html" onclick="localStorage.setItem(\'currentTopic\', \'' + topics[t].name + '\')">Edit</a>\
            <a href="duplicateTopic.html" onclick="localStorage.setItem(\'currentTopic\', \'' + topics[t].name + '\')">Duplicate</a>\
            <a onclick="deleteTopic(' + t + ')">Delete</a>'
            altGrey = true
        }
        topicList.innerHTML += row
    }
}

function setupAddTopicPage() {
    // Sets up the page to add a topic
    extractLSData()
    setupTeacherNavbar('addTopic.html')
}

function setupEditTopicPage() {
    // Sets up the page to edit a topic
    extractLSData()
    setupTeacherNavbar('editTopic.html')
    document.editTopicForm.topicName.placeholder = ''
    document.editTopicForm.topicName.value = cTP
}

function setupDuplicateTopicPage() {
    extractLSData()
    setupTeacherNavbar('duplicateTopic.html')
    var t = getCurrentTopic()
    document.getElementById('topicName').innerHTML = topics[t].name
}



function createTopic() {
    // Creates a topic
    var name = document.addTopicForm.topicName.value
    var newTopic = new Topic(name)
    topics.push(newTopic)
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'topicList.html'
}

function updateTopic() {
    // Updates a topic
    var name = document.editTopicForm.topicName.value
    var t = getCurrentTopic()

    for (var c = 0; c < courses.length; c++) {
        for (var tp = 0; tp < courses[c].topics.length; tp++) {
            if (courses[c].topics[tp].topicname == topics[t].name) {
                courses[c].topics[tp].topicname = name
            }
        }
    }

    topics[t].name = name
    localStorage.setItem('topics', JSON.stringify(topics))
    localStorage.setItem('courses', JSON.stringify(courses))
    window.location.href = 'topicList.html'
}

//====TOPIC PAGES====//

function setupTopicManagePage() {
    // Sets up the page to manage a topic
    extractLSData()
    setupTeacherNavbar('manageTopic.html')

    var t = getCurrentTopic()
    document.getElementById('topicTitle').innerHTML = topics[t].name
    document.getElementById('topicCourses').innerHTML = topics[t].courses.join(', ')

    var altGrey = true

    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        var title = '<td>' + topics[t].taskgroups[tg].name + '</td>'
        var numberOfTasks = ' <td>' + topics[t].taskgroups[tg].tasks.length + '</td>'
        var actions = ' <td><a href="editTaskGroup.html" \
        onclick="localStorage.setItem(\'currentTaskGroup\', \'' + topics[t].taskgroups[tg].name + '\')">Edit</a>\
                        <a href="moveTaskGroup.html">Move</a> <a href="#" onclick="deleteTaskGroup(' + tg +')">Delete</a>'
        if (altGrey) {
            var taskGroupRow = '<tr class="altGrey">' + title + numberOfTasks + actions + '</tr>'
            altGrey = false
        } else {
            var taskGroupRow = '<tr>' + title + numberOfTasks + actions + '</tr>'
            altGrey = true
        }
        document.getElementById('taskGroupList').innerHTML += taskGroupRow

        var taskGroupName = '<h3>' + topics[t].taskgroups[tg].name + '</h3>'
        var newTaskButton = '<div class="teacherButton">\
        <a href="addTask.html" onclick="localStorage.setItem(\'currentTaskGroup\',\'' + topics[t].taskgroups[tg].name + '\')">New Task</a></div>'
        var reorderTasksButton = '<div class="teacherButton" onclick="reorderTasks(this,' + tg + ')" style="margin-right: 100px;" name="notReordering" id="reorderTasksButton">Reorder Tasks</div>'

        if (topics[t].taskgroups[tg].tasks.length != 0) {
            var taskListTable = '<table id="taskGroup' + tg + '"><tr><td>Name</td><td>Difficulty</td><td>Actions</td></tr>'

            var altGrey1 = true
            for (var task = 0; task < topics[t].taskgroups[tg].tasks.length; task++) {
                var name = '<td><a href="viewTask.html" onclick="localStorage.setItem(\'currentTask\',\'' +
                    topics[t].taskgroups[tg].tasks[task].name + '\'); localStorage.setItem(\'currentTaskGroup\', \'' +
                    topics[t].taskgroups[tg].name + '\')">' + topics[t].taskgroups[tg].tasks[task].name + '</td>'
                var difficulty = '<td>' + topics[t].taskgroups[tg].tasks[task].difficulty + '</td>'
                var actions = '<td><a href="editTask.html" onclick="localStorage.setItem(\'currentTask\',\'' +
                    topics[t].taskgroups[tg].tasks[task].name + '\'); localStorage.setItem(\'currentTaskGroup\', \'' +
                    topics[t].taskgroups[tg].name + '\')">Edit</a> <a href="#">Move</a> \
                    <a href="#" onclick="deleteTask(' + tg + ','+ task + ')">Delete</a> <a href="addFileToTask.html" onclick="localStorage.setItem(\'currentTask\',\'' +
                    topics[t].taskgroups[tg].tasks[task].name + '\'); localStorage.setItem(\'currentTaskGroup\', \'' +
                    topics[t].taskgroups[tg].name + '\')">Attachments</a> </td>'

                if (altGrey1) {
                    var taskRow = '<tr class="altGrey">' + name + difficulty + actions + '</tr>'
                    altGrey1 = false
                } else {
                    var taskRow = '<tr>' + name + difficulty + actions + '</tr>'
                    altGrey1 = true
                }
                taskListTable += taskRow
            }

            var taskGroupSection = '<div>' + taskGroupName + newTaskButton + reorderTasksButton + taskListTable + '<hr>' + '</table>'
            document.getElementById('tasksList').innerHTML += taskGroupSection
        } else {
            var noTasksSection = '<div>There are no tasks for this task group.</div>'
            document.getElementById('tasksList').innerHTML += '<div>' + taskGroupName + newTaskButton + '<hr>' + '<div class="blueAlert">' +noTasksSection + '</div></div>'
        }
    }
}


//====TASK GROUP PAGES====//

function setupAddTaskGroupPage() {
    // Sets up the page to add a task group
    extractLSData()
    setupTeacherNavbar('addTaskGroup.html')

    var t = getCurrentTopic()
    document.getElementById('topicTitle').innerHTML = topics[t].name
}

function createTaskGroup() {
    // Creates a task group
    var name = document.addTaskGroup.taskGroupName.value
    var newTaskGroup = new Taskgroup(name)
    var t = getCurrentTopic()
    topics[t].taskgroups.push(newTaskGroup)
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageTopic.html'
}

function setupTaskGroupEditPage() {
    // Sets up the page to edit a task group
    extractLSData()
    setupTeacherNavbar('editTaskGroup.html')

    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()

    document.editTaskGroupForm.taskGroupName.placeholder = ''
    document.editTaskGroupForm.taskGroupName.value = topics[t].taskgroups[tg].name
}

function updateTaskGroup() {
    // Updates a task group's core details
    var name = document.editTaskGroupForm.taskGroupName.value
    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()

    topics[t].taskgroups[tg].name = name
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageTopic.html'
}


//====TASK PAGES====//

function createTask() {
    // Creates a new task
    var name = document.addTask.taskName.value
    var difficulty = document.addTask.difficulty.value
    var description = document.addTask.description.value.replace('\n', '<br>')
    var hint = document.addTask.hint.value
    var solution = document.addTask.solution.value

    var newTask = new Task(name, difficulty, description, hint, solution)
    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()
    topics[t].taskgroups[tg].tasks.push(newTask)
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageTopic.html'
}

function updateTask() {
    var name = document.editTaskForm.taskName.value
    var difficulty = document.editTaskForm.difficulty.value
    var description = document.editTaskForm.description.value.replace('\n', '<br>')
    var hint = document.editTaskForm.hint.value
    var solution = document.editTaskForm.solution.value

    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()
    var tk = getCurrentTask()
    topics[t].taskgroups[tg].tasks[tk].name = name
    topics[t].taskgroups[tg].tasks[tk].difficulty = difficulty
    topics[t].taskgroups[tg].tasks[tk].description = description
    topics[t].taskgroups[tg].tasks[tk].hint = hint
    topics[t].taskgroups[tg].tasks[tk].solution = solution
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageTopic.html'
}

function addAttachment(t, tg, tk, covername, filename) {
    extractLSData()
    var attachment = new Attachment(covername, filename)
    topics[t].taskgroups[tg].tasks[tk].attachments.push(attachment)
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageTopic.html'
}

function setupAddTaskPage() {
    // Sets up the page to add a task
    extractLSData()
    setupTeacherNavbar('addTaskGroup.html')

    var t = getCurrentTopic()
    document.getElementById('topicTitle').innerHTML = topics[t].name
    var tg = getCurrentTaskGroup()
    document.getElementById('taskGroupTitle').innerHTML = topics[t].taskgroups[tg].name
}

function setupViewTaskPage() {
    extractLSData()
    setupTeacherNavbar()
    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()
    var tk = getCurrentTask()

    document.getElementById('topicTitle').innerHTML = topics[t].name
    document.getElementById('taskGroupTitle').innerHTML = topics[t].taskgroups[tg].name

    document.getElementById('taskName').innerHTML = topics[t].taskgroups[tg].tasks[tk].name
    document.getElementById('description').innerHTML = topics[t].taskgroups[tg].tasks[tk].description
    document.getElementById('hint').innerHTML = topics[t].taskgroups[tg].tasks[tk].hint
    document.getElementById('solution').innerHTML = topics[t].taskgroups[tg].tasks[tk].solution

    var attachmentList = document.getElementById('attachments')
    for (var a = 0; a < topics[t].taskgroups[tg].tasks[tk].attachments.length; a++) {
        attachmentList.innerHTML += '<li>' + topics[t].taskgroups[tg].tasks[tk].attachments[a].covername + '</li>'
    }
}

function setupEditTaskPage() {
    extractLSData()
    setupTeacherNavbar('editTask.html')
    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()
    var tk = getCurrentTask()

    document.getElementById('topicTitle').innerHTML = topics[t].name
    document.getElementById('taskGroupTitle').innerHTML = topics[t].taskgroups[tg].name

    document.editTaskForm.taskName.value = topics[t].taskgroups[tg].tasks[tk].name
    document.editTaskForm.description.value = topics[t].taskgroups[tg].tasks[tk].description.replace('<br>', '\n')
    document.editTaskForm.hint.value = topics[t].taskgroups[tg].tasks[tk].hint
    document.editTaskForm.solution.value = topics[t].taskgroups[tg].tasks[tk].solution
}


//====CLASS PAGES====//

function setupManageClassPage() {
    extractLSData()
    setupTeacherNavbar('manageClass.html')

    var cl = getCurrentClass()

    studentList = document.getElementById('studentList')

    var altGrey = true
    for (var s = 0; s < classes[cl].students.length; s++) {
        var student = getStudentById(classes[cl].students[s])
        var name = '<td>' + students[student].name + '</td>'
        var id = '<td>' + students[student].id + '</td>'
        var actions = '<td><a href="studentDetails.html">Details</a> \
                       <a href="#" onclick="removeStudentFromClass(' + s + ')">Remove</a></td>'
        if (altGrey) {
            var row = '<tr class="altGrey">' + name + id + actions + '</tr>'
            altGrey = false
        } else {
            var row = '<tr>' + name + id + actions + '</tr>'
            altGrey = true
        }
        studentList.innerHTML += row
    }

    document.getElementById('classTitle').innerHTML = classes[cl].name
    document.getElementById('classTeachers').innerHTML = classes[cl].teachers.join(', ')
    document.getElementById('classCourse').innerHTML = '<a href="manageCourse.html" \
    onclick="localStorage.setItem(\'currentCourse\',\''+ classes[cl].course +'\')">' + classes[cl].course + '</a>'

}

function setupAddFileToTaskPage() {
    extractLSData()
    setupTeacherNavbar('addFileToTask.html')

    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()
    var tk = getCurrentTask()

    showAttachments(t, tg, tk)

    document.getElementById('topicTitle').innerHTML = topics[t].name
    document.getElementById('taskGroupTitle').innerHTML = topics[t].taskgroups[tg].name
    document.getElementById('taskTitle').innerHTML = topics[t].taskgroups[tg].tasks[tk].name
}

function setupAddEnrolmentPage() {
    extractLSData()
    setupTeacherNavbar('addEnrolment.html')
    var cl = getCurrentClass()

    document.getElementById('className').innerHTML = classes[cl].name

    var studentList = document.getElementById('students')
    for (var s = 0; s < students.length; s++) {
        var option = '<option value="' + students[s].id + '">' + students[s].name + '</option>'
        studentList.innerHTML += option
    }
}

function addEnrolment() {
    var student = document.getElementById('students').value
    var cl = getCurrentClass()
    var studentIndex = getStudentById(student)
    var enrolment = new Enrolment(classes[cl].name)

    classes[cl].students.push(student)
    students[studentIndex].enrolments.push(enrolment)

    localStorage.setItem('students', JSON.stringify(students))
    localStorage.setItem('classes', JSON.stringify(classes))

    window.location.href = 'manageClass.html'
}


//====DELETION====//

function deleteTaskGroup(tg) {
    var t = getCurrentTopic()
    if (topics[t].taskgroups[tg].tasks.length != 0) {
        alert('Task group could not be deleted.\nYou must remove it from any courses before deletion.')
    } else {
        if (confirm('Are you sure you want to delete "' + topics[t].taskgroups[tg].name + '"?')) {
            topics[t].taskgroups.splice(getTaskGroupByName(t, topics[t].taskgroups[tg].name), 1)
            localStorage.setItem('topics', JSON.stringify(topics))
            window.location.href = 'manageTopic.html'
            window.location.href = 'manageTopic.html'
        }
    }
}

function deleteTask(tg, tk) {
    var t = getCurrentTopic()
    if (confirm('Are you sure you want to delete "' + topics[t].taskgroups[tg].tasks[tk].name + '"?')) {
        topics[t].taskgroups[tg].tasks.splice(tk, 1)
        localStorage.setItem('topics', JSON.stringify(topics))
        window.location.href = 'manageTopic.html'
    }
}

function deleteTopic(t) {
    console.log(topics[t].courses)
    if (topics[t].courses.length != 0) {
        alert('Topic could not be deleted.\nYou must remove it from any courses before deletion.')
    } else {
        if (confirm('Are you sure you want to delete "' + topics[t].name + '"?')) {
            topics.splice(getTopicByName(topics[t].name), 1)
            localStorage.setItem('topics', JSON.stringify(topics))
            window.location.href = 'topicList.html'
        }
    }
}

function deleteClass(cl) {
    if (classes[cl].students.length != 0) {
        alert('Class could not be deleted.\nYou must remove any students in it before deletion.')
    } else {
        if (confirm('Are you sure you want to delete "' + classes[cl].name + '"?')) {
            classes.splice(getClassByName(classes[cl].name), 1)
            localStorage.setItem('classes', JSON.stringify(classes))
            window.location.href = 'classList.html'
        }
    }
}

function deleteCourse(c) {
    if (courses[c].classes.length != 0) {
        alert('Course could not be deleted.\nYou must delete any classes that have it before deletion.')
    } else {
        if (confirm('Are you sure you want to delete "' + courses[c].name + '"?')) {
            var indexOfCourse = getCourseByName(courses[c].name)
            courses.splice(indexOfCourse, 1)
            localStorage.setItem('courses', JSON.stringify(courses))
            window.location.href = 'courseList.html'
        }
    }
}

function removeStudentFromClass(s) {
    var cl = getCurrentClass()
    cS = students[s].id
    var e = getIndexofEnrolment(getCourseByName(classes[cl].course))
    console.log(e)
    var st = getStudentInClass(students[s].id, cl)
    classes[cl].students.splice(st, 1)
    students[s].enrolments.splice(e, 1)
    console.log(students)
    localStorage.setItem('classes', JSON.stringify(classes))
    localStorage.setItem('students', JSON.stringify(students))
    window.location.href = 'manageClass.html'
}

function removeTopic(t) {
    var c = getCurrentCourse()
    var i1 = getIndexOfTopic(courses[c].topics[t].topicname)
    var i2 = getIndexOfCourseInTopic(i1, courses[c].name)
    var i3 = getIndexOfTopicInCourse(c, topics[i1].name)
    topics[i1].courses.splice(i2,1)
    courses[c].topics.splice(i3,1)
    localStorage.setItem('courses', JSON.stringify(courses))
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageCourse.html'
}

//====STUDENT PAGES====//

function setupViewCourseStudentPage() {
    extractLSData()
    if (cS != null) {
        setupStudentNavbar('viewCourseStudent.html')
    } else {
        setupTeacherNavbar('viewCourseStudent.html')
    }
    console.log(cC)
    var c = getCurrentCourse()

    document.getElementById('courseName').innerHTML = courses[c].name

    var topicProgress = document.getElementById('topicProgress')
    var topicTables = document.getElementById('topicTabs')


    // Setup the progress table
    var topicNameRow = '<tr>'
    var topicProgressRow = '<tr id="progressDashRow">'
    var width = 1 / courses[c].topics.length * 100

    for (var t = 0; t < courses[c].topics.length; t++) {
        topicNameRow += '<td style="width: ' + width + '%;">' + courses[c].topics[t].covername + '</td>'

        // TBD & TBR
        if (cS == null) {
            topicProgressRow += '<td><div class="progressDash"></div></td>'
        } else {
            var completion = getCompletionForTopic(getTopicByName(courses[c].topics[t].topicname))
			console.log(completion)
            var unmarked = completion[0]
            var correct = completion[1]
            var incorrect = completion[2]
            var fillBar = completion[3]
            topicProgressRow += '<td><div class="progressDash">\
            <div class="unmarkedDash" style="width: ' + unmarked + '%;"></div>\
            <div class="correctDash" style="width: ' + correct + '%;"></div>\
            <div class="incorrectDash" style="width: ' + incorrect + '%;"></div>\
            <div class="fillBarDash" style="width: ' + fillBar + '%;"></div></div></td>'
        }
    }
    topicProgress.innerHTML += topicNameRow + '</tr>' + topicProgressRow + '</tr>'


    // Setup the topic tabs
    var topicTabs = document.getElementById('topicTabs')
    for (var t = 0; t < courses[c].topics.length; t++) {
        var tab = '<div class="topicTab" onclick="showTopic(this, \'' + courses[c].topics[t].topicname + '\')" onmouseover="highlightTopicTab(this)" onmouseout="unhighlightTopicTab(this)">' + courses[c].topics[t].covername + '</div>'
        topicTabs.innerHTML += tab
    }
}

function showTopic(el, topicName) {
    removeStylingForTopicTabs(el.parentNode, el)
    el.style.borderTop = '1px solid lightgray'
    el.style.borderLeft = '1px solid lightgray'
    el.style.borderRight = '1px solid lightgray'

    var t = getIndexOfTopic(topicName)
    var taskgroupList = document.getElementById('taskgroupList')

    taskgroupList.innerHTML = ''

    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        var taskGroup = topics[t].taskgroups[tg]

        var taskGroupList = '<span class="taskGroupList" name="undisplayed"><span class="taskGroupName" onmouseover="underline(this)" onmouseout="deunderline(this)" onclick="displayTaskgroup(this.parentNode)">' + taskGroup.name + '</span>'

        for (var tk = 0; tk < taskGroup.tasks.length; tk++) {
            if (cS != null) {
                var submissionState = getSubmissionStateForTask(t, tg, tk)
            } else {
                var submissionState = 'notDone'
            }
            var taskName = '<span style="display: none; " name="' + submissionState + '" onmouseover="underline(this)" onmouseout="deunderline(this)" onclick="displayTask('+tk+',' + tg +',' + t +')" class="'+ taskGroup.tasks[tk].difficulty +'">' + taskGroup.tasks[tk].name + '</span>'
            taskGroupList += taskName
        }

        taskgroupList.innerHTML += taskGroupList + '</span>'
    }
}

function removeStylingForTopicTabs(el, currentTopic) {
    var elements = el.childNodes
    for (var t = 1; t < elements.length; t++) {
        if (elements[t].innerHTML != currentTopic.innerHTML) {
            elements[t].style.border = '0px'
        }
    }
}

function displayTask(tk, tg, t) {
    var taskBox = document.getElementById('taskBox')
    taskBox.innerHTML = '\
    <h1>' + topics[t].taskgroups[tg].tasks[tk].name + '</h1>\
    ' + topics[t].taskgroups[tg].tasks[tk].description
    // Hints and attachments

    for (var a = 0; a < topics[t].taskgroups[tg].tasks[tk].attachments.length; a++) {
        taskBox.innerHTML += '<div class="attachment">' + topics[t].taskgroups[tg].tasks[tk].attachments[a].covername
        + ' <a href="Attachments/' + topics[t].taskgroups[tg].tasks[tk].attachments[a].filename + '">Download</a></div>'
    }


    if (topics[t].taskgroups[tg].tasks[tk].hint) {
        taskBox.innerHTML += '<div class="teacherButton" name="hintHide" onclick="showHint(this, \'' +
        topics[t].taskgroups[tg].tasks[tk].hint + '\')">Show Hint</div><br><br>'
    }

    // Submission
    if (cS != null) {
        var formHeader = '<div class="submissionBox"><h4>Submit Your Solution</h3> \
        <hr><p>Files</p><form name="submit_activity_form" action="submitForTask.py" method="POST" enctype="multipart/form-data">'
        var fileInput = '<input type="file" name="submission"/>'

        var addFileButton = '<div class="greenTeacherButton">Add File</div>'
        var studentID = '<input type="text" name="student" value="' + students[getCurrentStudent()].id + '" style="display: none;"/>'
        var topicInput = '<input type="text" name="topic" value="' + t + '" style="display: none;"/>'
        var taskgroupInput = '<input type="text" name="taskgroup" value="' + tg + '" style="display: none;"/>'
        var taskInput = '<input type="text" name="task" value="' + tk + '" style="display: none;"/>'
        var submitButton = '<input type="submit" value="Submit" />'
        taskBox.innerHTML += formHeader + fileInput + addFileButton + studentID + topicInput + taskgroupInput + taskInput + submitButton + '</div>'

        var submissions = getSubmissionsForTask(t, tg, tk)[0]

        if (submissions.length > 0) {
            var header = '<h4>Submissions</h4>'

            for (var sb = 0; sb < submissions.length; sb++) {
                var submissionDisplay = '<div class="submissionDisplay" name="' + submissions[sb].state + '">' +
                    submissions[sb].comment + ' <strong>' + submissions[sb].state + '</strong> ' + '<a href="Submissions/' + submissions[sb].file + '">Download</a>' + '</div>'
                taskBox.innerHTML += submissionDisplay
            }
        }
    }
}


function submitForTask(filename, t, tg, tk) {
    extractLSData()
    console.log(filename)

    var s = getCurrentStudent()
    var e = getEnrolmentOfStudentByCourse(s, cC)


    for (var sb = 0; sb < students[s].enrolments[e].submissions.length; sb++) {
        if (students[s].enrolments[e].submissions[sb].topic == topics[t].name &&
            students[s].enrolments[e].submissions[sb].task == topics[t].taskgroups[tg].tasks[tk].name &&
           students[s].enrolments[e].submissions[sb].taskgroup == topics[t].taskgroups[tg].name) {
            students[s].enrolments[e].submissions[sb].isObsolete = true
        }
    }


    var submission = new Submission(filename, topics[t].name, topics[t].taskgroups[tg].name, topics[t].taskgroups[tg].tasks[tk].name)
    students[s].enrolments[e].submissions.push(submission)

    localStorage.setItem('students', JSON.stringify(students))
    window.location.href = 'viewCourseStudent.html'
}

function showHint(el, hint) {
    console.log('called')
    el.innerHTML = '<h4>Hint</h4><br><br>' + hint
    el.style.width = '100%'
}

function displayTaskgroup(element) {
    console.log(element)
    if (element.name == 'undisplayed') {
        var elements = element.childNodes
        for (var e = 1; e < elements.length; e++) {
            elements[e].style.display = 'block'
        }
        element.name = 'displayed'
    } else if (element.name == 'displayed') {
        var elements = element.childNodes
        for (var e = 1; e < elements.length; e++) {
            elements[e].style.display = 'none'
        }
        element.name = 'undisplayed'
    } else {
        var elements = element.childNodes
        for (var e = 1; e < elements.length; e++) {
            elements[e].style.display = 'none'
        }
        element.name = 'undisplayed'
        displayTaskgroup(element)
    }
}

function setupClassCourseProgressReportPage() {
    extractLSData()
    setupTeacherNavbar('classCourseProgressReport.html')

    var cl = getCurrentClass()
    var altGrey = false
    var topicProgressTable = document.getElementById('topicProgress')

    document.getElementById('className').innerHTML = classes[cl].name
    document.getElementById('courseName').innerHTML = classes[cl].course



    var topicRow = '<tr><td><h4>Student</h4></td>'
    var c = getCourseByName(classes[cl].course)

    for (var t = 0; t < courses[c].topics.length; t++) {
        topicRow += '<td class="topicName"><a href="classTopicProgressReport.html" onclick="localStorage.setItem(\'currentTopic\', \'' + courses[c].topics[t].topicname + '\')">' + courses[c].topics[t].covername + '</a></td>'
    }

    topicProgressTable.innerHTML += topicRow + '<td><h4>Submitted</h4></td><td><h4>Correct</h4></td></tr>'

    cC = classes[cl].course
    localStorage.setItem('currentCourse', cC)


    for (var s = 0; s < classes[cl].students.length; s++) {
        var row = '<tr><td>' + students[getStudentById(classes[cl].students[s])].name + '</td>'
        cS = classes[cl].students[s]

        for (var t = 0; t < courses[c].topics.length; t++) {
            var completion = getCompletionForTopic(getTopicByName(courses[c].topics[t].topicname))
            var unmarked = completion[0]
            var correct = completion[1]
            var incorrect = completion[2]
            var fillBar = completion[3]
            row += '<td><div class="progressDash">\
            <div class="unmarkedDash" style="width: ' + unmarked + '%;"></div>\
            <div class="correctDash" style="width: ' + correct + '%;"></div>\
            <div class="incorrectDash" style="width: ' + incorrect + '%;"></div>\
            <div class="fillBarDash" style="width: ' + fillBar + '%;"></div></div></td>'
        }

        var courseProgress = getCompletionForCourse(c)

        var progressSubmitted = courseProgress[0] + courseProgress[1] + courseProgress[2]
        var progressCorrect = courseProgress[1]

        row += '<td>' + progressSubmitted.toFixed(2) + '%</td><td>' + progressCorrect.toFixed(2) + '%</td></tr>'

        topicProgressTable.innerHTML += row
    }
}

function setupClassTopicProgressReportPage() {
    extractLSData()
    setupTeacherNavbar('classTopicProgressReport.html')

    var cl = getCurrentClass()
    var t = getCurrentTopic()
    var c = getCourseByName(classes[cl].course)
    var tp = getIndexOfTopicInCourse(c, cTP)

    var taskgroupProgressTable = document.getElementById('taskgroupProgress')

    document.getElementById('className').innerHTML = classes[cl].name
    document.getElementById('topicName').innerHTML = courses[c].topics[tp].covername + ' (' + topics[t].name + ')'

    var taskgroupRow = '<tr><td><h4>Student</h4></td>'
    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        taskgroupRow += '<td><a href="classTaskGroupProgressReport.html" onclick="localStorage.setItem(\'currentTaskGroup\', \'' + topics[t].taskgroups[tg].name + '\')">' + topics[t].taskgroups[tg].name + '</a></td>'
    }

    taskgroupProgressTable.innerHTML += taskgroupRow + '<td><h4>Submitted</h4></td><td><h4>Correct</h4></td></tr>'

    for (var s = 0; s < classes[cl].students.length; s++) {
        var row = '<tr><td>' + students[getStudentById(classes[cl].students[s])].name + '</td>'
        cS = classes[cl].students[s]

        for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
            var completion = getCompletionForTaskGroup(t, tg)
            var unmarked = completion[0]
            var correct = completion[1]
            var incorrect = completion[2]
            var fillBar = completion[3]
            row += '<td><div class="progressDash">\
            <div class="unmarkedDash" style="width: ' + unmarked + '%;"></div>\
            <div class="correctDash" style="width: ' + correct + '%;"></div>\
            <div class="incorrectDash" style="width: ' + incorrect + '%;"></div>\
            <div class="fillBarDash" style="width: ' + fillBar + '%;"></div></div></td>'
        }

        var topicProgress = getCompletionForTopic(t)

        var progressSubmitted = topicProgress[0] + topicProgress[1] + topicProgress[2]
        var progressCorrect = topicProgress[1]

        row += '<td>' + progressSubmitted.toFixed(2) + '%</td><td>' + progressCorrect.toFixed(2) + '%</td></tr>'

        taskgroupProgressTable.innerHTML += row
    }
}

function setupClassTaskGroupProgressReportPage() {
    extractLSData()
    setupTeacherNavbar('classTaskGroupProgressReport.html')

    document.getElementById('classTaskGroupProgressReportPage').onclick = function(el) {
        if (firstClickOutsideDiv) {
            firstClickOutsideDiv = false
            return
        }
        if (el.target != document.getElementsByClassName('viewSubmission')[0]) {
            console.log('outside')
        } else {
            console.log('inside')
        }
    }

    var cl = getCurrentClass()
    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()
    var c = getCourseByName(classes[cl].course)
    var tp = getIndexOfTopicInCourse(c, cTP)

    var taskProgressTable = document.getElementById('taskProgress')

    document.getElementById('className').innerHTML = classes[cl].name
    document.getElementById('taskgroupName').innerHTML = topics[t].taskgroups[tg].name


    var taskRow = '<tr><td><h4>Student</h4></td>'
    for (var tk = 0; tk < topics[t].taskgroups[tg].tasks.length; tk++) {
        taskRow += '<td>' + topics[t].taskgroups[tg].tasks[tk].name + '</td>'
    }

    taskProgressTable.innerHTML += taskRow + '<td><h4>Submitted</h4></td><td><h4>Correct</h4></td></tr>'

    for (var s = 0; s < classes[cl].students.length; s++) {
        var row = '<tr><td>' + students[getStudentById(classes[cl].students[s])].name + '</td>'
        cS = classes[cl].students[s]

        for (var tk = 0; tk < topics[t].taskgroups[tg].tasks.length; tk++) {
            var submissions = getSubmissionsForTask(t, tg, tk)[0]
            var indexes = getSubmissionsForTask(t, tg, tk)[1]
            console.log(submissions)
            var e = getIndexofEnrolment(getCourseByName(classes[cl].course))
            if (submissions.length > 0) {
                var recentSubmission = submissions[submissions.length - 1]
                var indexOfSubmission = indexes[indexes.length - 1]
                var viewSubmission = '<td><div class="progressDash"><div class="'+recentSubmission.state+'Dash" onclick="viewSubmission('+t+','+tg+','+tk+','+s +','+e+','+(indexOfSubmission)+')" style="width: 100%">View Submission</div></div></td>'
                row += viewSubmission
            } else {
                row += '<td><div class="progressDash"></div></td>'
            }
        }

        var taskgroupProgress = getCompletionForTaskGroup(t, tg)

        var progressSubmitted = taskgroupProgress[0] + taskgroupProgress[1] + taskgroupProgress[2]
        var progressCorrect = taskgroupProgress[1]

        row += '<td>' + progressSubmitted.toFixed(2) + '%</td><td>' + progressCorrect.toFixed(2) + '%</td></tr>'

        taskProgressTable.innerHTML += row

    }

}

function viewSubmission(t, tg, tk, s, e, sb) {
    var submission = students[s].enrolments[e].submissions[sb]
    var viewSubmissionDiv = '<div class="viewSubmission">\
    <a href="Submissions/'+ submission.file+'"><h4>Submission File</h4></a><span id="closeWindow" onclick="closeWindow()">Close</span>\
    <div class="teacherButton" id="taskSolutionAlternate" onclick="alternateTaskSolutionOnSubmissionView(this,'+t+','+tg+','+tk+')">Task</div><br><br><div id="taskSolutionContent">' +
    topics[t].taskgroups[tg].tasks[tk].description + '</div>\
    <h4>Comments</h4><form name="addCommentForm">\
    <input type="text" name="comment" value="' + submission.comment + '"/></form>\
    <div class="teacherButton" onclick="addComment(\''+s+'\',\''+e+'\',\''+sb+'\')">Add Comment</div>\
    <div class="greenTeacherButton" onclick="markCorrect(\''+s+'\',\''+e+'\',\''+sb+'\')">Correct</div><div class="redTeacherButton" onclick="markIncorrect(\''+s+'\',\''+e+'\',\''+sb+'\')">Incorrect</div>\
    </form></div>'
    document.getElementById('background').style.opacity = '0.1'
    document.getElementById('classTaskGroupProgressReportPage').innerHTML += viewSubmissionDiv
}

function alternateTaskSolutionOnSubmissionView(el, t, tg, tk) {
    if (el.innerHTML == 'Task') {
        el.innerHTML = 'Solution'
        el.style.backgroundColor = '#5eb95e'
        document.getElementById('taskSolutionContent').innerHTML = topics[t].taskgroups[tg].tasks[tk].solution
    } else {
        el.innerHTML = 'Task'
        el.style.backgroundColor = 'rgb(45, 136, 205)'
        document.getElementById('taskSolutionContent').innerHTML = topics[t].taskgroups[tg].tasks[tk].description
    }
}

function closeWindow() {
    document.getElementsByClassName('viewSubmission')[0].style.display = 'none'
    document.getElementById('background').style.opacity = '1'
    window.location.href = 'classTaskGroupProgressReport.html'
}

function markCorrect(s, e, sb) {
    students[s].enrolments[e].submissions[sb].state = 'correct'
    localStorage.setItem('students', JSON.stringify(students))
    window.location.href = 'classTaskGroupProgressReport.html'
}

function markIncorrect(s, e, sb) {
    students[s].enrolments[e].submissions[sb].state = 'incorrect'
    localStorage.setItem('students', JSON.stringify(students))
    window.location.href = 'classTaskGroupProgressReport.html'
}

function addComment(s, e, sb) {
    students[s].enrolments[e].submissions[sb].comment = document.addCommentForm.comment.value
    localStorage.setItem('students', JSON.stringify(students))
    window.location.href = 'classTaskGroupProgressReport.html'
}

//====DUPLICATION OF TOPICS====//

function duplicateTopic() {
    var t = getCurrentTopic()
    console.log('called')
    var duplicatedTopic = new Topic(document.duplicateTopicForm.topicName.value)
    duplicatedTopic.taskgroups = topics[t].taskgroups
    topics.push(duplicatedTopic)
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'topicList.html'
}

//====HIGHLIGHTING FUNCTIONS====//

function highlightTopicTab(el) {
    el.style.backgroundColor = 'rgb(245, 245, 245)'
}

function unhighlightTopicTab(el) {
    el.style.backgroundColor = 'white'
}

function underline(el) {
    el.style.textDecoration = 'underline'
}

function deunderline(el) {
    el.style.textDecoration = 'none'
}

//====HELPER FUNCTIONS====//

function getTeacherByUsername(username) {
    for (var t = 0; t < teachers.length; t++) {
        if (teachers[t].username == username) {
            return t
        }
    }
    return false
}

function getTeacherByName(name) {
    for (var t = 0; t < teachers.length; t++) {
        if (teachers[t].name == name) {
            return t
        }
    }
    return false
}

function getCurrentTopic() {
    for (var t = 0; t < topics.length; t++) {
        if (topics[t].name == cTP) {
            return t
        }
    }
    return false
}

function getCurrentTaskGroup() {
    var t = getCurrentTopic()
    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        if (topics[t].taskgroups[tg].name == cTG) {
            return tg
        }
    }
    return false
}

function getCurrentTask() {
    var t = getCurrentTopic()
    var tg = getCurrentTaskGroup()
    for (var task = 0; task < topics[t].taskgroups[tg].tasks.length; task++) {
        if (topics[t].taskgroups[tg].tasks[task].name == cTK) {
            return task
        }
    }
    return false
}

function getCurrentCourse() {
    for (var c = 0; c < courses.length; c++) {
        if (courses[c].name == cC) {
            return c
        }
    }
    return false
}

function getCurrentClass() {
    for (var cl = 0; cl < classes.length; cl++) {
        if (classes[cl].name == cCL) {
            return cl
        }
    }
    return false
}

function getClassByName(name) {
    for (var cl = 0; cl < classes.length; cl++) {
        if (classes[cl].name == name) {
            return cl
        }
    }
}

function getCourseByName(name) {
    for (var c = 0; c < courses.length; c++) {
        if (courses[c].name == name) {
            return c
        }
    }
}

function getTopicByName(name) {
    for (var t = 0; t < topics.length; t++) {
        if (topics[t].name == name) {
            return t
        }
    }
}

function getTaskGroupByName(t, name) {
    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        if (topics[t].taskgroups[tg].name == name) {
            return tg
        }
    }
}

function getCurrentCourseTopic() {
    var c = getCurrentCourse()
    for (var t = 0; t < courses[c].topics.length; c++) {
        if (courses[c].topics[t].topicname == cTP) {
            return t
        }
    }
    return false
}

function getTaskByName(t, tg, name) {
    for (var tk = 0; tk < topics[t].taskgroups[tg].tasks.length; tk++) {
        if (topics[t].taskgroups[tg].tasks[tk].name == name) {
            return tk
        }
    }
}

function getStudentById(ID) {
    for (var s = 0; s < students.length; s++) {
        if (students[s].id == ID) {
            return s
        }
    }
    return false
}

function getCurrentStudent() {
    for (var s = 0; s < students.length; s++) {
        if (students[s].id == cS) {
            return s
        }
    }
}

function getStudentInClass(id, cl) {
    for (var s = 0; s < classes[cl].students.length; cl++) {
        if (classes[cl].students[s] == id) {
            return s;
        }
    }
}

function getEnrolmentOfStudentByCourse(s, c) {
    var student = students[s]
    for (var e = 0; e < student.enrolments.length; e++) {
        var cl = getClassByName(student.enrolments[e].classref)
        if (classes[cl].course == c) {
            return e
        }
    }
}


function getCourseTopicNames(c) {
    var topicnames = []
    for (var t = 0; t < courses[c].topics; t++) {
        topicnames.push(courses[c].topics[t].topicname)
    }
    return topicnames
}

function getIndexOfTopic(topicname) {
    for (var t = 0; t < topics.length; t++) {
        if (topics[t].name == topicname) {
            return t
        }
    }
}

function getIndexOfCourseInTopic(t, coursename) {
    for (var c = 0; c < topics[t].courses.length; c++) {
        if (topics[t].courses[c].name == coursename) {
            return c
        }
    }
}

function getIndexOfTopicInCourse(c, topicname) {
    for (var t = 0; t < courses[c].topics.length; t++) {
        if (courses[c].topics[t].topicname == topicname) {
            return t
        }
    }
}

function getIndexOfTopicInCourseByCovername(c, covername) {
    for (var t = 0; t < courses[c].topics.length; t++) {
        if (courses[c].topics[t].covername == covername) {
            return t
        }
    }
}

function genLinksToCoursesForTopic(t) {
    var links = []
    for (var c = 0; c < topics[t].courses.length; c++) {
        var link = '<a href="manageCourse.html" onclick="localStorage.setItem(\'currentCourse\', \'' +
        topics[t].courses[c] + '\')">' + topics[t].courses[c] + '</a>'
        links.push(link)
    }

    return links.join(', ')
}

function getIndexOfTaskGroupInTopic(t, name) {
    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        if (topics[t].taskgroups[tg].name == name) {
            return tg
        }
    }
    return false
}

function getIndexOfTaskInTaskGroup(t, tg, name) {
    for (var tk = 0; tk < topics[t].taskgroups[tg].tasks.length; tk++) {
        if (topics[t].taskgroups[tg].tasks[tk].name == name) {
            return tk
        }
    }
}

//==COMPLETION FUNCTIONS==//

function getIndexofEnrolment(c) {
    var s = getCurrentStudent()
    var enrolments = students[s].enrolments
    console.log(enrolments)
    for (var e = 0; e < enrolments.length; e++) {
        console.log(classes[getClassByName(enrolments[e].classref)].course)
        if (classes[getClassByName(enrolments[e].classref)].course == courses[c].name) {
            return e
        }
    }
    return false
}


function getCompletionForCourse(c) {
    var length = 0
    var totalUnmarked = 0
    var totalCorrect = 0
    var totalIncorrect = 0
    var e = getIndexofEnrolment(c)

    for (var tp = 0; tp < courses[c].topics.length; tp++) {
        var t = getTopicByName(courses[c].topics[tp].topicname)
        console.log(t)

        length += getNumberOfTasksForTopic(t)

        for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
            totalUnmarked += getProgressOfStateForTaskGroup(t, tg, e, 'unmarked')
            totalCorrect += getProgressOfStateForTaskGroup(t, tg, e, 'correct')
            totalIncorrect += getProgressOfStateForTaskGroup(t, tg, e, 'incorrect')
        }
    }

    var progressUnmarked = totalUnmarked / length * 100
    var progressCorrect = totalCorrect/ length * 100
    var progressIncorrect = totalIncorrect / length * 100
    var percentLeft = 100 - progressUnmarked - progressCorrect - progressIncorrect

    return [progressUnmarked, progressCorrect, progressIncorrect]
}

function getCompletionForTopic(t) {
    var length = getNumberOfTasksForTopic(t)

    if (length == 0) {
        return [0,0,0]
    }

    var e = getIndexofEnrolment(getCourseByName(cC))
    var totalUnmarked = 0
    var totalCorrect = 0
    var totalIncorrect = 0
    console.log(e)
    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        totalUnmarked += getProgressOfStateForTaskGroup(t, tg, e, 'unmarked')
        totalCorrect += getProgressOfStateForTaskGroup(t, tg, e, 'correct')
        totalIncorrect += getProgressOfStateForTaskGroup(t, tg, e, 'incorrect')
    }

    var percentUnmarked = totalUnmarked/length * 100
    var percentCorrect = totalCorrect/length * 100
    var percentIncorrect = totalIncorrect/length * 100
    var percentLeft = 100 - percentUnmarked - percentCorrect - percentIncorrect

    return [percentUnmarked, percentCorrect, percentIncorrect, percentLeft]
}


function getCompletionForTaskGroup(t, tg) {
    var length = topics[t].taskgroups[tg].tasks.length

    if (length == 0) {
        return [0,0,0]
    }

    var e = getIndexofEnrolment(getCourseByName(cC))

    var progressUnmarked = getProgressOfStateForTaskGroup(t, tg, e, 'unmarked') / length * 100
    var progressCorrect = getProgressOfStateForTaskGroup(t, tg, e, 'correct') / length * 100
    var progressIncorrect = getProgressOfStateForTaskGroup(t, tg, e, 'incorrect') / length * 100

    return [progressUnmarked, progressCorrect, progressIncorrect]
}

function getProgressOfStateForTaskGroup(t, tg, e, state) {
    var s = getCurrentStudent()
    var counter = 0
    console.log([t, tg, e, state])
    console.log(students[s].enrolments[e])
    var submissions = students[s].enrolments[e].submissions


    for (var sb = 0; sb < submissions.length; sb++) {
        if (submissions[sb].state == state && submissions[sb].topic == topics[t].name
            && submissions[sb].taskgroup == topics[t].taskgroups[tg].name && !submissions[sb].isObsolete) {
            counter += 1
        }
    }
    return counter
}

function getNumberOfTasksForTopic(t) {
    var counter = 0
    for (var tg = 0; tg < topics[t].taskgroups.length; tg++) {
        for (var tk = 0; tk < topics[t].taskgroups[tg].tasks.length; tk++) {
            counter += 1
        }
    }

    return counter
}

function getSubmissionsForTask(t, tg, tk) {
    var s = getCurrentStudent()
    var e = getIndexofEnrolment(getCourseByName(cC))
    var submissions = students[s].enrolments[e].submissions
    var taskSubmissions = []
    var taskSubmissionIndexes = []

    for (var sb = 0; sb < submissions.length; sb++) {
        if (submissions[sb].topic == topics[t].name && submissions[sb].task == topics[t].taskgroups[tg].tasks[tk].name &&
           submissions[sb].taskgroup == topics[t].taskgroups[tg].name) {
            taskSubmissions.push(submissions[sb])
            taskSubmissionIndexes.push(sb)
        }
    }

    return [taskSubmissions, taskSubmissionIndexes]
}

function getSubmissionStateForTask(t, tg, tk) {
    var submissions = getSubmissionsForTask(t, tg, tk)[0]
    if (submissions.length > 0) {
        return submissions[submissions.length - 1].state
    } else {
        return 'notDone'
    }
}

//====DRAG AND DROP EVENT HANDLERS====//

function handleDragStart(el) {
    this.style.opacity = '0.4'
    dragSrcEl = this
    el.dataTransfer.effectAllowed = 'none'
    el.dataTransfer.setData('text/html', this.innerHTML)
}

function handleDragOver(el) {
    if (el.preventDefault) {
        el.preventDefault()
    }
    
    el.dataTransfer.dropEffect = 'move'
    
    return false
}

function handleDragEnter(el) {
    this.classList.add('over')
}

function handleDragLeave(el) {
    this.classList.remove('over')
}

function handleDrop(el) {
    if (el.stopPropagation) {
        el.stopPropagation()
    }
    
    if (dragSrcEl != this) {
        dragSrcEl.innerHTML = this.innerHTML
        this.innerHTML = el.dataTransfer.getData('text/html')
    }
    
    return false
}

function handleDragEnd(el) {
    this.style.opacity = '1';
    [].forEach.call(tableRows, function(tableRow) {
        tableRow.classList.remove('over')
    })
    console.log('calledDragent')
}

function startReorder(tableID) {
    tableRows = document.querySelectorAll(tableID)
    console.log(tableRows)
    
    for (var row = 1; row < tableRows.length; row++) {
        tableRows[row].draggable = 'true'
    }
    
    [].forEach.call(tableRows, function(tableRow) {
        tableRow.addEventListener('dragstart', handleDragStart, false)
        tableRow.addEventListener('dragenter', handleDragEnter, false)
        tableRow.addEventListener('dragover', handleDragOver, false)
        tableRow.addEventListener('dragleave', handleDragLeave, false)
        tableRow.addEventListener('drop', handleDrop, false)
        tableRow.addEventListener('dragend', handleDragEnd, false)
    })
}

function reorderTopics(el) {
    console.log(el.attributes['name'].value)
    if (el.attributes['name'].value == 'notReordering') {
        el.class = 'redTeacherButton'
        el.style.backgroundColor = '#dd514c'
        el.style.color = 'white'
        el.innerHTML = 'Finish Reorder'
        el.attributes['name'].value = 'reordering'
        startReorder('#topicList tr')
    } else {
        finishReorder('#topicList tr')
        el.attributes['name'].value = 'notReordering'
        reorderTopicsInCourse(tableRows)
    }
}

function reorderTaskGroups(el) {
    console.log('called')
    if (el.attributes['name'].value == 'notReordering') {
        el.class = 'redTeacherButton'
        el.style.backgroundColor = '#dd514c'
        el.style.color = 'white'
        el.innerHTML = 'Finish Reorder'
        el.attributes['name'].value = 'reordering'
        startReorder('#taskGroupList tr')
    } else {
        finishReorder('#taskGroupList tr')
        el.attributes['name'].value = 'notReordering'
        reorderTaskGroupsInTopic(tableRows)
    }
}

function reorderTasks(el, ID) {
    console.log('called')
    if (el.attributes['name'].value == 'notReordering') {
        el.class = 'redTeacherButton'
        el.style.backgroundColor = '#dd514c'
        el.style.color = 'white'
        el.innerHTML = 'Finish Reorder'
        el.attributes['name'].value = 'reordering'
        startReorder('#taskGroup' + ID + ' tr')
    } else {
        finishReorder('#taskGroup' + ID + ' tr')
        el.attributes['name'].value = 'notReordering'
        reorderTasksInTaskGroup(tableRows, ID)
    }
}

function finishReorder(tableID) {
    tableRows = document.querySelectorAll(tableID)
    console.log(tableRows)
    
    for (var row = 1; row < tableRows.length; row++) {
        tableRows[row].draggable = 'false'
    }
    
    [].forEach.call(tableRows, function(tableRow) {
        tableRow.removeEventListener('dragstart', handleDragStart, false)
        tableRow.removeEventListener('dragenter', handleDragEnter, false)
        tableRow.removeEventListener('dragover', handleDragOver, false)
        tableRow.removeEventListener('dragleave', handleDragLeave, false)
        tableRow.removeEventListener('drop', handleDrop, false)
        tableRow.removeEventListener('dragend', handleDragEnd, false)
    })
}

function reorderTaskGroupsInTopic(trList) {
    var t = getCurrentTopic()
    var newTopicTaskGroupList = []
    console.log(trList)
    for (var row = 1; row < trList.length; row++) {
        var name = trList[row].childNodes[0].innerHTML
        console.log(name)
        var index = getIndexOfTaskGroupInTopic(t, name)
        newTopicTaskGroupList.push(topics[t].taskgroups[index])
    }
    topics[t].taskgroups = newTopicTaskGroupList
    console.log(topics[t])
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageTopic.html'
}

function reorderTopicsInCourse(trList) {
    var c = getCurrentCourse()
    console.log(trList)
    var newCourseTopicList = []
    
    for (var row = 1; row < trList.length; row++) {
        var name = trList[row].childNodes[0].innerHTML
        var index = getIndexOfTopicInCourseByCovername(c, name)
        console.log(name)
        console.log(index)
        newCourseTopicList.push(courses[c].topics[index])
    }
    console.log(newCourseTopicList)
    courses[c].topics = newCourseTopicList
    localStorage.setItem('courses', JSON.stringify(courses))
    window.location.href = 'manageCourse.html'
}

function reorderTasksInTaskGroup(trList, tg) {
    var t = getCurrentTopic()
    var newTaskGroupTaskList = []
    console.log(t, tg)
    for (var row = 1; row < trList.length; row++) {
        var name = trList[row].childNodes[0].childNodes[0].innerHTML
        var index = getIndexOfTaskInTaskGroup(t, tg, name)
        newTaskGroupTaskList.push(topics[t].taskgroups[tg].tasks[index])
    }
    
    topics[t].taskgroups[tg].tasks = newTaskGroupTaskList
    console.log(topics[t].taskgroups[tg])
    localStorage.setItem('topics', JSON.stringify(topics))
    window.location.href = 'manageTopic.html'
}
