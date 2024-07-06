# -*- coding: utf-8 -*-
import requests 
from datetime import datetime 
from typing import List, Optional, Dict, Any 
import json 
from request_manager import RequestManager 
class Match(): 
    def __init__(self) -> None:
        self.headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.1 Safari/537.36',
                    }
    
    def get_daily_puzzle(self, random: bool=False ) -> List[dict]:
        if random : 
            return RequestManager.http('puzzle/random', default=False) 
        return RequestManager.http('puzzle', default=False)
    
    
    def get_daily_puzzle_archived(self,start_date:datetime,end_date:datetime) : 
        def date_to_str(d:datetime): 
            return f'{d.year}-{d.month}-{d.day}'
        s=date_to_str(start_date)
        e=date_to_str(end_date)
        res=requests.get(f'https://www.chess.com/callback/puzzles/daily?start={s}&end={e}', headers=self.headers).json()
        
        return res        
    
    def get_match(self, url:str, with_pgn:bool=False):
        # https://www.chess.com/game/live/81807947466 
        #TODO: Colocar DTO 
        def get_id(txt:str): 
            return txt.split('/')[-1]
        
        id:str = get_id(url)
        res:str =requests.get(f'https://www.chess.com/callback/live/game/{id}', headers=self.headers).json()['game']
        get_date_res:str =res['pgnHeaders']['Date']
        
        if(with_pgn): 
            get_date:List[dict] =list(map(lambda x : int(x) , get_date_res.split('.')))
            date:datetime =datetime(get_date[0], get_date[1],get_date[2])
            player:str =res['pgnHeaders']['White']
            response_pgn:List[dict] =requests.get(f'https://api.chess.com/pub/player/{player}/games/{date.year}/{date.month}', headers=self.headers).json()
            games:List[dict] =response_pgn['games']
            
            for g in games : 
                if(get_id(g['url'])==id ) :
                    return g
            return {'error': 'match not found'}
        return res 
            
        
    