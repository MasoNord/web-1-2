import requests

from harmony_hound.main.config import load_rapid_api_config


class RecognitionService:
    def recognise_song(self, google_web_view_link: str):
        """
        The method which recognises songs by Google Drive url
        The recognition process is performed by Shazam Song Recognition API
        From RapidAPI website
        :param google_web_view_link: str
        :return:
        """

        rapid_api_config = load_rapid_api_config()

        url = "https://shazam-song-recognition-api.p.rapidapi.com/recognize/url"

        querystring = {"url": google_web_view_link}

        headers = {
            "x-rapidapi-key": rapid_api_config.rapid_api_key,
            "x-rapidapi-host": rapid_api_config.rapid_api_host
        }

        response = requests.get(url, headers=headers, params=querystring)

        return response.json()