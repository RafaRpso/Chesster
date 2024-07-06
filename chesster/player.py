# -*- coding: utf-8 -*-
import requests
from datetime import datetime 
from utils import Utils 
from typing import List, Optional, Dict, Any 
from request_manager import RequestManager
import aiohttp
import asyncio


class Player(): 
    def __init__(self):
        pass 
    
    def get_user(self, nick : str )-> List[dict]: 
        return RequestManager.http(f'user/popup/{nick}', default=False) 
    
    
    def get_player_games_archived(
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
           
           
    def get_players_by_country(self, country_iso : str ) -> List[dict ]: 
        return RequestManager.http(f'country/{country_iso.upper()}/players')['players']
    
    def get_leaderboards(self, only_rapid:bool=False, only_blitz:bool=False ) -> List[dict ]: 
        return RequestManager.http(f'/leaderboards')
        
    def get_titled_players(self, title :str="GM") -> List[dict ] : 
        return RequestManager.http(f'/titled_players/ {title}')
    
    def get_player_online_status(self, nick:str) -> dict:
        return RequestManager.http(f'/player/{nick}/is-online')
    
    def get_player_clubs(self, nick:str) -> List[dict]:
        return RequestManager.http(f'/player/{nick}/clubs')
    
    def get_player_tournaments(self, nick:str) -> List[dict]:
        return RequestManager.http(f'/player/{nick}/tournaments')
    
    def get_player_clubs(self, nick:str)->List[dict]: 
        return RequestManager.http(f'/player/{nick}/clubs')
    
    def get_player_team_matches(self, nick:str)->List[dict]:
        return RequestManager.http(f'/player/{nick}/matches')
    


        
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

    def get_player_recent_content(self, pages: int) -> List[dict]:
        """
        Retrieves recent content from Chess.com.

        :param pages: Number of pages to retrieve.
        :return: List of recent content.
        """
        return asyncio.run(self.__get_player_recent_content(pages))
        
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
            response = await session.get(f'/pub/player/{nick}/games/archives')
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
        
        
        
    async def __get_player_recent_content(self, pages: int) -> List[dict]:
        async def __fetch_content( session, url):
            async with session.get(url) as response:
                return await response.json()
        
        contents:list  = []
        _url:str = 'https://www.chess.com/callback/member/activity/hikaru?page={}'

        async with aiohttp.ClientSession() as session:
            tasks: list = []
            for i in range(pages):
                url = _url.format(i)
                tasks.append(__fetch_content(session, url))
            results = await asyncio.gather(*tasks)

            for res in results:
                if res['recentContents'] is None:
                    break
                contents.extend(res['recentContents'])

        return contents
    
