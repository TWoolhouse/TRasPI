import core
from windows.game import Room

class Main:

    def __init__(self):
        super().__init__()
        self.flag = True
        self.score = 0
    
    async def show(self):
        await Room(self)
        self.finish()
        #Results screen? 
        

        