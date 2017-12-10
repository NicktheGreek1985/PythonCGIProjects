Student = function(firstname, lastname, username, password) {
    this.id = username;
    this.password = password;
    this.studentcourses = [];
    this.firstname = firstname
    this.lastname = lastname
}

Teacher = function(username, password, name) {
    this.username = username;
    this.password = password;
    this.name = name;
    this.classRefs = [];
    this.studentRefs = [];
    this.addClass = function(index) {
        this.classRefs.push(index);
        this.studentRefs.push([])
    };
}

StudentCourse = function(ref) {
    this.courseRef = ref
    this.progressUnmarked = 0
    this.progressCorrect = 0
    this.progressIncorrect = 0
    this.average = 0
    this.submissions = []
}

Submission = function(unitRef, moduleRef, activityRef, href) {
    this.unit = unitRef
    this.module = moduleRef
    this.activity = activityRef
    this.href = href
    this.state = 'unmarked'
    this.comment = ''
    this.isObsolete = false
}

Course = function(name) {
    this.name = name;
    this.units = [];
    this.totalNumberOfActivities = 0
    this.description = ''
    this.files = []
    this.links = []
}

Class = function(name, teacher, courseRef) {
    this.name = name
    this.teacher = teacher
    this.courseRef = courseRef
    this.currentHomework = ''
}

Unit = function(name) {
    this.name = name;
    this.modules = [];
    this.totalNumberOfActivities = 0
}

Module = function(name){
    this.name = name;
    this.activities = [];
}

Activity = function(name, difficulty) {
    this.name = name;
    this.content = "";
    this.attachments = [];
    this.difficulty = difficulty;
    this.hint = ""
    this.solution = ""
    this.canShowSolution = false
}

var users, teachers, courses, classes;
var cTI, cSI, cCI, cCLI, c_unit, c_module;
var currentContentPosition = null;// Used for editing content only
var canSubmit = false // Used for students submit activities

function loginPrep(courses, teachers, users, classes) {
    localStorage.setItem('teachers', teachers)
    localStorage.setItem('users', users)
    localStorage.setItem('classes', classes)
    localStorage.setItem('courses', courses)
    prep()
    setupLoginPage()
}

function prep() {
    try { document.getElementsByClassName('footer')[0].innerHTML = 'Gallifrey 2.5.2<br>Developed By <a href="mailto:nick.p@iinet.net.au">Nick Patrikeos</a>. Inspired by <a href="http://arcadia.ccgs.wa.edu.au/">Arcadia</a> developed by Thomas Drake-Brockman.' } catch (err) {}
    canSubmit = JSON.parse(localStorage.getItem('canSubmit'))
    teachers = JSON.parse(localStorage.getItem('teachers'))
    users = JSON.parse(localStorage.getItem('users'))
    classes = JSON.parse(localStorage.getItem('classes'))
    courses = JSON.parse(localStorage.getItem('courses'))
    
    if (users === null) {
        users = []//[new Student('1234', 'a'), new Student('1235', 'b')]
        localStorage.setItem('users', JSON.stringify(users))
    }
    if (teachers === null) {
        teachers = [new Teacher('NicktheGreek1985', 'abc', 'Nick Patrikeos')]
        localStorage.setItem('teachers', JSON.stringify(teachers))
    }
    
    
    if (courses === null) {
        courses = []
        //console.log(teachers)
        //var c = new Course('Year 10 Computer Science', teachers[0].name)
        //var d = new Course('Mobile App Development', teachers[0].name)
        //courses.push(c)
        //courses.push(d)
        //console.log(courses)
        localStorage.setItem('courses', JSON.stringify(courses))
    }
    if (classes === null) {
        classes = []
        //var a = new Class('10CSC1', 'Nick Patrikeos', 0)
        //var b = new Class('09MADA1', 'Nick Patrikeos', 1)
        //classes.push(a)
        //classes.push(b)
        //localStorage.setItem('teachers', JSON.stringify(teachers))
        localStorage.setItem('classes', JSON.stringify(classes))
    }
    
    cCLI = JSON.parse(localStorage.getItem('currentClass'))
    cTI = JSON.parse(localStorage.getItem('currentTeacher'))
    cSI = JSON.parse(localStorage.getItem('currentStudent'))
    cCI = JSON.parse(localStorage.getItem('currentCourse'))
    c_unit = JSON.parse(localStorage.getItem('currentUnit'))
    console.log(c_unit)
    c_module = JSON.parse(localStorage.getItem('currentModule'))
    
    if (window.location.href == 'http://tartarus.ccgs.wa.edu.au/~1019912/Gallifrey%20Beta%20Development/courseManage.html' || window.location.href == 'http://tartarus.ccgs.wa.edu.au/~1019912/Gallifrey%20Beta%20Development/unitManage.html' || window.location.href == 'http://tartarus.ccgs.wa.edu.au/~1019912/Gallifrey%20Beta%20Development/moduleManage.html' ) {
        cTI = teacherIndex(teachers, classes[cCLI].teacher)
    }
    console.log('Prepared ... hopefully')
}

function setupLoginPage() {
    prep()
    localStorage.setItem('currentCourse', null)
    localStorage.setItem('currentTeacher', null)
    localStorage.setItem('currentStudent', null)
    localStorage.setItem('currentClass', null)
    localStorage.setItem('canSubmit', false)
    document.getElementById('go').style.display = 'none'
}

function login() {
    var username = document.login_form.username.value
    var password = document.login_form.pass.value
    for (var i = 0; i < users.length; i++) {
        if (users[i].id == username) {
            if (users[i].password == password) {
                // Display Button to login and set current student
                localStorage.setItem('currentStudent', JSON.stringify(i))
                document.getElementById('go').style.display = 'block'
                document.getElementById('go_link').href = 'student.html'
                return
            }
        }
    }
    for (var j = 0; j < teachers.length; j++) {
        if (teachers[j].username == username) {
            if (teachers[j].password == password) {
                // Display Button to login and set current teacher
                localStorage.setItem('currentTeacher', JSON.stringify(j))
                document.getElementById('go').style.display = 'block'
                document.getElementById('go_link').href = 'teacher.html'
                return
            }
        }
    }
    alert('Your username or password was incorrect.')
}

