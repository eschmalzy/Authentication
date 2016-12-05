#Users

1. id
2. email
3. encryptedpass (encrypted with bcrypt)
4. fname
5. lname

#Contacts

1. id
2. name
3. phone
4. email
5. age
6. birthday
7. address

#Database Schema for Users
**CREATE TABLE users (id integer PRIMARY KEY NOT NULL,
                      email varchar(60) NOT NULL,
                      encryptedpass varchar(255) NOT NULL,
                      fname varchar(30),
                      lname varchar(30));


#Database Schema for Contacts
**CREATE TABLE contacts(id INTEGER PRIMARY KEY,
                      name VARCHAR(64) NOT NULL,
                      phone INTEGER,
                      email VARCHAR(64),
                      age INTEGER,
                      birthday CHAR(10),
                      address VARCHAR(64));**

#REST endpoint methods
getContacts
  method: GET
  localhost:8080/contacts

getContact
  method: GET
  localhost:8080/contacts/id

addContact
  method: POST
  localhost:8080/contacts

updateContact
  method: PUT
  localhost:8080/contacts/id

deleteContact
  method: DELETE
  localhost:8080/contacts/id

signIn
  method: POST
  localhost:8080/sessions

getUsers
  method: POST
  localhost:8080/users
