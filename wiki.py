#!/usr/bin/python

from bottle import route,run,get,post,request

import shelve
db = shelve.open("wiki.db",writeback=True)
def markup(data):
    return str(data.replace("\n","<br>"))

@route("/")
def print_pages():
    html = "<br>"
    for elem in db:
        html += "<a href="+markup(elem)+">"+markup(elem)+"</a><br>"
    return html

@get("/:name")
def get_page(name):
    if db.has_key(name):
        return markup(db[name])
    else:
        return ""

@get("/:name/:command")
def node(name,command):
    if db.has_key(name):
        cont = db[name]
    else:
        cont = ""
    if command == "edit":
        return str('<form method="POST"><textarea name="content" type="text" rows="40" cols="120">'+cont+'</textarea><br><input type="submit" value="submit" /></form>')
    elif command == "del":
        db.pop(name)
        return str("Deleted: "+name)
    else:
        return "Unknown command: ", command

@post('/:name/:command')
def node_submit(name,command):
    cont  = request.forms.get('content')
    db[name] = cont
    return markup(cont)


run(host='localhost', port=8080)
print "[+] Flushing data to db..."
db.close()
print "[+] Done, bye"