#!/usr/bin/python
print('Content-type: text/html\n')

import json
import cgi
import cgitb; cgitb.enable()

storage = json.loads(open('store.json').read())
# for x in storage: print(x)

print('<html>')
print('<link rel="stylesheet" href="main.css" />')
print("<script src='script.js'></script>")
print('<title>Gallifrey</title>')
print('<body id="loginpage" onload=\'loginPrep(' + json.dumps(storage[0]) + ',' + json.dumps(storage[1]) + ',' + json.dumps(storage[2]) + ',' + json.dumps(storage[3]) +')\'>')
print('''
<div class='navbar'><h3>Gallifrey</h3></div>
    
    <div id='logindiv'><h1>Login</h1><form name='login_form'>
        <input type='text' name='username' placeholder="Username" />
        <input type='password' name='pass' placeholder="Password" />
    </form>
    <button onclick='login()'>Verify</button>
    <div id='go'><a href='student.html' id='go_link'>Login</a></div>
    
    <div class='footer'>
        Gallifrey 1.0.0<br>
        Developed By <a href='mailto:nick.p@iinet.net.au'>Nick Patrikeos</a>.
    </div>
    </div>
''')
print('</body>')
print('</html>')
