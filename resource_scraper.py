from serpapi.google_search import GoogleSearch
import os
import requests
from dotenv import load_dotenv


load_dotenv()

DEFAULT_USER_AGENT = "('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')"


class Resources():
  
    def __init__(self, apikey:str, engine: str = "google") -> None:
        self.apikey = apikey
        self.engine = engine

    async def google_get_resources_pdf(self, query: str):

        params = {
        "api_key": self.apikey, 
        "engine": "google",
        "q": f"{query}:pdf",
        "hl": "en",
        "num": 5
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        resp_result = []

        for _, result in enumerate(results['organic_results']):
            if '.pdf' or '.docx' or '.epub' in result['link']:
                resp_obj = {
                    "title": result["title"],
                    "link": result["link"],
                }
                resp_result.append(resp_obj)
            else: pass
        return resp_result

    async def google_get_resources_videos(self, query: str) -> dict:
        params = {
            "api_key": self.apikey, 
            "engine": "google",
            "q": f"site:www.youtube.com {query}",
            "hl": "en",
            "num": 5
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        resp_result = []

        try:
            for _, result in enumerate(results["inline_videos"]):
                resp_obj = {
                    "title": result["title"],
                    "link": result["link"],
                    "thumbnail": result["thumbnail"]
                }
                resp_result.append(resp_obj)
            return resp_result
        except Exception as err:
            pass

        try:
            for _, result in enumerate(results["organic_results"]):
                resp_obj = {
                    "title": result["title"],
                    "link": result["link"],
                    "thumbnail": result["thumbnail"]
                }
                resp_result.append(resp_obj)
            return resp_result
        except Exception as err:
            pass

        return resp_result

    def save_pdf(self, url, filename):

        headers = {"User-Agent": DEFAULT_USER_AGENT}

        pdf = requests.get(url=url, headers=headers)

        with open(filename, 'wb') as resource:
            resource.write(pdf.content)

        return filename


"""
r = Resources(apikey=os.getenv("SERP_API_KEY"))

r.google_get_resources_pdf(query="what is a schist and what are some properties of this rock type.")
r.google_get_resources_videos(query="what is a schist and what are some properties of this rock type.")

"""