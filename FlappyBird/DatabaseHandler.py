import firebase_admin
from firebase_admin import credentials, firestore
from argon2 import PasswordHasher


class DatabaseHandler():

    def  __init__(self):
        cred = credentials.Certificate("FlappyBird-Secrets.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.ph = PasswordHasher()
        
        self.minLength = 3
        self.maxLength = 32
    
    # Passwords will be hashed here, also returns the account
    def AddAccount(self, user:str, password:str):
        if self.IsValidInformation(user, password) == False:
            print("Invalid information")
            return None
        
        hashedPassword = self.ph.hash(password)
        docRef = self.db.collection("Users").document()
        docInput = {
            "Bestscore": 0,
            "Username": user,
            "Password": hashedPassword
            
        }
        docRef.set(docInput)
        
        return self.GetAccount(user, password)
        
    def GetAccount(self, user:str, password:str):
        if self.UserNameIsTaken(user) == False or self.IsValidPassword(password) == False:
            return None
        
        users = self.db.collection("Users").where("Username", "==", user).stream()
        
        for user in users:
            userRef = self.db.collection("Users").document(user.id)
            doc = userRef.get()
            docDict = doc.to_dict()
            hashedPassword = docDict["Password"]
            print(hashedPassword)
            if self.ph.verify(hashedPassword, password):
                docDict["id"] = doc.id
                docDict["Password"] = password
                return docDict
                    
        return None
        
    # Assume the password isn't hashed
    def UpdateAccount(self, accountInfo):
        if accountInfo is None:
            return
        
        doc = self.db.collection("Users").document(accountInfo["id"])  
        doc.set({
             "Bestscore": accountInfo["Bestscore"],
            "Username": accountInfo["Username"],
            "Password": self.ph.hash(accountInfo["Password"])
                        
        })  
    
    def IsValidPassword(self, password:str):
        return len(password.strip()) > 0    
    
    def IsValidInformation(self, user:str, password:str):
        user = user.strip()
        password = password.strip()
        if len(user) == 0 or password == 0:
            print("Invalid length")
            return False
        
        if self.IsValidUsername(user) == False:
            print("Invalid User name")
            return False
        
        return True
    
    def IsValidUsername(self, username):
        if len(username) < self.minLength or len(username) > self.maxLength:
            return False
        
        users = self.db.collection("Users").where("Username", "==", username).stream()
        
        for user in users:
            userRef = self.db.collection("Users").document(user.id)
            doc = userRef.get()
            print(doc.to_dict())
            if user.exists:
                return False
            
        return True

    def UserNameIsTaken(self, username):
        if len(username) < self.minLength or len(username) > self.maxLength:
                    return False
                
        users = self.db.collection("Users").where("Username", "==", username).stream()
        
        for user in users:
            userRef = self.db.collection("Users").document(user.id)
            doc = userRef.get()
            print(doc.to_dict())
            if user.exists:
                return True
            
        return False
