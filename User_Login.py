class UserLogin():
    def fromDB(self , user_id , db):
        myusers=db.query.all()
        for user1 in myusers:
            if user_id == str(user1.id):
                self.__user=user1
        return self
    
    def create(self , user):
        self.__user = user 
        return self
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.__user.db)
            