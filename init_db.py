import sqlite3

class DB:
    def __init__(self,db):
        self.conn = sqlite3.Connection(db)
        self.cursor = self.conn.cursor()
        
    def user_exists(self,user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?",(user_id,))
        result = result.fetchall()
        return bool(len(result))
    
    def add_user(self,user_id,birthday_date,username):
        self.cursor.execute("INSERT INTO users (user_id,birthday_date,username) VALUES (?,?,?)",(user_id,birthday_date,username,))
        return self.conn.commit()
    
    def agreement_yes(self,user_id):
        self.cursor.execute("UPDATE users SET agreement = 1 WHERE user_id = ?",(user_id,))
        return self.conn.commit()
    
    def agreement_no(self,user_id):
        self.cursor.execute("UPDATE users SET agreement = 0 WHERE user_id = ?",(user_id,))
        return self.conn.commit()
    
    def get_users_subs(self,user_id):
        result = self.cursor.execute("SELECT user_id,username,subscribes FROM users WHERE user_id != ?",(user_id,))
        return result.fetchall()
    
    def get_user_subs(self,user_id):
        result = self.cursor.execute("SELECT agreement, subscribes, username FROM users WHERE user_id = ?",(user_id,))
        return result.fetchall()
    
    def update_subs(self,user_id,subs):
        self.cursor.execute("UPDATE users SET subscribes = ? WHERE user_id = ?",(subs,user_id,))
        return self.conn.commit()
    
    def get_date(self):
         result = self.cursor.execute("SELECT user_id, birthday_date FROM users")
         return result.fetchall()