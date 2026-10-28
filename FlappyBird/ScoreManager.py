class ScoreManager():
    def __init__(self):
        self.bestScore = 0
        self.score = 0
        
    def UpdateBestScore(self):
        if self.score > self.bestScore:
            self.bestScore = self.score
            
    def IncreaseScore(self):
        self.score += 1
        self.UpdateBestScore()
    
    def ResetScore(self):
        self.score = 0