import sqlite3
import json

class ContactsDB:

    def __init__(self):
        pass

    def getIDS(self):
        connection = sqlite3.connect("demodb.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id from contacts")
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
        values = ["", "", "", "", "", ""]
        for key in data:
            if key == "name":
                values[0] = (data.get(key)[0])
            if key == "phone":
                values[1] = int(data.get(key)[0])
            if key == "email":
                values[2] = data.get(key)[0]
            if key == "age":
                values[3] = int(data.get(key)[0])
            if key == "birthday":
                values[4] = data.get(key)[0]
            if key == "address":
                values[5] = (data.get(key)[0])
        return values

    def rowFactory(self, cursor, row):
        d = {}
        for idX, col in enumerate(cursor.description):
            d[col[0]] = row[idX]
        return d

    def getContact(self, idPath):
        personID = self.getPath(idPath)
        connection = sqlite3.connect("demodb.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = (?)", (personID,))
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    def getContacts(self):
        connection = sqlite3.connect("demodb.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    def deleteContact(self, path):
        personID = self.getPath(path)
        connection = sqlite3.connect("demodb.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * from contacts WHERE id = (?)",(personID,))
        result = cursor.fetchall()
        if result == []:
            return False
        cursor.execute("DELETE FROM contacts WHERE id = (?)", (personID,))
        connection.commit()
        # rows = cursor.fetchall()
        connection.close()
        # return json.dumps(rows)


    def addContact(self,contactInfo):
        contactInfo = self.parseDict(contactInfo)
        connection = sqlite3.connect("demodb.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contacts (name,phone,email,age,birthday,address) VALUES (?,?,?,?,?,?)",(contactInfo[0],contactInfo[1],contactInfo[2],contactInfo[3],contactInfo[4],contactInfo[5]))
        connection.commit()
        cursor.execute("SELECT * FROM contacts;")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)

    def updateContact(self, path, contactInfo):
        personID = self.getPath(path)
        contactInfo = self.parseDict(contactInfo)
        connection = sqlite3.connect("demodb.db")
        connection.row_factory = self.rowFactory
        cursor = connection.cursor()
        cursor.execute("SELECT * from contacts WHERE id = (?)",(personID,))
        result = cursor.fetchall()
        if result == []:
            return False
        cursor.execute("UPDATE contacts SET name=?,phone=?,email=?,age=?,birthday=?,address=? WHERE id=?",(contactInfo[0],contactInfo[1],contactInfo[2],contactInfo[3],contactInfo[4],contactInfo[5],personID))
        connection.commit()
        cursor.execute("SELECT * FROM contacts;")
        rows = cursor.fetchall()
        connection.close()
        return json.dumps(rows)
