import sqlite3

class DatabaseService:
    
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.createTables()
        
    def createTables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username varchar(20), password varchar(20))''')
        self.conn.commit()