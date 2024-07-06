from chess import Chesster
from datetime import datetime
chess = Chesster() 
start =datetime(2024, 6,23)
end = datetime(2024, 12, 31)
print(chess.match.get_daily_puzzle(start,end))