class User:
    def __init__(self,userId,username,password,role):
        self.userId=userId
        self.username=username
        self.password=password
        self.role=bool(role)
        
