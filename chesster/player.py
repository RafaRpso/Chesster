# -*- coding: utf-8 -*-
from datetime import datetime 
from typing import List, Optional, Dict, Any 
from chesster.src.service import Service

class Player(): 
    """
    Represents a player in Chess.com.

    This class provides methods to retrieve various information about a player, such as user information, player games, player clubs, and more.

    """
    def __init__(self):
        self.service = Service.Player() 
        

    def get_player(self, nick : str )-> List[dict]:
        """
        Retrieves user information from Chess.com.
        
        :param nick: Chess.com username.
        :return: User information.
        
        """ 
        return self.service.get_player(nick) 
    
    
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
        return self.service.get_player_games_archived( nick, start_date, end_date, only_blitz, only_rapid, only_defeat, only_win, get_pgn, get_fen) 
           
           
    def get_players_by_country(self, country_iso : str ) -> List[dict ]: 
        """ 
        Retrieves a list of players from a specific country.
        
        :param country_iso: Country ISO code (US, BR, CA. CN, etc.)
        :return: List of players from the specified country
        """
        return self.service.get_players_by_country(country_iso ) 
    
    def get_leaderboard(self) -> List[dict ]: 
        """ 
        Retrieves the Chess.com leaderboards.
        :return: Leaderboards.
        """
        return self.service.get_leaderboard() 
        
    def get_titled_players(self, title :str="GM") -> List[dict ] : 
        """ 
        Retrieves a list of titled players.
            
        :param title: Title of the players to retrieve (GM, IM, FM, WGM, WIM, WFM).
        :return List of titled players."""
        return self.service.get_titled_players(title)   
    
    def get_player_online_status(self, nick: str) -> str:
        """
        Retrieves the online status of a player.
        
        :param nick: Nickname of the player.
        :return: Dictionary containing the player's online status.
        """
        return self.service.get_player_online_status( nick) 

    def get_player_clubs(self, nick: str) -> List[dict]:
        """
        Retrieves a list of clubs a player is associated with.
        
        :param nick: Nickname of the player.
        :return: List of dictionaries representing player's clubs.
        """
        return self.service.get_player_clubs(nick) 

    def get_player_tournaments(self, nick: str) -> List[dict]:
        """
        Retrieves a list of tournaments a player has participated in.
        
        :param nick: Nickname of the player.
        :return: List of dictionaries representing player's tournaments.
        """
        return self.service.get_player_tournaments( nick) 

    def get_player_team_matches(self, nick: str) -> List[dict]:
        """
        Retrieves a list of team matches a player has participated in.
        
        :param nick: Nickname of the player.
        :return: List of dictionaries representing player's team matches.
        """
        return self.service.get_player_team_matches( nick) 


    def get_player_recent_content(self, nick : str,  pages: int) -> List[dict]:
        """
        Retrieves recent content from Chess.com.

        :param pages: Number of pages to retrieve.
        :return: List of recent content.
        """
        return self.service.get_player_recent_content(nick,  pages)
    

        
        

    
