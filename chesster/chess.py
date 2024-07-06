from extractor import Extractor 
from player import Player  
from match import Match

class Chesster: 
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.1 Safari/537.36',
            }
        #TODO: Inserir DTO em todos 
        self.match=Match()
        self.player=Player() 
        self.extractor=Extractor() 
    