function setupTeacherDashboard() {
    prep()
    localStorage.setItem('currentCourse', null);
    document.getElementById('welcome_message').innerHTML = 'Welcome to Gallifrey, ' + teachers[cTI].name
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    if (teachers[cTI].classRefs.length !== 0) {
        for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
            try {
                document.getElementById('course_container').innerHTML += "<div class='course_box' style='width: 45%'>" + classes[teachers[cTI].classRefs[i]].name + '<br><div class="viewcoursebtn"><a href="coursehomepageedit.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(classes[teachers[cTI].classRefs[i]].courseRef) + ')">Homepage</a></div><div class="viewcoursebtn"><a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')">Manage</a></div><div class="viewcoursebtn"><a href="courseEdit.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(classes[teachers[cTI].classRefs[i]].courseRef) + ')">Edit</a></div></div>'
                document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
                for (var student = 0; student < teachers[cTI].studentRefs[i].length; student++) {
                    var g = comparativeIndex(users[teachers[cTI].studentRefs[i][student]].studentcourses, teachers[cTI].classRefs[i])
                    for (var sub = 0; sub < users[teachers[cTI].studentRefs[i][student]].studentcourses[g].submissions.length; sub++) {
                        var subm = users[teachers[cTI].studentRefs[i][student]].studentcourses[g].submissions[sub]
                        if (subm.state == 'unmarked') {
                            console.log(subm.activity)
                            document.getElementById('rsubmissions').innerHTML += '<tr><td>' + users[teachers[cTI].studentRefs[i][student]].firstname + ' ' + users[teachers[cTI].studentRefs[i][student]].lastname + '</td><td>' + courses[classes[users[teachers[cTI].studentRefs[i][student]].studentcourses[g].courseRef].courseRef].units[subm.unit].modules[subm.module].activities[subm.activity].name + '</td></tr>'
                            console.log(document.getElementById('rsubmissions').innerHTML)
                            console.log('abrd')
                        }
                    }
                }
            } catch(err) {}
        }
    } else {
        document.getElementById('course_container').innerHTML = 'No Classes'
    }
    setupLogoutForm()
}

function courseIndex(lst, value) {
    for (var x = 0; x < lst.length; x++) {
        if (lst[x].name == value) {
            return x
        }
    }
}

function setupCourseEditPage() {
    prep()
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        try {
            document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
        } catch(err) {}
    }
    document.getElementById('coursename').innerHTML = courses[cCI].name;
    for (var i = 0; i < courses[cCI].units.length; i++) {
        document.getElementById('tab_holder').innerHTML += '<div class="tab" onclick="showUnitInEdit(this,'+ i +')"><h4>' + courses[cCI].units[i].name + '</h4></div>'
    }
    var fstr = ''
    for (var x = 0; x < courses.length; x++) {
        for (var y = 0; y < courses[x].units.length; y++) {
            fstr += '<option value="' + JSON.stringify([x, y]) + '">' + courses[x].units[y].name + '</option>'
        }
    }
    document.getElementById('existingUnitChoice').innerHTML = fstr
    console.log(document.getElementById('existingUnitChoice'))
    for (var x = 0; x < courses.length; x++) {
        for (var y = 0; y < courses[x].units.length; y++) {
            for (var z = 0; z < courses[x].units[y].modules.length; z++) {
                document.getElementById('existingModuleChoice').innerHTML += '<option value="' + JSON.stringify([x, y, z]) + '">' + courses[x].units[y].modules[z].name + '</option>'
            }
        }
    }
    setupLogoutForm()
}

function showContent(i, j, k) {
    document.edit_activity_form.content.value = courses[cCI].units[i].modules[j].activities[k].content
    document.edit_activity_form.activityname.value = courses[cCI].units[i].modules[j].activities[k].name
    document.edit_activity_form.hint.value = courses[cCI].units[i].modules[j].activities[k].hint
    document.edit_activity_form.solution.value = courses[cCI].units[i].modules[j].activities[k].solution
    document.getElementById('difficulty_edit').value = courses[cCI].units[i].modules[j].activities[k].difficulty
    document.edit_activity_form.show_solution.checked = courses[cCI].units[i].modules[j].activities[k].canShowSolution
    document.add_file_form.unit.value = courses[cCI].units[i].name
    document.add_file_form.module.value = courses[cCI].units[i].modules[j].name
    document.add_file_form.activity.value = courses[cCI].units[i].modules[j].activities[k].name
    document.new_activity_form.unit.value = courses[cCI].units[i].name
    document.new_activity_form.module.value = courses[cCI].units[i].modules[j].name
    document.new_module_form.unit.value = courses[cCI].units[i].name
    document.existing_module_form.unit.value = courses[cCI].units[i].name
    console.log([i,j,k])
    currentContentPosition = [i, j, k]
}

function changeContent() {
    courses[cCI].units[currentContentPosition[0]].modules[currentContentPosition[1]].activities[currentContentPosition[2]].content = document.edit_activity_form.content.value
    courses[cCI].units[currentContentPosition[0]].modules[currentContentPosition[1]].activities[currentContentPosition[2]].name = document.edit_activity_form.activityname.value
    courses[cCI].units[currentContentPosition[0]].modules[currentContentPosition[1]].activities[currentContentPosition[2]].hint = document.edit_activity_form.hint.value
    courses[cCI].units[currentContentPosition[0]].modules[currentContentPosition[1]].activities[currentContentPosition[2]].solution = document.edit_activity_form.solution.value
    courses[cCI].units[currentContentPosition[0]].modules[currentContentPosition[1]].activities[currentContentPosition[2]].difficulty = document.getElementById('difficulty_edit').value
    courses[cCI].units[currentContentPosition[0]].modules[currentContentPosition[1]].activities[currentContentPosition[2]].canShowSolution = document.edit_activity_form.show_solution.checked
    localStorage.setItem('courses', JSON.stringify(courses))
    setupLogoutForm()
    window.location.href = 'courseEdit.html'
}

function addUnit() {
    courses[cCI].units.push(new Unit(document.new_unit_form.unit.value))
    localStorage.setItem('courses', JSON.stringify(courses))
    setupLogoutForm()
    window.location.href = 'courseEdit.html'
}

function addExistingUnit() {
    var pos = JSON.parse(document.getElementById('existingModuleChoice').value)
    courses[cCI].units.push(courses[pos[0]].units[pos[1]])
    localStorage.setItem('courses', JSON.stringify(courses))
    setupLogoutForm()
    window.location.href = 'courseEdit.html'
}

function addModule() {
    courses[cCI].units[courseIndex(courses[cCI].units, document.new_module_form.unit.value)].modules.push(new Module(document.new_module_form.module.value))
    localStorage.setItem('courses', JSON.stringify(courses))
    setupLogoutForm()
    window.location.href = 'courseEdit.html'
}

function addExistingModule() {
    var pos = JSON.parse(document.getElementById('existingModuleChoice').value)
    courses[cCI].units[courseIndex(courses[cCI].units, document.existing_module_form.unit.value)].modules.push(courses[pos[0]].units[pos[1]].modules[pos[2]])
    localStorage.setItem('courses', JSON.stringify(courses))
    setupLogoutForm()
    window.location.href = 'courseEdit.html'
}

