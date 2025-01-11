import sqlite3

def open_database():
    with sqlite3.connect("userInfo.db")as db:
        cursor=db.cursor()
        cursor.execute("""  CREATE TABLE IF NOT EXISTS
                   tblUserDetails
                   (UserName TEXT,
                   Password TEXT,
                   HighScore_1 INT,
                   HighScore_2 INT,
                   HighScore_3 INT,
                   HighScore_4 INT,
                   HighScore_5 INT)  """)
        
def add_user_details(username, password):
    if username==''or password=='':
        pass
    else:
        with sqlite3.connect("userInfo.db")as db:
            cursor=db.cursor()
            values=(username, password, 0, 0, 0, 0, 0)
            sql = """INSERT OR IGNORE INTO tblUserDetails 
                	(UserName, Password, HighScore_1, HighScore_2, HighScore_3, HighScore_4, HighScore_5)
                    
                    	VALUES (?, ?, ?, ?, ?, ?, ?) """	   
            cursor.execute(sql, values)

        db.commit()