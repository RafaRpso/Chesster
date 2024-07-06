from chesster.player import Player  
from chesster.match import Match

class Chesster:
    """
    Chesster is a class that initializes a chess match with a player and an extractor.

    Attributes:
        match (Match): An instance of the Match class, representing a chess match.
        player (Player): An instance of the Player class, representing a player in the chess match.
        extractor (Extractor): An instance of the Extractor class, used for extracting information.
    """

    def __init__(self) -> None:
        """
        Initializes the Chesster class by creating instances of Match, Player, and Extractor.
        """
        self.match = Match()
        self.player = Player()