function addActivity() {
    var i = courseIndex(courses[cCI].units, document.new_activity_form.unit.value)
    var j = courseIndex(courses[cCI].units[i].modules, document.new_activity_form.module.value)
    courses[cCI].units[i].modules[j].activities.push(new Activity(document.new_activity_form.activity.value, document.getElementById('difficulty').value))
    console.log(courses)
    courses[cCI].totalNumberOfActivities += 1
    courses[cCI].units[i].totalNumberOfActivities += 1
    localStorage.setItem('courses', JSON.stringify(courses))
    setupLogoutForm()
    window.location.href = 'courseEdit.html'
}

function setupCourseViewPage() {
    prep()
    localStorage.setItem('currentClass', null)
    localStorage.setItem('canSubmit', false)
    for (var i = 0; i < classes.length; i++) {
        document.getElementById('view_body').innerHTML += '<div class="course_view" style="width: 100%"><span>' + classes[i].name + '</span> with ' + classes[i].teacher + '<div class="viewcoursebtn"><a href="coursePage.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(classes[i].courseRef) + ')">View Course</a></div></div>';
    }
    console.log(document.getElementById('view_body').innerHTML)
    setupLogoutForm()
}

function setupCourseViewTeacherPage() {
    prep()
    localStorage.setItem('currentClass', null)
    localStorage.setItem('canSubmit', false)
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
    }
    for (var i = 0; i < courses.length; i++) {
        document.getElementById('course_list').innerHTML += '<div class="course_view" style="width: 100%"><span>' + courses[i].name + '</span><div class="viewcoursebtn"><a href="courseEdit.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(i) + ')">Edit</a></div><div class="viewcoursebtn" name="extbtn"><a href="coursePage.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(i) + ')">View Course (Read-Only)</a></div></div>';
    }
    setupLogoutForm()
}

function setupClassViewPage() {
    prep()
    localStorage.setItem('currentClass', null)
    localStorage.setItem('canSubmit', false)
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
    }
    for (var i = 0; i < classes.length; i++) {
        document.getElementById('class_list').innerHTML += '<div class="course_view" style="width: 100%"><span>' + classes[i].name + '</span> with ' + classes[i].teacher + '<div class="viewcoursebtn"><a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + JSON.stringify(i) + ')">Manage</a></div></div>';
    }
    console.log(document.getElementById('view_body').innerHTML)
    setupLogoutForm()
}

function setupUserViewPage() {
    prep()
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
    }
    for (var i = 0; i < users.length; i++) {
        document.getElementById('students').innerHTML += '<tr><td>'+ users[i].firstname + ' ' + users[i].lastname + ' ('+ users[i].id + ') </td><td>' + getStudentClassNames(users[i].studentcourses) + '</td>'
    }
    for (var j = 0; j < teachers.length; j++) {
        document.getElementById('teachers').innerHTML += '<tr><td>' + teachers[j].name + '</td><td>' + teachers[j].username + '</td><td>' + getTeacherClassNames(teachers[j].classRefs) + '</td>'
    }
    setupLogoutForm()
}

function getStudentClassNames(lst) {
    var f = []
    for (var i = 0; i < lst.length; i++) {
        f.push(classes[lst[i].courseRef].name)
    }
    return f.join(', ')
}

function getTeacherClassNames(lst) {
    var f = []
    for (var i = 0; i < lst.length; i++) {
        f.push(classes[lst[i]].name)
    }
    return f.join(', ')
}

function setupCoursePage() {
    prep()
    document.getElementById('coursename').innerHTML = courses[cCI].name
    if (cSI !== null) {
        for (var i = 0; i < users[cSI].studentcourses.length; i++) {
            document.getElementsByClassName('navbar')[0].innerHTML += '<a href="coursePage.html" onclick="localStorage.setItem(\'currentClass\',' + JSON.stringify(users[cSI].studentcourses[i].courseRef) + ')"><h4>' + classes[users[cSI].studentcourses[i].courseRef].name + '</h4></a>'
        }
    }
    if (canSubmit) {
        var i = comparativeIndex(users[cSI].studentcourses, courses[cCI])
        // document.getElementById('unit_prog_container').innerHTML = '<div class="dash_enc" style="margin-bottom: 20px;"><div class="progress_dash" style="width: ' + JSON.stringify(users[cSI].studentcourses[i].progressUnmarked) + '%;"></div><div class="correct_dash" style="width: ' + JSON.stringify(users[cSI].studentcourses[i].progressCorrect) + '%;"></div><div class="incorrect_dash" style="width: ' + JSON.stringify(users[cSI].studentcourses[i].progressIncorrect) + '%;"></div>'
        for (var x = 0; x < courses[cCI].units.length; x++) {
            var cmp = unitCompletionPercentage(users[cSI].studentcourses[referenceIndex3(users[cSI].studentcourses, courses[cCI].name)].submissions, x)
            console.log(cmp)
            var width = (1 / courses[cCI].units.length) * 100 - 5
            document.getElementById('unit_prog_container').innerHTML += '<div class="unit_prog" style="width: ' + width + '%">' + courses[cCI].units[x].name + '<br><div class="dash_enc"><div class="progress_dash" style="width: ' + JSON.stringify(cmp[0]) + '%"></div><div class="correct_dash" style="width: ' + JSON.stringify(cmp[1]) + '%"></div><div class="incorrect_dash" style="width: '+ JSON.stringify(cmp[2]) + '%"></div><div style="width: ' + JSON.stringify(cmp[3]) + '"></div></div></div>'
        }
    }
    console.log(document.getElementById('unit_prog_container').innerHTML)
    for (var i = 0; i < courses[cCI].units.length; i++) {
        document.getElementById('tab_holder').innerHTML += '<div class="tab" onclick="showUnit(this,'+ i +')"><h4>' + courses[cCI].units[i].name + '</h4></div>'
    }
    setupLogoutForm()
}

