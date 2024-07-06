class Utils : 
    '''GET_USER_GAMES'''
    @staticmethod
    def extract_date_from_url_games_by_date(url:str) :
        return {'year': int(url.split('/')[-2]), 'month': int(url.split('/')[-1])}

