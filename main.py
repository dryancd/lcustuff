import requests as rq
import datetime, time
import base64
import lcu_connector_python as lcu
import os, json


class BaseLCU(object):
    def __init__(self):
        self._local = lcu.connect()
        self.token = base64.b64encode(f'riot:{self._local["authorization"]}'.encode()).decode()
        self.url = "https://" + self._local['url']
        self.headers = {'Authorization': f"Basic {self.token}", 'Accept': 'application/json'}
        self.session = rq.Session()
        self.session.verify = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'riotgames.pem')
        self.session.headers = self.headers
        # self.check_perm_file()

    def check_perm_file(self):
        perm_path = os.path.dirname(os.path.abspath(__file__)), 'riotgames.pem'
        return perm_path

    def check_200(self, path, method: str, _bool: bool = False, payload=None):
        request_data = self.session.request(method, path, data=payload)

        if request_data.status_code in [200, 204]:
            if _bool is True:
                return True
            return request_data

        raise RuntimeError


class Lobby(BaseLCU):
    def __init__(self):
        super().__init__()

    def create_lobby(self, queue_type: int = 400):
        path = self.url + "/lol-lobby/v2/lobby"
        payload = {
            "queueId": queue_type
        }
        return self.check_200(path, 'POST', _bool=False, payload=json.dumps(payload))

    def create_custom(self, queue_type: int = 400):
        path = self.url + "/lol-lobby/v2/lobby"
        payload = {
            "customGameLobby": {
                "configuration": {
                    "gameMode": "CLASSIC", "gameMutator": "", "gameServerRegion": "", "mapId": 11,
                    "mutators": {"id": 1}, "spectatorPolicy": "AllAllowed", "teamSize": 5
                },
                "lobbyName": "bot lobby",
                "lobbyPassword": "4r634556342"
            },
            "isCustom": "true"
        }
        self.check_200(path, 'POST', _bool=False, payload=json.dumps(payload))
        self.add_bots()

    def create_custom_practice(self, queue_type: int = 400):
        path = self.url + "/lol-lobby/v2/lobby"
        payload ={
            "customGameLobby": {
                "configuration": {
			        "gameMode": 'PRACTICETOOL',
			        "gameMutator": [ ""],
			        "mapId": 11,
			        "mutators": {
				        "id": 1
			        },
			        "spectatorPolicy": 'NotAllowed',
			        "teamSize": 5
		        },
		        "lobbyName": 'Practice Tool',
		        "lobbyPassword": "null"
	        },
	        "isCustom": "true"
            }
        self.check_200(path, 'POST', _bool=False, payload=json.dumps(payload))
        self.add_bots()

    def add_bots(self):
        path = self.url + "/lol-lobby/v1/lobby/custom/bots"
        #ids = [63,115,45,25,99]
        ids = [63,143,54,51,86]
        for id in ids:
            payload = {
                "botDifficulty": "MEDIUM",
                "championId": id,
                "teamId": "200"
            }
            self.check_200(path, 'POST', _bool=False, payload=json.dumps(payload))
        return


class MatchMaking(BaseLCU):
    def __init__(self):
        super().__init__()

    def ready_check(self):
        """
        Check to see if lobby is in queue and ready to accept match
        """
        path = self.url + '/lol-matchmaking/v1/ready-check'
        return self.check_200(path, 'GET')

    def decline_match(self):
        """
        Accept match found
        """
lobby = Lobby()
lobby.create_custom()