function showUnit(element, pos) {
    element.style.borderTop = '1px solid lightgray'
    element.style.borderLeft = '1px solid lightgray'
    element.style.borderRight = '1px solid lightgray'
    element.style.borderBottom = '1px solid white'
    var fstr = '<ul class="shown_modules">'
    for (var module = 0; module < courses[cCI].units[pos].modules.length; module++) {
        var sstr = '<ul class="acvm">'
        for (var ac = 0; ac < courses[cCI].units[pos].modules[module].activities.length; ac++) {
            if (canSubmit) {
                sstr += '<li style="list-style-image: url(\'' + courses[cCI].units[pos].modules[module].activities[ac].difficulty + '.png\')" onclick="showActivity('+pos+','+module+','+ac+')" onmouseover="underline(this)" onmouseout="deunderline(this)">' + courses[cCI].units[pos].modules[module].activities[ac].name + '<img src="'+ imgForActivity(users[cSI].studentcourses[referenceIndex3(users[cSI].studentcourses, courses[cCI].name)].submissions, pos, module, ac) +'" /></li>'
            } else {
                sstr += '<li style="list-style-image: url(\'' + courses[cCI].units[pos].modules[module].activities[ac].difficulty + '.png\')" onclick="showActivity('+pos+','+module+','+ac+')" onmouseover="underline(this)" onmouseout="deunderline(this)">' + courses[cCI].units[pos].modules[module].activities[ac].name + '</li>'
            }
        }
        sstr += '</ul>'
        fstr += '<li onclick="displayModule(this)">' +'<p onmouseover="underline(this)" onmouseout="deunderline(this)">'+ courses[cCI].units[pos].modules[module].name +'</p>'+ sstr + '</li>'
    }
    fstr += '</ul>'
    document.getElementById('module_box').innerHTML = '' 
    document.getElementById('module_box').innerHTML += fstr
}

function showUnitInEdit(element, pos) {
    element.style.borderTop = '1px solid lightgray'
    element.style.borderLeft = '1px solid lightgray'
    element.style.borderRight = '1px solid lightgray'
    element.style.borderBottom = '1px solid white'
    var fstr = '<ul class="shown_modules">'
    for (var module = 0; module < courses[cCI].units[pos].modules.length; module++) {
        var sstr = '<ul class="acvm">'
        for (var ac = 0; ac < courses[cCI].units[pos].modules[module].activities.length; ac++) {
            if (canSubmit) {
                sstr += '<li style="list-style-image: url(\'' + courses[cCI].units[pos].modules[module].activities[ac].difficulty + '.png\')" onclick="showActivity('+pos+','+module+','+ac+'); showContent('+pos+','+module+','+ac+')" onmouseover="underline(this)" onmouseout="deunderline(this)">' + courses[cCI].units[pos].modules[module].activities[ac].name + '<img src="'+ imgForActivity(users[cSI].studentcourses[comparativeIndex(users[cSI].studentcourses, cCI)].submissions, pos, module, ac) +'" /></li>'
            } else {
                sstr += '<li style="list-style-image: url(\'' + courses[cCI].units[pos].modules[module].activities[ac].difficulty + '.png\')" onclick="showActivity('+pos+','+module+','+ac+'); showContent('+pos+','+module+','+ac+')" onmouseover="underline(this)" onmouseout="deunderline(this)">' + courses[cCI].units[pos].modules[module].activities[ac].name + '</li>'
            }
        }
        sstr += '</ul>'
        fstr += '<li onclick="displayModule(this)">' +'<p onmouseover="underline(this)" onmouseout="deunderline(this)">'+ courses[cCI].units[pos].modules[module].name +'</p>'+ sstr + '</li>'
    }
    fstr += '</ul>'
    document.getElementById('module_box').innerHTML = '' 
    document.getElementById('module_box').innerHTML += fstr
}

function displayModule(element) {
    var elements = element.childNodes
    console.log(elements)
    for (var j = 0; j < elements[1].childNodes.length; j++) {
        console.log(elements[1].childNodes[j])
        elements[1].childNodes[j].style.display = 'list-item'
    }
}

function imgForActivity(submissions, i, j, k) {
    var subs = findSubmissions2(submissions, i, j, k)
    if (subs.length == 0) {
        return 'diamond.png'
    }
    if (submissions[subs[subs.length - 1]].state == 'unmarked') {
        return 'dot.png'
    } else if (submissions[subs[subs.length - 1]].state == 'correct') {
        return 'tick.png'
    } else if (submissions[subs[subs.length -1]].state == 'incorrect') {
        return 'cross.png'
    }
}

function underline(element) {
    element.style.textDecoration = 'underline';
}

function deunderline(element) {
    element.style.textDecoration = 'none'
}

function showActivity(unitPos, modulePos, activityPos) {
    document.getElementById('content_title').innerHTML = courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].name
    document.getElementById('content_box').innerHTML = courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].content
    if (courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].hint !== '') {
        var nstr = '<div id="hint_show" onclick="showHint(\'' + courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].hint + '\')">Show Hint</div>'
        console.log(nstr)
        document.getElementById('content_box').innerHTML += nstr
    }
    if (courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].canShowSolution) {
        var nstr = '<div id="solution_show" onclick="showSolution(\'' + courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].solution + '\')">Show Solution</div>'
        console.log(nstr)
        document.getElementById('content_box').innerHTML += nstr
    }
    if (courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].attachments.length !== 0) {
        var fstr = '<div class="attachments_section"><h4>Attachments</h4><br>'
        for (var i = 0; i < courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].attachments.length; i++) {
            fstr += '<p>' + courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].attachments[i].split('.')[0] + '</p> <a href="Attachments/' + courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].attachments[i]  + '">Download</a><br>'
        }
        document.getElementById('content_box').innerHTML += fstr + '</div>'
    } else {}
    if (canSubmit) {
        var submitForm = '<h4>Submit Your Solution</h3>\
    <hr><p>Files</p>\
    <form name="submit_activity_form" action="submit.py" method="POST" enctype="multipart/form-data">\
        <input type="file" name="file_1"/>\
        File Name:<input type="text" name="filename" />\
        <input type="text" name="unit" style="display: none" value="' + courses[cCI].units[unitPos].name +'"/>\
        <input type="text" name="module" style="display: none" value="' + courses[cCI].units[unitPos].modules[modulePos].name +'"/>\
        <input type="text" name="activity" style="display: none" value="' + courses[cCI].units[unitPos].modules[modulePos].activities[activityPos].name +'"/>\
        <input type="text" name="courseref" style="display: none" value="' + referenceIndex3(users[cSI].studentcourses, courses[cCI].name) +'"/>\
        <input type="submit" value="Submit" />\
    </form>'
        document.getElementById('content_box').innerHTML += submitForm + '</div>'
        var cmp = referenceIndex3(users[cSI].studentcourses, courses[cCI].name)
        var subs = findSubmissions(users[cSI], cmp, unitPos, modulePos, activityPos)
        if (subs.length > 0) {
          var fstr = '<h4>Submissions</h4><hr>'
          for (var a = 0; a < subs.length; a++) {
              var substate;
              if (users[cSI].studentcourses[cmp].submissions[subs[a]].state == 'unmarked') {
                  substate = 'orange'
              } else if (users[cSI].studentcourses[cmp].submissions[subs[a]].state == 'correct') {
                  substate = 'green'
              } else if (users[cSI].studentcourses[cmp].submissions[subs[a]].state == 'incorrect') {
                  substate = 'red'
              } 
              console.log(users[cSI].studentcourses[cmp].submissions[subs[a]].state)
              console.log(substate)
              var mdiv = '<div class="submission_show" style="border: 1px solid ' + substate +'"><a href="Submissions/' + users[cSI].studentcourses[cmp].submissions[subs[a]].href + '">Download File</a><p class="state_show">' + users[cSI].studentcourses[cmp].submissions[subs[a]].state + '</p><br>' + users[cSI].studentcourses[cmp].submissions[subs[a]].comment + '</div>'
              fstr += mdiv 
          }
          document.getElementById('content_box').innerHTML += fstr
        }
    }
}

