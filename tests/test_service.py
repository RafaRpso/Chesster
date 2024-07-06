import unittest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
import asyncio
from chesster.src.service import Service

class TestService(unittest.TestCase):

    def setUp(self):
        self.service = Service()

    def test_get_daily_puzzle_random(self):
        self.service.RequestManager.http = MagicMock(return_value='random puzzle data')
        result = self.service.Match().get_daily_puzzle(random=True)
        self.assertEqual(result, 'random puzzle data')
        self.service.RequestManager.http.assert_called_once_with('puzzle/random')

    def test_get_daily_puzzle(self):
        self.service.RequestManager.http = MagicMock(return_value='daily puzzle data')
        result = self.service.Match().get_daily_puzzle(random=False)
        self.assertEqual(result, 'daily puzzle data')
        self.service.RequestManager.http.assert_called_once_with('puzzle')

    def test_get_daily_puzzle_archived(self):
        mock_start_date = datetime(2024, 7, 1)
        mock_end_date = datetime(2024, 7, 5)
        expected_url = f'puzzles/daily?start=2024-7-1&end=2024-7-5'
        
        self.service.RequestManager.http = MagicMock(return_value='archived puzzle data')
        result = self.service.Match().get_daily_puzzle_archived(mock_start_date, mock_end_date)
        
        self.assertEqual(result, 'archived puzzle data')
        self.service.RequestManager.http.assert_called_once_with(expected_url, default=False)

    def test_get_match_with_pgn(self):
        mock_response_json = {'game': {'pgnHeaders': {'Date': '2024.07.01'}, 'pgnHeaders': {'White': 'Player'}}}
        self.service.RequestManager.http = MagicMock(return_value=mock_response_json)
        
        result = self.service.Match().get_match('mock_url', pgn=True)
        self.assertIn('game', result)
        self.service.RequestManager.http.assert_called_once_with('live/game/mock_url', default=False)

    async def test_get_player_games_archived(self):
        mock_start_date = datetime(2024, 7, 1)
        mock_end_date = datetime(2024, 7, 5)
        mock_nick = 'mock_nick'

        mock_session = MagicMock()
        mock_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value={'archives': ['mock_game_url']})

        self.service.Utils.extract_date_from_url_games_by_date = MagicMock(return_value={'year': 2024, 'month': 7})
        self.service.fetch_game_data = AsyncMock(return_value={'games': [{'time_class': 'blitz', 'url': 'mock_game_url'}]})

        result = await self.service.Player().get_player_games_archived(
            mock_nick, start_date=mock_start_date, end_date=mock_end_date, only_blitz=True, get_pgn=False, get_fen=False
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['url'], 'mock_game_url')

if __name__ == '__main__':
    unittest.main()
