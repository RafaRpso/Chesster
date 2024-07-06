# -*- coding: utf-8 -*- 
from chesster.request_manager import RequestManager
from datetime import datetime 
from typing import List  
from typing import Optional
from chesster.utils import Utils
import asyncio 
import aiohttp 

class Service : 
    class Match : 
        def get_daily_puzzle(self, random=False ): 
            if random : 
                return RequestManager.http('puzzle/random')
            return RequestManager.http('puzzle')
        
        
        def get_daily_puzzle_archived(self, start_date, end_date): 
            def date_to_str(d):
                return f'{d.year}-{d.month}-{d.day}'

            s: str = date_to_str(start_date)
            e: str = date_to_str(end_date)

            return RequestManager.http(f'puzzles/daily?start={s}&end={e}', default=False)
        
        def get_match(self, url: str, pgn: bool = False):
            def get_id(txt: str):
                return txt.split('/')[-1]

            id: str = get_id(url)
            response_json:str= RequestManager.http(f'live/game/{id}', default=False)
            res=response_json['game']
            get_date_res: str = res['pgnHeaders']['Date']

            if pgn:
                get_date: List[int] = list(map(lambda x: int(x), get_date_res.split('.')))
                date: datetime = datetime(get_date[0], get_date[1], get_date[2])
                player: str = res['pgnHeaders']['White']
                response_pgn: List[dict] = RequestManager.http(f'player/{player}/games/{date.year}/{date.month}')
                games: List[dict] = response_pgn['games']

                for g in games:
                    if get_id(g['url']) == id:
                        return g
                return {'error': 'match not found'}
            
            return res
    
    class Player : 
    
        def __init__(self):
            pass 
            
        def get_player(self, nick : str):
            return RequestManager.http(f'user/popup/{nick}', default=False) 
            
            
        def get_players_by_country(self, country_iso : str ) -> List[dict ]: 
            return RequestManager.http(f'country/{country_iso.upper()}/players')['players']
            
        def get_leaderboard(self) -> List[dict ]: 
            return RequestManager.http(f'/leaderboards')
            
                
        def get_titled_players(self, title :str="GM") -> List[dict ] : 
            return RequestManager.http(f'titled/{title}')
            
            
        def get_player_online_status(self, nick: str) -> dict:
            return RequestManager.http(f'user/popup/{nick}', default=False)['onlineStatus']
        
        def get_player_clubs(self, nick: str) -> List[dict]:
            return RequestManager.http(f'player/{nick}/clubs')
        
        def get_player_tournaments(self, nick: str) -> List[dict]:
            return RequestManager.http(f'player/{nick}/tournaments')
        
        def get_player_team_matches(self, nick: str) -> List[dict]:
            return RequestManager.http(f'player/{nick}/matches')

        
        def get_player_recent_content(self, pages: int) -> List[dict]:
            return asyncio.run(self.__get_player_recent_content(pages))
        
         
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
        ) : 
            return asyncio.run(self.__get_user_games_async(
                nick, start_date, end_date, only_blitz, only_rapid, only_defeat, only_win, get_pgn, get_fen
            ))
            
            
         
        def get_player_recent_content(self, nick, pages: int) -> List[dict]:
            return asyncio.run(self.__get_player_recent_content(nick, pages))
        
        
        def __filter_games_by_user_conditions(self,games ,filters,nick) :
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
        ) : 
            headers={           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.1 Safari/537.36'}
            async with aiohttp.ClientSession(headers=headers) as session:
                response = await session.get(f'https://api.chess.com/pub/player/{nick}/games/archives')
                games_by_date = await response.json()
                
                games_months = [
                    {'game': game, 'date': Utils.extract_date_from_url_games_by_date(game)} 
                    for game in games_by_date['archives'] 
                    if self.__filter_games_by_date(start_date, end_date, game)
                ]

                tasks = [self.fetch_game_data(g['game'], session) for g in games_months]
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
            
            
            
        async def __get_player_recent_content(self, nick , pages: int) -> List[dict]:
            async def __fetch_content( session, url):
                async with session.get(url) as response:
                    return await response.json()
            
            contents:list  = []
            _url:str = 'https://www.chess.com/callback/member/activity/{}?page={}'

            async with aiohttp.ClientSession() as session:
                tasks: list = []
                for i in range(pages):
                    url = _url.format(nick,i)
                    tasks.append(__fetch_content(session, url))
                results = await asyncio.gather(*tasks)

                for res in results:
                    if res['recentContents'] is None:
                        break
                    contents.extend(res['recentContents'])

            return contents
        
        async def fetch_game_data(self, url: str, session ):
            async with session.get(url) as response:
                return await response.json()