function showHint(hint) {
    document.getElementById('hint_show').style.width = "100%"
    document.getElementById('hint_show').style.textAlign = "left"
    document.getElementById('hint_show').innerHTML = '<h4>Hint</h4>' + hint
}

function showSolution(solution) {
    document.getElementById('solution_show').style.width = "100%"
    document.getElementById('solution_show').style.textAlign = "left"
    document.getElementById('solution_show').innerHTML = '<h4>Solution</h4>' + solution
}

function showModule(element) {
    element.style.display = 'block'
}

function changeActivityAttachment(unit, module, activity, href) {
    prep()
    var i = courseIndex(courses[cCI].units, unit)
    var j = courseIndex(courses[cCI].units[i].modules,module)
    var k = courseIndex(courses[cCI].units[i].modules[j].activities,activity)
    courses[cCI].units[i].modules[j].activities[k].attachments.push(href)
    localStorage.setItem('courses', JSON.stringify(courses))
    window.location.href = 'courseEdit.html'
}

function referenceIndex(lst, val) {
    for (var i = 0; i < lst.length; i++) {
        if (courses[lst[i]].name == val) {
            return i
        }
    }
}

function referenceIndex2(lst, val) {
    for (var i = 0; i < lst.length; i++) {
        if (classes[lst[i]].name == val) {
            return i
        }
    }
}

function referenceIndex3(lst, val) {
    for (var i = 0; i < lst.length; i++) {
        if (courses[classes[lst[i].courseRef].courseRef].name == val) {
            return i
        }
    }
}

function studentReferenceIndex(lst, val) {
    for (var i = 0; i < lst.length; i++) {
        if (courses[lst[i].courseRef].name == val) {
            return i
        }
    }
}

function studentIndex(lst, value) {
    for (var x = 0; x < lst.length; x++) {
        if (lst[x].id == value) {
            return x
        }
    }
}

function setupCourseManagementPage() {
    prep()
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
    }
    document.getElementById('coursename').innerHTML = classes[cCLI].name;
    var fstr = '<td></td>'
    var cc = referenceIndex2(teachers[cTI].classRefs, classes[cCLI].name)

    for (var x = 0; x < courses[classes[cCLI].courseRef].units.length; x++) {
        fstr += '<td><a href="unitManage.html" onclick="localStorage.setItem(\'currentUnit\', ' + JSON.stringify(x) + ')">' + courses[classes[cCLI].courseRef].units[x].name + '</a></td>'
    }
    
    document.getElementById('class_table').innerHTML += '<tr>' + fstr + '</tr>'
    console.log(cTI)
    for (var c = 0; c < teachers[cTI].studentRefs[cc].length; c++) {
        console.log('ahr')
        var nstr = '<tr><td>' + users[teachers[cTI].studentRefs[cc][c]].firstname + ' ' + users[teachers[cTI].studentRefs[cc][c]].lastname + '</td>'
        for (var x = 0; x < courses[classes[teachers[cTI].classRefs[cc]].courseRef].units.length; x++) {
            // var cmp = unitCompletionPercentage(users[cSI].studentcourses[comparativeIndex(users[cSI].studentcourses, cCI)].submissions, x)
            console.log(users[teachers[cTI].studentRefs[cc][c]].studentcourses[comparativeIndex(users[teachers[cTI].studentRefs[cc][c]].studentcourses, cCLI)])
            var cmp = unitCompletionPercentage(users[teachers[cTI].studentRefs[cc][c]].studentcourses[comparativeIndex(users[teachers[cTI].studentRefs[cc][c]].studentcourses, cCLI)].submissions, x)
            console.log(cmp)
            var width = (1 / courses[classes[cCLI].courseRef].units.length) * 100 - 5
            nstr += '<td><div class="dash_enc"><div class="progress_dash" style="width: ' + JSON.stringify(cmp[0]) + '%"></div><div class="correct_dash" style="width: ' + JSON.stringify(cmp[1]) + '%"></div><div class="incorrect_dash" style="width: '+ JSON.stringify(cmp[2]) + '%"></div><div style="width: ' + JSON.stringify(cmp[3]) + '"></div></div></td>'
        }
        document.getElementById('class_table').innerHTML += nstr + '</td>'
    }
    document.homework_form.homework.value = classes[cCLI].currentHomework
    setupLogoutForm()
}

function setHomework() {
    classes[cCLI].currentHomework = document.homework_form.homework.value
    localStorage.setItem('classes', JSON.stringify(classes))
    setupLogoutForm()
    window.location.href = 'courseManage.html'
}

function setupUnitManagementPage() {
    prep()
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
    }
    
    document.getElementById('coursename').innerHTML = classes[cCLI].name;
    document.getElementById('unitname').innerHTML = courses[classes[cCLI].courseRef].units[c_unit].name
    var fstr = '<td></td>'
    var cc = referenceIndex2(teachers[cTI].classRefs, classes[cCLI].name)
    console.log(cc)
    for (var x = 0; x < courses[classes[cCLI].courseRef].units[c_unit].modules.length; x++) {
        fstr += '<td><a href="moduleManage.html" onclick="localStorage.setItem(\'currentModule\', ' + JSON.stringify(x) + ')">' + courses[classes[cCLI].courseRef].units[c_unit].modules[x].name + '</a></td>'
    }
    
    document.getElementById('module_table').innerHTML += '<tr>' + fstr + '</tr>'
    for (var c = 0; c < teachers[cTI].studentRefs[cc].length; c++) {
        var nstr = '<tr><td>' + users[teachers[cTI].studentRefs[cc][c]].id + '</td>'
        for (var x = 0; x < courses[classes[teachers[cTI].classRefs[cc]].courseRef].units[c_unit].modules.length; x++) {
            // var cmp = unitCompletionPercentage(users[cSI].studentcourses[comparativeIndex(users[cSI].studentcourses, cCI)].submissions, x)
            var cmp = moduleCompletionPercentage(users[teachers[cTI].studentRefs[cc][c]].studentcourses[comparativeIndex(users[teachers[cTI].studentRefs[cc][c]].studentcourses, cCLI)].submissions, c_unit, x)
            console.log(cmp)
            var width = (1 / courses[classes[cCLI].courseRef].units[c_unit].modules.length) * 100 - 5
            nstr += '<td><div class="dash_enc"><div class="progress_dash" style="width: ' + JSON.stringify(cmp[0]) + '%"></div><div class="correct_dash" style="width: ' + JSON.stringify(cmp[1]) + '%"></div><div class="incorrect_dash" style="width: '+ JSON.stringify(cmp[2]) + '%"></div><div style="width: ' + JSON.stringify(cmp[3]) + '"></div></div></td>'
        }
        document.getElementById('module_table').innerHTML += nstr + '</td>'
    }
    setupLogoutForm()
}

