# Coded by Shawn de Jesus

import base64
import datetime
from urllib.parse import urlencode
import json
import requests


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        # Returns a base64 encoded string
        client_id = self.client_id
        client_secret = self.client_secret

        if client_secret == None or client_id == None:
            raise Exception("client_id and client_secret missing")

        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Authentication failed.")
            # technically ends up false

        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # in seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)

        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def base_search(self, query_params):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)

        if r.status_code not in range(200, 299):
            return {}
        return r.text

    # Main Search Function
    def search(self, query=None, operator=None, operator_query=None, market=None, search_type='track'):
        if query == None:
            raise Exception("Query missing")

        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])

        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        if market == None:
            query_params = urlencode(
                {"q": query, "type": search_type.lower(), "limit": "1"})
        else:
            query_params = urlencode(
                {"q": query, "type": search_type.lower(), "limit": "1", 'market': market})
        # print(query_params)
        return self.base_search(query_params)

    # Get Audio Features json data using track ID as argument
    # Requires use of get_TrackID for "id" argument
    def get_audioFeat(self, id):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/audio-features"
        lookup_url = f"{endpoint}/{id}"
        r = requests.get(lookup_url, headers=headers)

        if r.status_code not in range(200, 299):
            return {}
        return r.text

    # Gets track image url
    # Just give it Song name for query
    def get_image(self, query=None):
        data = self.search(query=query, search_type='track')
        jdata = json.loads(data)
        return jdata["tracks"]["items"][0]["album"]["images"][1]["url"]

    # Gets track song url
    # Just give it Song name for query
    def get_Song(self, query=None):
        data = self.search(query=query, search_type='track')
        jdata = json.loads(data)
        return jdata["tracks"]["items"][0]["external_urls"]["spotify"]

    # Gets track ID
    # Just give it Song name for query
    def get_trackID(self, query=None):
        data = self.search(query=query, search_type='track')
        jdata = json.loads(data)
        return jdata["tracks"]["items"][0]["id"]

    def get_podcastURL(self, query=None, market="US", type="show"):
        data = self.search(query=query, market=market, search_type=type)
        jdata = json.loads(data)
        return jdata["shows"]["items"][0]["external_urls"]["spotify"]

    def get_podcastImage(self, query=None, market="US", type="show"):
        data = self.search(query=query, market=market, search_type=type)
        jdata = json.loads(data)
        return jdata["shows"]["items"][0]["images"][1]["url"]

    def get_podcastEpCount(self, query=None, market="US", type="show"):
        data = self.search(query=query, market=market, search_type=type)
        jdata = json.loads(data)
        return jdata["shows"]["items"][0]["total_episodes"]

    def get_podcastDesc(self, query=None, market="US", type="show"):
        data = self.search(query=query, market=market, search_type=type)
        jdata = json.loads(data)
        return jdata["shows"]["items"][0]["description"]


# Shawn's Client info for Spotify API account
client_id = '8b4b0c15be434dcb8ce52f4b557a3d19'
client_secret = 'a90c9e3b502f4c2089da0d0d93209240'

# TESTING AREA
"""
spotify = SpotifyAPI(client_id=client_id, client_secret=client_secret)
print(spotify.get_trackID("Car Crash eaJ"))
print(spotify.get_audioFeat(spotify.get_trackID("Car Crash eaJ")))

"""
"""
spotify = SpotifyAPI(client_id=client_id, client_secret=client_secret)
print(spotify.get_podcastDesc("waffle makers")) // description
print(spotify.get_podcastImage("waffle makers")) // image url
print(spotify.get_podcastURL("waffle makers"))  // link to actual podcast show
print(spotify.get_podcastEpCount("waffle makers")) // 48 
"""
