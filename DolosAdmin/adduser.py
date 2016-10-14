import hashlib
import uuid
import os
import sqlite3

def generateHash(salt, inp):
    hashedInput = hashlib.sha512(inp + salt).hexdigest()
    return hashedInput

def generateSalt():
    return uuid.uuid4().hex

def addUser(username, password):
    BASE_DIR = os.path.dirname(os.path.abspath('./Dolos'))
    DB_PATH = os.path.join(BASE_DIR, 'dolos.sqlite3')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    salt = generateSalt()
    password = generateHash(salt, password)

    cursor.execute('''
                    INSERT INTO admins(username, password, salt) values(?,?,?);
                   ''', (username, password, salt))

    conn.commit()
    conn.close()

    print 'New user added'
    print 'Username: {}'.format(username)
