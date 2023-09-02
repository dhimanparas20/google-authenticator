from os import system
import sqlite3
import json
from passlib.hash import pbkdf2_sha256

class SQLiteDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.conn.close()   

    def hash_password(self, password):
        # Hash the password using Passlib's pbkdf2_sha256
        return pbkdf2_sha256.hash(password)  

    def createTable(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                              "name" TEXT,
                              "email" TEXT PRIMARY KEY,
                              "password" TEXT
                              )''')
        self.conn.commit()
        self.conn.close()    

    def insertData(self, name, email, password):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        try:
            hashed_password = self.hash_password(password)
            query = "INSERT INTO users (name,email,password) VALUES (?, ?, ?)"
            values = (name, email, hashed_password)
            self.cursor.execute(query, values)
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("Insert Exception:", e)
            return False

    def fetchAll(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM users")
        data = self.cursor.fetchall()

        columns = ["name", "email", "password"]
        json_data = [dict(zip(columns, row)) for row in data]
        self.conn.close()  
        return json.dumps(json_data)
       
        columns = ["name", "email", "password"]
        json_data = [dict(zip(columns, row)) for row in data]
        return json.dumps(json_data)

    def fetchByMail(self, email):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        query = "SELECT * FROM users WHERE email = ?"
        values = (email,)  # Make sure to pass the values as a tuple
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        self.conn.close()
        
        if not data:
            return False
        
        columns = ["name", "email", "password"]
        json_data = [dict(zip(columns, row)) for row in data]
        newdata =json.dumps(json_data)
        return True    

    def mailExists(self,email):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        try:
            query = "SELECT email FROM users WHERE email = ?"
            values = (email,)  # Make sure to pass the values as a tuple
            self.cursor.execute(query, values)
            data = (self.cursor.fetchall())[0][0]
            return True
    
        except:
            return False


    def verify_password(self, email, provided_password):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        try:
            query = "SELECT password FROM users WHERE email = ?"
            values = (email,)  # Make sure to pass the values as a tuple
            self.cursor.execute(query, values)
            stored_hash = (self.cursor.fetchall())[0][0]
            self.conn.close()
            return pbkdf2_sha256.verify(provided_password, stored_hash)       
        except:
            return False



