#Contains glabol info(like screen dimensions, fps, etc) to prevent writting same thing in each file
class GlobalInfo():
    screenWidth = 1280
    screenHeight = 720
    
    mouseClick = False
    pressedKey = False
    curKey = None
    curUnicode = None
    
    def ResetTempInfo(self):
        GlobalInfo.mouseClick = False
        GlobalInfo.pressedKey = False
        GlobalInfo.curUnicode = None
        GlobalInfo.curKey = None