function setupModuleManagementPage() {
    prep()
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
    }
    
    document.getElementById('coursename').innerHTML = classes[cCLI].name;
    document.getElementById('unitname').innerHTML = courses[classes[cCLI].courseRef].units[c_unit].name
    document.getElementById('modulename').innerHTML = courses[classes[cCLI].courseRef].units[c_unit].modules[c_module].name
    var fstr = '<td></td>'
    var cc = referenceIndex2(teachers[cTI].classRefs, classes[cCLI].name)
    console.log()
    for (var x = 0; x < courses[classes[cCLI].courseRef].units[c_unit].modules[c_module].activities.length; x++) {
        fstr += '<td>' + courses[classes[cCLI].courseRef].units[c_unit].modules[c_module].activities[x].name + '</td>'
    }
    
    document.getElementById('module_table').innerHTML += '<tr>' + fstr + '</tr>'
    for (var c = 0; c < teachers[cTI].studentRefs[cc].length; c++) {
        var nstr = '<tr><td>' + users[teachers[cTI].studentRefs[cc][c]].id + '</td>'
        
        for (var x = 0; x < courses[classes[teachers[cTI].classRefs[cc]].courseRef].units[c_unit].modules[c_module].activities.length; x++) {
            var i = comparativeIndex(users[teachers[cTI].studentRefs[cc][c]].studentcourses, cCLI)
            var f = findSubmissions(users[teachers[cTI].studentRefs[cc][c]], i, c_unit, c_module, x)
            if (f.length > 0) {
                var substate;
                if (users[teachers[cTI].studentRefs[cc][c]].studentcourses[i].submissions[f[f.length - 1]].state  == 'unmarked') {
                    substate = 'rgb(45, 136, 205)'
                } else if (users[teachers[cTI].studentRefs[cc][c]].studentcourses[i].submissions[f[f.length - 1]].state  == 'correct') {
                    substate = 'rgb(1,194,96)'
                } else if (users[teachers[cTI].studentRefs[cc][c]].studentcourses[i].submissions[f[f.length - 1]].state  == 'incorrect') {
                    substate = 'rgb(240,57,60)'
                }
                nstr += '<td><a class="viewFile" style="background-color: ' + substate + ';" href="Submissions/' + users[teachers[cTI].studentRefs[cc][c]].studentcourses[i].submissions[f[f.length - 1]].href + '" download>View</a><button onclick="markCorrect('+JSON.stringify([cc, c, i, f[f.length - 1]])+')">Correct</button><button onclick="markIncorrect('+JSON.stringify([cc, c, i, f[f.length - 1]])+')">Incorrect</button></td>'
                console.log(nstr)
            } else {
                nstr += "<td></td>"
            }
        }
        document.getElementById('module_table').innerHTML += nstr + '</td>'
    }
    setupLogoutForm()
}


function markCorrect(p) {
    console.log(p)
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions[p[3]].state = 'correct'
    var comm = document.comment_form.comment.value
    if (comm !== null) {
        users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions[p[3]].comment = comm
    }
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].progressCorrect = (findNumberOfCorrectSubmissions(users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions) / courses[classes[cCLI].courseRef].totalNumberOfActivities) * 100
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].progressIncorrect = (findNumberOfIncorrectSubmissions(users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions) / courses[classes[cCLI].courseRef].totalNumberOfActivities) * 100
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].progressUnmarked = (findNumberOfUnmarkedSubmissions(users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions) / courses[classes[cCLI].courseRef].totalNumberOfActivities) * 100
    
    localStorage.setItem('users', JSON.stringify(users))
    setupLogoutForm()
    window.location.href = 'moduleManage.html'
}

function markIncorrect(p) {
    var comm = document.comment_form.comment.value
    if (comm !== null) {
        users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions[p[3]].comment = comm
    }
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions[p[3]].state = 'incorrect'
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].progressIncorrect = (findNumberOfIncorrectSubmissions(users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions) / courses[classes[cCLI].courseRef].totalNumberOfActivities) * 100
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].progressCorrect = (findNumberOfCorrectSubmissions(users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions) / courses[classes[cCLI].courseRef].totalNumberOfActivities) * 100
    users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].progressUnmarked = (findNumberOfUnmarkedSubmissions(users[teachers[cTI].studentRefs[p[0]][p[1]]].studentcourses[p[2]].submissions) / courses[classes[cCLI].courseRef].totalNumberOfActivities) * 100
    localStorage.setItem('users', JSON.stringify(users))
    setupLogoutForm()
    window.location.href = 'moduleManage.html'
}

function comparativeIndex(lst, n) {
    for (var x = 0; x < lst.length; x++) {
        if (n == lst[x].courseRef) {
            return x
        }
    }
}

function comparativeIndexForUnit(lst, n) {
    for (var x = 0; x < lst.length; x++) {
        if (n == lst[x].unitRef) {
            return x
        }
    }
}

function addStudentToClass() {
    var username = document.add_student_form.username.value
    var index = studentIndex(users, username)
    var cc = referenceIndex2(teachers[cTI].classRefs, classes[cCLI].name)
    console.log(cc)
    teachers[cTI].studentRefs[cc].push(index)
    users[index].studentcourses.push(new StudentCourse(cCLI))
    localStorage.setItem('users', JSON.stringify(users))
    localStorage.setItem('teachers', JSON.stringify(teachers))
    setupLogoutForm()
}

function addCourse() {
    courses.push(new Course(document.add_course_form.coursename.value))
    localStorage.setItem('courses', JSON.stringify(courses))
    setupLogoutForm()
    window.location.href = 'courseViewTeacher.html'
}

