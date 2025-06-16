from dotenv import load_dotenv
import requests
import os


# ------------ #

load_dotenv()

API_KEY = os.getenv('AK')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": API_KEY
}


# ------------ #

class LolConnection:

    def __init__(self):

        self.url_tops = ''
        self.url_region_status = ''
        self.url_summoner = ''
        self.top_data = None
        self.region_data = None


    def get_urls(self, region, tier, queue, division):

        self.url_tops = f'https://{region.lower()}.api.riotgames.com/lol/league-exp/v4/entries/{queue}/{tier}/{division}?page=1'
        self.url_region_status = f'https://{region.lower()}.api.riotgames.com/lol/status/v4/platform-data'


    def get_data(self):

        response_top = requests.get(self.url_tops, headers=HEADERS)
        response_top.raise_for_status()
        response_top = response_top.json()
        self.top_data = response_top[:10]

        response_region = requests.get(self.url_region_status, headers=HEADERS)
        response_region.raise_for_status()
        self.region_data = response_region.json()


class LolPlayer:

    def __init__(self, region, puuid, leaguepoints, wins, losses):

        self.region = region
        self.puuid = puuid
        self.profileIconUrl = None
        self.gameName = None
        self.tagline = None
        self.summonerLevel = None
        self.leaguePoints = leaguepoints
        self.wins = wins
        self.losses = losses


    def get_player_info(self, version):

        response_id = requests.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{self.puuid}', headers=HEADERS)
        response_id.raise_for_status()
        response_id = response_id.json()
        self.gameName = response_id['gameName']
        self.tagline = response_id['tagLine']

        response_more = requests.get(f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.puuid}', headers=HEADERS)
        response_more.raise_for_status()
        response_more = response_more.json()
        profileIconId = response_more['profileIconId']
        self.profileIconUrl = f'https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{profileIconId}.png'
        self.summonerLevel = response_more['summonerLevel']


