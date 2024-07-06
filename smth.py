from chesster.chess import Chesster
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')

chess = Chesster() 
# The line `print("2: GET PLAYER GAMES ARCHIVED",
# chess.player.get_player_games_archived('doaskatharsis', start, end))` is calling
# a method `get_player_games_archived` from the `player` module of the `Chesster`
# class instance `chess`.
start =datetime(202, 6,23)
end = datetime(2024, 12, 31)


print("...TESTE ENDPOINTS...")
print("[MATCH]")
# print("1: GET DAILY PUZZLE \n", chess.match.get_daily_puzzle())
# print("2: GET DAILY PUZZLE ARCHIVED \n", chess.match.get_daily_puzzle_archived(start, end))
# print("3: GET MATCH \n", chess.match.get_match('https://www.chess.com/game/live/107464295324'))


print("[PLAYER]")
# print("1: GET DATA FROM PLAYER", chess.player.get_player('doaskatharsis'))
# print("2: GET PLAYER GAMES ARCHIVED", chess.player.get_player_games_archived('doaskatharsis', start, end))
# print("3: GET PLAYERS BY COUNTRY", chess.player.get_players_by_country('BR'))
# print("4: GET LEADERBOARD", chess.player.get_leaderboard())
# print("5: GET GM PLAYERS", chess.player.get_titled_players('GM')) 
# print("6: GET IM PLAYERS", chess.player.get_titled_players('IM'))
# print("7: GET ONLINE PLAYER", chess.player.get_player_online_status('doaskatharsis'))
# print("8: GET PLAYER RECENT CONTENT", chess.player.get_player_recent_content('Hikaru', 5))
