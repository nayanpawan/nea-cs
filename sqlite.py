import sqlite3

def open_database():
    ##creating database##
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
        db.commit()  

def add_user_details(username, password):
        ##add user to database if it dosen't already exist##
        with sqlite3.connect("userInfo.db")as db:
            cursor=db.cursor()
            value=(username,)
            sql="""SELECT * from tblUserDetails
                   WHERE UserName = ? """
            cursor.execute(sql,value)
            result=cursor.fetchall()
            
            if result:
                return False
            else:
                values_in=(username, password, 0, 0, 0, 0, 0)
                sql = """INSERT OR IGNORE INTO tblUserDetails 
                        (UserName, Password, HighScore_1, HighScore_2, HighScore_3, HighScore_4, HighScore_5)
                        
                            VALUES (?, ?, ?, ?, ?, ?, ?) """	   
                cursor.execute(sql, values_in)

                db.commit()
                return True
            
def check_user_exists(username,password):
     ##checking if details enetred match the one that exist in database##
     with sqlite3.connect("userInfo.db")as db:
            cursor=db.cursor()
            value=(username,password)
            sql="""SELECT * from tblUserDetails
                   WHERE UserName = ? AND Password = ?"""
            cursor.execute(sql,value)
            result=cursor.fetchall()
            
            if result:
                return True
            else:
                 return False
            
def get_highscores(username):
    ##retrives highscores for username that is logged in##
    with sqlite3.connect("userInfo.db")as db:
            cursor=db.cursor()
            value=(username,)
            sql="""SELECT HighScore_1, HighScore_2, HighScore_3, HighScore_4, HighScore_5
                   from tblUserDetails
                   WHERE UserName=?"""
            cursor.execute(sql,value)
            result=cursor.fetchone()
            if result:
                return list(result)
            else:
                 return None

def update_highscores(username, new_highscores):
    ##updating the new highscores on database##
    with sqlite3.connect("userInfo.db") as db:
        cursor = db.cursor()
        sql = """UPDATE tblUserDetails
                 SET HighScore_1 = ?, HighScore_2 = ?, HighScore_3 = ?, 
                     HighScore_4 = ?, HighScore_5 = ?
                 WHERE UserName = ?"""
        
        cursor.execute(sql, (*new_highscores, username))
        db.commit()            