function addClass() {
    console.log(courseIndex(courses, document.add_class_form.course.value))
    classes.push(new Class(document.add_class_form.classname.value, teachers[cTI].name, courseIndex(courses, document.add_class_form.course.value)))
    console.log(classes)
    teachers[cTI].classRefs.push(classes.length-1)
    teachers[cTI].studentRefs.push([])
    localStorage.setItem('classes', JSON.stringify(classes))
    localStorage.setItem('teachers', JSON.stringify(teachers))
}

function setupStudentDashboard() {
    prep()
    localStorage.setItem('currentCourse', null);
    localStorage.setItem('canSubmit', true)
    if (users[cSI].studentcourses.length !== 0) {
        for (var i = 0; i < users[cSI].studentcourses.length; i++) {
            document.getElementsByClassName('navbar')[0].innerHTML += '<a href="coursePage.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(classes[users[cSI].studentcourses[i].courseRef].courseRef) + ')"><h4>' + classes[users[cSI].studentcourses[i].courseRef].name + '</h4></a>'
            var nstr= ''
            if (classes[users[cSI].studentcourses[i].courseRef].currentHomework !== "") {
                nstr = '<br>Homework: ' + classes[users[cSI].studentcourses[i].courseRef].currentHomework
            }
            cCI = classes[users[cSI].studentcourses[i].courseRef].courseRef
            console.log(cCI)
            var cmp = courseCompletionPercentage(users[cSI].studentcourses[i].submissions)
            document.getElementById('course_container').innerHTML += "<div class='course_box'><span>" + classes[users[cSI].studentcourses[i].courseRef].name + '</span> with ' + classes[users[cSI].studentcourses[i].courseRef].teacher +'<div class="viewcoursebtn"><a href="coursePage.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(classes[users[cSI].studentcourses[i].courseRef].courseRef) + ')">View Course</a></div><div class="viewcoursebtn"><a href="coursehomepage.html" onclick="localStorage.setItem(\'currentCourse\',' + JSON.stringify(classes[users[cSI].studentcourses[i].courseRef].courseRef) + ')">Homepage</a></div><br><div class="dash_enc"><div class="progress_dash" style="width: ' + JSON.stringify(cmp[0]) + '%;"></div><div class="correct_dash" style="width: ' + JSON.stringify(cmp[1]) + '%;"></div><div class="incorrect_dash" style="width: ' + JSON.stringify(cmp[2]) + '%;"></div></div>' + nstr+ '</div>'
            cCI = undefined    
        }
    } else {
        document.getElementById('course_container').innerHTML = 'No Classes'
    }
    setupLogoutForm()
}

function addNewStudent() {
    users.push(new Student(document.add_student_form.firstname.value, document.add_student_form.lastname.value, document.add_student_form.username.value, document.add_student_form.password.value))
    console.log(users)
    localStorage.setItem('users', JSON.stringify(users))
    window.location.href = 'userView.html'
}

function addNewTeacher() {
    teachers.push(new Teacher(document.add_teacher_form.username.value, document.add_teacher_form.password.value, document.add_teacher_form.name.value))
    localStorage.setItem('teachers', JSON.stringify(teachers))
    setupLogoutForm()
    window.location.href = 'userView.html'
}

function submitActivity(courseref, unit, module, activity, href) {
    prep()
    var i = courseIndex(courses[cCI].units, unit)
    var j = courseIndex(courses[cCI].units[i].modules,module)
    var k = courseIndex(courses[cCI].units[i].modules[j].activities,activity)
    var n = findSubmissions2(users[cSI].studentcourses[courseref].submissions, i, j, k)
    if (n.length > 0) {
        users[cSI].studentcourses[courseref].submissions[n[n.length - 1]].isObsolete = true
    }
    users[cSI].studentcourses[courseref].submissions.push(new Submission(i, j, k, href))
    console.log(courses[cCI].totalNumberOfActivities)
    console.log((users[cSI].studentcourses[courseref].submissions.length / courses[cCI].totalNumberOfActivities))
    users[cSI].studentcourses[courseref].progressUnmarked = (findNumberOfUnmarkedSubmissions(users[cSI].studentcourses[courseref].submissions) / courses[cCI].totalNumberOfActivities) * 100
    users[cSI].studentcourses[courseref].progressCorrect = (findNumberOfCorrectSubmissions(users[cSI].studentcourses[courseref].submissions) / courses[cCI].totalNumberOfActivities) * 100
    users[cSI].studentcourses[courseref].progressIncorrect = (findNumberOfIncorrectSubmissions(users[cSI].studentcourses[courseref].submissions) / courses[cCI].totalNumberOfActivities) * 100
    localStorage.setItem('users', JSON.stringify(users))
    
    window.location.href = 'coursePage.html'
}

function findSubmissions(student, c, i, j, k) {
    var subs = []
    console.log(c)
    for (var sub = 0; sub < student.studentcourses[c].submissions.length; sub++) {
        var p = student.studentcourses[c].submissions[sub]
        if (p.unit == i && p.module == j && p.activity == k) {
            subs.push(sub)
        }
    }
    return subs
}

function findSubmissions2(submissions, i, j, k) {
    var subs = []
    for (var sub = 0; sub < submissions.length; sub++) {
        var p = submissions[sub]
        if (p.unit == i && p.module == j && p.activity == k) {
            subs.push(sub)
        }
    }
    return subs
}

function findNumberOfUnmarkedSubmissions(submissions) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'unmarked' && !submissions[i].isObsolete) {
            t += 1
        }
    }
    return t
}

function findNumberOfCorrectSubmissions(submissions) {
    console.log(submissions)
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'correct'  && !submissions[i].isObsolete) {
            t += 1
        }
    }
    return t
}

function findNumberOfIncorrectSubmissions(submissions) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'incorrect'  && !submissions[i].isObsolete) {
            t += 1
        }
    }
    return t
}

function findNumberofUnmarkedSubmissionForUnit(submissions, unit) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'unmarked' && !submissions[i].isObsolete && submissions[i].unit == unit) {
            t += 1
        }
    }
    return t
}

function findNumberofCorrectSubmissionForUnit(submissions, unit) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'correct' && !submissions[i].isObsolete && submissions[i].unit == unit) {
            t += 1
        }
    }
    return t
}

function findNumberofIncorrectSubmissionForUnit(submissions, unit) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'incorrect' && !submissions[i].isObsolete && submissions[i].unit == unit) {
            t += 1
        }
    }
    return t
}

function findNumberofUnmarkedSubmissionForModule(submissions, unit, module) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'unmarked' && !submissions[i].isObsolete && submissions[i].unit == unit && submissions[i].module == module) {
            t += 1
        }
    }
    return t
}

function findNumberofCorrectSubmissionForModule(submissions, unit, module) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'correct' && !submissions[i].isObsolete && submissions[i].unit == unit && submissions[i].module == module) {
            t += 1
        }
    }
    return t
}


