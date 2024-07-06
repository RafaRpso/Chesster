# -*- coding: utf-8 -*-
import requests 
from datetime import datetime 
from typing import List, Optional, Dict, Any 
import json 
class Match(): 
    def __init__(self) -> None:
         pass
    
    def get_daily_puzzle(self,start_date:datetime,end_date:datetime) : 
        def date_to_str(d:datetime): 
            return f'{d.year}-{d.month}-{d.day}'
        s=date_to_str(start_date)
        e=date_to_str(end_date)
        res=requests.get(f'https://www.chess.com/callback/puzzles/daily?start={s}&end={e}').text
        
        return res        
    
    def get_match(url:str, with_pgn:bool=False):
        ''' Se for com o PGN, tenho que fazer de outro jeito, por isso a condição'''
        
    