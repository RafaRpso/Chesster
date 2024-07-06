from extractor import Extractor 
from player import Player  
from match import Match

class Chesster: 
    def __init__(self) -> None:
        #TODO: Inserir DTO em todos 
        self.match=Match()
        self.player=Player() 
        self.extractor=Extractor() 
    
