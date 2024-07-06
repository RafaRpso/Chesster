# -*- coding: utf-8 -*- 
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import sys
sys.stdout.reconfigure(encoding='utf-8')
class RequestManager:
    
    @staticmethod
    def http(uri: str, headers: dict = None, default:bool=True):
        def get_url():
            return 'https://api.chess.com/pub/' + str(uri) if default else 'https://www.chess.com/callback/' + str(uri)

        url: str =  get_url()
        session = requests.Session()
        timeout = 60
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.1 Safari/537.36'
            }

        try:
            response = session.get(url=url, headers=headers, timeout=timeout)
            response.raise_for_status()  
            return response.json()  
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        finally:
            session.close()
