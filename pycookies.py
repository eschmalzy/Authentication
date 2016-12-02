from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from sessionStore import SessionStore
from usrdb import *
from ContactsDB import *
from urllib.parse import urlparse, parse_qs
from passlib.hash import bcrypt

gSessionStore = SessionStore()
gEmail = ""

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #index or list action
        self.load_session()
        lst = ContactsDB()
        usr = UserDB()
        if self.path.startswith("/contacts/"):
            #handle specific contact
            idPath = self.path
            contact = lst.getContact(idPath)
            if len(contact) == 2:
                self.header404("Couldn't find contact")
            else:
                self.header200()
                self.wfile.write(bytes(contact, "utf-8"))
        elif self.path.startswith("/contacts"):
            #handle contacts
            matched = False
            allUsers = usr.getUsernames()
            for i in allUsers:
                if gSessionStore.sessionData[self.session] == i[0] and i[0] != "":
                    matched = True
                    break
                else:
                    matched = False
            print(matched)
            if matched:
                contacts = lst.getContacts()
                self.header200()
                self.wfile.write(bytes(contacts, "utf-8"))
            else:
                self.header401()
        else:
            self.header404("Collection not found")

    def do_POST(self):
        #index or list action
        self.load_session()
        lst = ContactsDB()
        usr = UserDB()
        if self.path.startswith("/contacts"):
            length = self.header201()
            data, amount = self.parseInput(length)
            if amount > 6:
                self.header404("Unable to add contact")
                return
            lst.addContact(data)
            self.wfile.write(bytes(lst.getContacts(), "utf-8"))
        elif self.path.startswith("/users/"):
            idPath = self.path
            userInfo = usr.getUser(idPath)
            length = int(self.headers['Content-Length'])
            data, amount = self.parseInput(length)
            testPass = data["encryptedpass"]
            if userInfo:
                if bcrypt.verify(testPass[0],userInfo[0]["encryptedpass"]):
                    print("saved email")
                    self.header200()
                    self.wfile.write(bytes(json.dumps(userInfo),"utf-8"))
                    gSessionStore.sessionData[self.session] = userInfo[0]["email"]
                    print(gSessionStore.sessionData)
                else:
                    self.header401()
        elif self.path.startswith("/users"):
            ids = usr.getUsernames()
            length = int(self.headers['Content-Length'])
            data, amount = self.parseInput(length)
            for i in ids:
                if i[0] == data["email"][0]:
                    self.header401()
                    return
            self.header201()
            data["encryptedpass"][0] = bcrypt.encrypt(data["encryptedpass"][0])
            useradded = usr.addUser(data)
            self.wfile.write(bytes(useradded, "utf-8"))
        else:
            self.header404("Collection not found")

    def do_PUT(self):
        self.load_session()
        lst = ContactsDB()
        if self.path.startswith("/contacts/"):
            id = lst.getPath(self.path)
            allid = lst.getIDS()
            for i in allid:
                if i == id:
                    length = self.altHeader201()
                    data, num = self.parseInput(length)
                    lst.updateContact(self.path, data)
                    self.wfile.write(bytes(lst.getContacts(), "utf-8"))
                else:
                    self.header404("No such user")
        elif self.path.startswith("/contacts"):
            self.header404("Cannot update collection")
        else:
            self.header404("Collection not found")

    def do_DELETE(self):
        self.load_session()
        lst = ContactsDB()
        usr = UserDB()
        if self.path.startswith("/contacts/"):
            delete = lst.deleteContact(self.path)
            if delete == False:
                self.header404("No such contact")
            else:
                self.header200()
        else:
            self.header404("Collection not found")

    def do_OPTIONS(self):
        # self.m200()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.end_headers()

    def altHeader200(self):
        #OK
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", '*')
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def header200(self):
        #OK
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def header404(self, error):
        #error
        self.send_response(404)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<p>404 "+error+"</p>", "utf-8"))

    def header401(self):
        self.send_response(401)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<p>401 Unable to authenticate.</p>", "utf-8"))

    def altHeader201(self):
        self.send_response(201)
        self.send_header("Access-Control-Allow-Origin", '*')
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        length = int(self.headers['Content-Length'])
        return length

    def header201(self):
        #created element
        self.send_response(201)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        length = int(self.headers['Content-Length'])
        return length

    def header204(self):
        #didn't create anything and didn't give anything back
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def parseInput(self, length):
        data = self.rfile.read(length).decode("utf-8")
        num = 0
        parsed = parse_qs(data)
        for key in parsed:
            num += 1
        return parsed, num

    def load_session(self):
        self.load_cookie()
        # check for a session ID in a cookie
        # IF cookie exists:
        print("self.cookie")
        print(self.cookie)
        if "!" not in self.cookie:
            print("COOKIE")
            # try to load the session object using the ID
            self.session = gSessionStore.getSession(self.cookie["sessionID"].value)
            # IF session data was retrieved:
            if self.session != None:
                print("Session Exists")
                print(self.session)
                # yay! save/use it.
            else:
                # create a new session object, save/use it.
                print("Created new session")
                self.session = gSessionStore.createSession()
                print(self.session)
                gSessionStore.sessionData[self.session] = ""
                # store the session ID in a cookie
                self.cookie["sessionID"] = self.session
        else:
            print("NO COOKIE")
            self.cookie = cookies.SimpleCookie()
            # create a new session object, save/use it.
            self.session = gSessionStore.createSession()
            # store the session ID in a cookie
            self.cookie["sessionID"] = self.session

    def load_cookie(self):
        if "Cookie" in self.headers:
            print("cookie in headers")
            cookie = cookies.SimpleCookie()
            sessionInfo = self.headers["Cookie"]
            cookie.load(sessionInfo)
            self.cookie = cookie
        else:
            print("No cookie in headers")
            self.cookie = cookies.SimpleCookie()
            self.cookie["!"] = ""

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Listening...")
    server.serve_forever()

run()
