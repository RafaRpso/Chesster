# -*- coding: utf-8 -*-
import requests
from datetime import datetime 
from utils import Utils 
from typing import List, Optional, Dict, Any 
import aiohttp
import asyncio

class Player(): 
    def __init__(self):
        super().__init__()
    
    def get_user(self, nick : str )-> List[dict]: 
        #TODO: Adicionar filtros e mais funcionalidades para isso 
        res=requests.get(f'https://www.chess.com/callback/user/popup/{nick}').json()
        return res 
    
    
    
    def get_user_games(
        self, 
        nick: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None,
        only_blitz: bool = False, 
        only_rapid: bool = False, 
        only_defeat: bool = False, 
        only_win: bool = False, 
        get_pgn: bool = False, 
        get_fen: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Retrieves user games from Chess.com within the specified date range and filters.

        :param nick: Chess.com username.
        :param start_date: Start date for filtering games.
        :param end_date: End date for filtering games.
        :param only_blitz: Filter for blitz games only.
        :param only_rapid: Filter for rapid games only.
        :param only_defeat: Filter for games where the user was defeated.
        :param only_win: Filter for games where the user won.
        :param get_pgn: Retrieve PGN data.
        :param get_fen: Retrieve FEN data.
        :return: List of games matching the filters.
        """
        return asyncio.run(self.__get_user_games_async(
            nick, start_date, end_date, only_blitz, only_rapid, only_defeat, only_win, get_pgn, get_fen
        ))
           
    
        
    def __filter_games_by_user_conditions(
        self, 
        games: List[Dict[str, Any]], 
        filters: Dict[str, bool], 
        nick: str
    ) -> List[Dict[str, Any]]:
        filtered_games = []
        if not any(filters.values()):
            return games
        
        for game in games:
            if filters['only_blitz'] and game['time_class'] != 'blitz':
                continue
            if filters['only_rapid'] and game['time_class'] != 'rapid':
                continue
            if filters['only_defeat'] and not (
                (game['white']['username'] == nick and game['white']['result'] == 'checkmated') or 
                (game['black']['username'] == nick and game['black']['result'] == 'checkmated')
            ):
                continue
            if filters['only_win'] and not (
                (game['white']['username'] == nick and game['white']['result'] == 'win') or 
                (game['black']['username'] == nick and game['black']['result'] == 'win')
            ):
                continue

            filtered_game = {"url": game['url']}
            if filters['get_pgn'] and 'pgn' in game:
                filtered_game['pgn'] = game['pgn']
            if filters['get_fen'] and 'fen' in game:
                filtered_game['fen'] = game['fen']

            filtered_games.append(filtered_game)

        return filtered_games
            
    async def __fetch_game_data(self, url: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        async with session.get(url) as response:
            return await response.json()
        
    def __filter_games_by_date(self, start_date: datetime|None,end_date: datetime|None,game:str):
            if not game:
                return False
            dates=Utils.extract_date_from_url_games_by_date(game)
            gm_year=dates['year']
            gm_month=dates['month']
            
            if start_date and (gm_year < start_date.year or (gm_year == start_date.year and gm_month < start_date.month)):
                return False
            if end_date and (gm_year > end_date.year or (gm_year == end_date.year and gm_month > end_date.month)):
                return False
            return True
        
    async def __get_user_games_async(
        self, 
        nick: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None,
        only_blitz: bool = False, 
        only_rapid: bool = False, 
        only_defeat: bool = False, 
        only_win: bool = False, 
        get_pgn: bool = False, 
        get_fen: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Retrieves user games from Chess.com within the specified date range and filters.

        :param nick: Chess.com username.
        :param start_date: Start date for filtering games.
        :param end_date: End date for filtering games.
        :param only_blitz: Filter for blitz games only.
        :param only_rapid: Filter for rapid games only.
        :param only_defeat: Filter for games where the user was defeated.
        :param only_win: Filter for games where the user won.
        :param get_pgn: Retrieve PGN data.
        :param get_fen: Retrieve FEN data.
        :return: List of games matching the filters.
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            response = await session.get(f'https://api.chess.com/pub/player/{nick}/games/archives')
            games_by_date = await response.json()
            
            games_months = [
                {'game': game, 'date': Utils.extract_date_from_url_games_by_date(game)} 
                for game in games_by_date['archives'] 
                if self.__filter_games_by_date(start_date, end_date, game)
            ]

            tasks = [self.__fetch_game_data(g['game'], session) for g in games_months]
            all_games_responses = await asyncio.gather(*tasks)
            
            all_games = [game for response in all_games_responses for game in response['games']]

            filters = {
                'only_blitz': only_blitz,
                'only_rapid': only_rapid,
                'only_defeat': only_defeat,
                'only_win': only_win,
                'get_pgn': get_pgn,
                'get_fen': get_fen
            }

            return self.__filter_games_by_user_conditions(all_games, filters, nick)