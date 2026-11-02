import json


class Packet():
    def __init__(self):
        self.birdColor = 0
        self.birdFrame = 0
        self.birdPos = (0,0)
        self.isDead = False
        self.pipesInfo:list[tuple[int, int, int, int, bool]] = []#The x, y, width, height, and if it's top or bottom(true for top)
        self.birdScore = 0
        self.username = ""
        self.playerCount = 1
        self.readyCount = 0
        self.isReady = False
        self.dissconnect = False
    
    def SetInfo(self,colorNum,frame,pos,isDead,pipeInfos,score,username,playerCount,readyCount,isReady, dissconnect = False):
        self.birdColor = colorNum
        self.birdFrame = frame
        self.birdPos = pos
        self.isDead = isDead
        self.pipesInfo = pipeInfos
        self.birdScore = score
        self.username = username
        self.playerCount = playerCount
        self.readyCount = readyCount
        self.isReady = isReady
        self.dissconnect = dissconnect
        
    
    def ConvertToJSON(self):
        return {
            "birdColor": self.birdColor,
            "birdFrame": self.birdFrame,
            "birdPos": self.birdPos,
            "isDead": self.isDead,
            "pipesInfo": self.pipesInfo,
            "birdScore": self.birdScore,
            "username": self.username,
            "playerCount":self.playerCount,
            "readyCount": self.readyCount,
            "isReady": self.isReady,
            "dissconnect":self.dissconnect
        }
    
    @classmethod
    def ConvertFromJSON(cls, data_dict):
        p = cls()
        if data_dict:
            p.birdColor = data_dict.get("birdColor", 0)
            p.birdFrame = data_dict.get("birdFrame", 0)
            p.birdPos = tuple(data_dict.get("birdPos", (0, 0))) # Ensure tuple
            p.isDead = data_dict.get("isDead", False)
            # Ensure inner pipe info stays tuples as msgpack often decodes them as lists
            p.pipesInfo = [tuple(pipe) for pipe in data_dict.get("pipesInfo", [])] 
            
            p.birdScore = data_dict.get("birdScore", 0)
            p.username = data_dict.get("username", "")
            p.playerCount = data_dict.get("playerCount", 1)
            p.readyCount = data_dict.get("readyCount", 0)
            p.isReady = data_dict.get("isReady", False)
            p.dissconnect = data_dict.get("dissconnect", False)
        return p
        
    
    def PrintInfo(self):
        print(f"Username: {self.username}\nPos: {self.birdPos}\nScore: {self.birdScore}\nColor: {self.birdColor}\n\n")