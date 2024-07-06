# -*- coding: utf-8 -*-
from chesster.src.service import Service
from typing import List 
from datetime import datetime
class Match(): 
    
    
    def __init__(self, *args, **kwargs):
        self.service = Service.Match()
        
    def get_daily_puzzle(self, random: bool = False) -> List[dict]:
        """
        Retrieves the daily puzzle.
        
        :param random: If True, retrieves a random daily puzzle.
        :return: List of dictionaries representing the daily puzzle.
        """
        return self.service.get_daily_puzzle(random)

    def get_daily_puzzle_archived(self, start_date: datetime, end_date: datetime) -> List[dict]:
        """
        Retrieves archived daily puzzles within a specified date range.
        
        :param start_date: Start date (datetime object) for the archive query.
        :param end_date: End date (datetime object) for the archive query.
        :return: List of dictionaries representing archived daily puzzles.
        """
        return self.service.get_daily_puzzle_archived(start_date, end_date)

    def get_match(self, url: str, pgn: bool = False):
        """
        Retrieves details of a match based on its URL.
        
        :param url: URL of the match.
        :param pgn: If True, retrieves additional PGN details of the match.
        :return: Dictionary containing match details or PGN data if requested.
        """
        return self.service.get_match(url, pgn)
        
        

        