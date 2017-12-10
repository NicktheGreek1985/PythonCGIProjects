#!/usr/bin/python
print('Content-type: text/html\n')

import cgi
import cgitb; cgitb.enable(); # Will be replaced with error handling

import algernon

try:
    form = cgi.FieldStorage()

    algo = form.getvalue('algorithm')

    DCSolution = algernon.DivideConquer()
    SortingSolution = algernon.Sorting()
    RandomisedSolution = algernon.Randomised()

    # Computes the answer with the relevant class method
    if algo == 'kmultiply':
        answer = DCSolution.karatsuba_multiply(int(form.getvalue('intA')), int(form.getvalue('intB')))

    elif algo == 'inversioncount':
        answer = DCSolution.inversion_count(list(map(int, form.getvalue('lst').split())))[0]

    elif algo == 'mergesort':
        answer = SortingSolution.mergesort(list(map(int, form.getvalue('lst').split())))

    elif algo == 'dquicksort':
        # Called in-place
        lst = list(map(int, form.getvalue('lst').split()))
        SortingSolution.d_quicksort(lst)
        answer = lst

    elif algo == 'rquicksort':
        # Called in-place
        lst = list(map(int, form.getvalue('lst').split()))
        RandomisedSolution.r_quicksort(list(map(int, form.getvalue('lst').split())))
        answer = lst[::-1]

    elif algo == 'mincut':
        # Uses eval as the input is a python dictionary (adjacency list)
        answer = RandomisedSolution.kmincut(eval(form.getvalue('graph')))
    else:
        pass

    print('<html>')
    print('<head>')
    print('<link rel="stylesheet" href="main.css" />')
    print('<script src="script.js"></script>')
    print('</head>')

    print('<body>')
    print('<div class="main" id="answer">')
    print('<h1>The answer is ' + repr(answer) + '</h1>')
    print('</div>')
    print('<div id="backbtn" onmouseover="highlightbtn(this)" onmouseout="unhighlightbtn(this)" onclick="backtopage()">Back to Main Page</div>')
    print('</body>')
    print('</html>')
except:
    print('<html>')
    print('<head>')
    print('<link rel="stylesheet" href="main.css" />')
    print('<script src="script.js"></script>')
    print('</head>')

    print('<body>')
    print('<div class="main" id="answer">')
    print('<h1>Please enter the data again correctly, an error occurred./</h1>')
    print('</div>')
    print('<div id="backbtn" onmouseover="highlightbtn(this)" onmouseout="unhighlightbtn(this)" onclick="backtopage()">Back to Main Page</div>')
    print('</body>')
    print('</html>')