function findNumberofIncorrectSubmissionForModule(submissions, unit, module) {
    var t = 0
    for (var i = 0; i < submissions.length; i++) {
        if (submissions[i].state == 'incorrect' && !submissions[i].isObsolete && submissions[i].unit == unit && submissions[i].module == module) {
            t += 1
        }
    }
    return t
}

function courseCompletionPercentage(submissions) {
    var x = 0
    var y = 0
    var z = 0
    for (var unit = 0; unit < courses[cCI].units.length; unit++) {
        var cmp = unitCompletionPercentage(submissions, unit)
        x += cmp[0]
        y += cmp[1]
        z += cmp[2]
    }
    var a = 100 - x - y - z
    return [x, y, z, a]
}

function unitCompletionPercentage(submissions, unit) {
    try { var total = findNumberOfActivities(courses[cCI].units[unit]) } catch(err) { var total = findNumberOfActivities(courses[classes[cCLI].courseRef].units[unit])  }
    var x = (findNumberofUnmarkedSubmissionForUnit(submissions, unit) / total) * 100
    var y = (findNumberofCorrectSubmissionForUnit(submissions, unit) / total) * 100
    var z = (findNumberofIncorrectSubmissionForUnit(submissions, unit) / total) * 100
    var a = 100 - x - y - z
    console.log(submissions)
    return [x, y, z, a]
}


function moduleCompletionPercentage(submissions, unit, module) {
    var total = courses[classes[cCLI].courseRef].units[unit].modules[module].activities.length
    var x = findNumberofUnmarkedSubmissionForModule(submissions, unit, module) / total * 100
    var y = findNumberofCorrectSubmissionForModule(submissions, unit, module) / total * 100
    var z = findNumberofIncorrectSubmissionForModule(submissions, unit, module) / total * 100
    var a = 100 - x - y - z
    return [x, y, z, a]
}

function findNumberOfActivities(unit) {
    var t = 0
    for (var m = 0; m < unit.modules.length; m++) {
        for (var a = 0; a < unit.modules[m].activities.length; a++) {
            t += 1
        }
    }
    return t
}

function setupLogoutForm() {
    var form = '<form action="logout.py" id="logout_form" method="POST">\
               <input type="text" value=\'' + JSON.stringify(courses) + '\' name="courses" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(teachers) + '\' name="teachers" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(users) + '\' name="users" style="display: none"/>\
               <input type="text" value=\'' + JSON.stringify(classes) + '\' name="classes" style="display: none"/>\
               <input type="submit" value="Logout">\
               </form>'
    document.getElementById('logoutformdiv').innerHTML = form
}
function redr() {
    window.location.href = 'index.html'
}

function teacherIndex(lst, teachername) {
    for (var i = 0; i < lst.length; i++) {
        if (lst[i].name == teachername) {
            return i
        }
    }
}

function prepForOuterManage() {
    cTI = teacherIndex(teachers, classes[cCLI].teacher)
    console.log(cTI)
}

function setupCourseHomepage() {
    prep()
    if (cSI !== null) {
        for (var i = 0; i < users[cSI].studentcourses.length; i++) {
            document.getElementsByClassName('navbar')[0].innerHTML += '<a href="coursePage.html" onclick="localStorage.setItem(\'currentClass\',' + JSON.stringify(users[cSI].studentcourses[i].courseRef) + ')"><h4>' + classes[users[cSI].studentcourses[i].courseRef].name + '</h4></a>'
        }
    } else {
        try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
        for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
            try {
            document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
            } catch(err) {}
        }
    }
    document.getElementById('coursename').innerHTML = courses[cCI].name
    document.getElementById('courseoverview').innerHTML = courses[cCI].description
    for (var x = 0; x < courses[cCI].units.length; x++) {
        document.getElementById('unitlst').innerHTML += '<tr><td>' + (x+1) + '. ' + courses[cCI].units[x].name + '</td></tr>'
    }
    for (var y = 0; y < courses[cCI].files.length; y++) {
        document.getElementById('ref_files').innerHTML = '<li><a href="HomepageFiles/' + courses[cCI].files[y][1] + '">' + courses[cCI].files[y][0] +'</a></li>'
    }
    for (var z = 0; z < courses[cCI].links.length; z++) {
        document.getElementById('links').innerHTML = '<li><a href=' + courses[cCI].links[z][0] + '>' + courses[cCI].links[z][1] +'</a></li>'
    }
    setupLogoutForm()
}

function setupCourseHomepageEdit() {
    prep()
    try { document.getElementsByClassName('navbar')[0].innerHTML += '<a href="teacher.html"><h4>Dashboard</h4></a><a href="courseViewTeacher.html"><h4>Courses</h4></a><a href="classView.html"><h4>Classes</h4></a><a href="userView.html"><h4>Users</h4></a>'} catch (err) {}
    for (var i = 0; i < teachers[cTI].classRefs.length; i++) {
        try {
        document.getElementsByClassName('navbar')[0].innerHTML += '<a href="courseManage.html" onclick="localStorage.setItem(\'currentClass\',' + teachers[cTI].classRefs[i] + ')"><h4>' + classes[teachers[cTI].classRefs[i]].name + '</h4></a>'
        } catch(err) {}
    }
    document.getElementById('coursename').innerHTML = courses[cCI].name
    document.getElementById('courseoverview').value = courses[cCI].description
    for (var x = 0; x < courses[cCI].units.length; x++) {
        document.getElementById('unitlst').innerHTML += '<tr><td>' + (x+1) + '. ' + courses[cCI].units[x].name + '</td></tr>'
    }
    for (var y = 0; y < courses[cCI].files.length; y++) {
        document.getElementById('ref_files').innerHTML = '<li><a href="HomepageFiles/' + courses[cCI].files[y][1] + '">' + courses[cCI].files[y][0] +'</a></li>'
    }
    for (var z = 0; z < courses[cCI].links.length; z++) {
        document.getElementById('links').innerHTML = '<li><a href="' + courses[cCI].links[z][0] + '">' + courses[cCI].links[z][1] +'</a></li>'
    }
    setupLogoutForm()
}

function changeDescription() {
    courses[cCI].description = document.getElementById('courseoverview').value
    localStorage.setItem('courses', JSON.stringify(courses))
}

function addLink() {
    courses[cCI].links.push([document.add_link_form.link.value, document.add_link_form.linkname.value])
    localStorage.setItem('courses', JSON.stringify(courses))
}

function addFile(filename, href) {
    prep()
    courses[cCI].files.push([href, filename])
    localStorage.setItem('courses', JSON.stringify(courses))
    window.location.href = 'coursehomepageedit.html'
}