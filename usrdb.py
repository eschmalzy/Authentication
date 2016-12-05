import sqlite3
import json

class UserDB:

    def __init__(self):
        pass

    def getUsernames(self):
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("SELECT email from users")
        result = cursor.fetchall()
        return result

    def getPath(self, idPath):
        i = -1
        endChar = idPath[i]
        while endChar != "/":
            i -= 1
            endChar = idPath[i]
        personID = idPath[i+1:]
        return personID

    def parseDict(self,data):
        values = ["", "", "", ""]
        print(values)
        for key in data:
            if key == "email":
                values[0] = data.get(key)[0]
            if key == "encryptedpass":
                values[1] = data.get(key)[0]
            if key == "fname":
                values[2] = data.get(key)[0]
            if key == "lname":
                values[3] = data.get(key)[0]
        return values

    def rowFactory(self, cursor, row):
        d = {}
        for idX, col in enumerate(cursor.description):
            d[col[0]] = row[idX]
        return d

    def getUser(self, idPath):
        personID = idPath[0]
        connection = sqlite3.connect("users.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = (?)", (personID,))
        rows = cursor.fetchall()
        connection.close()
        return rows

    def getUsers(self):
        connection = sqlite3.connect("users.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    def addUser(self,contactInfo):
        contactInfo = self.parseDict(contactInfo)
        connection = sqlite3.connect("users.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        print(contactInfo)
        cursor.execute("INSERT INTO users (email,encryptedpass,fname,lname) VALUES (?,?,?,?)",(contactInfo[0],contactInfo[1],contactInfo[2],contactInfo[3]))
        connection.commit()
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    # def updateUser(self, path, contactInfo):
    #     personID = self.getPath(path)
    #     contactInfo = self.parseDict(contactInfo)
    #     connection = sqlite3.connect("users.db")
    #     connection.row_factory = self.rowFactory
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * from users WHERE id = (?)",(personID,))
    #     result = cursor.fetchall()
    #     if result == []:
    #         return False
    #     cursor.execute("UPDATE users SET name=?,phone=?,email=?,age=?,birthday=?,address=? WHERE id=?",(contactInfo[0],contactInfo[1],contactInfo[2],contactInfo[3],contactInfo[4],contactInfo[5],personID))
    #     connection.commit()
    #     cursor.execute("SELECT * FROM users;")
    #     rows = cursor.fetchall()
    #     connection.close()
    #     return json.dumps(rows)
