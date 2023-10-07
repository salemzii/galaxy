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

  def google_get_resources(self, query: str):

      params = {
        "api_key": self.apikey, 
        "engine": "google",
        "q": f"{query}:pdf",
        "hl": "en",
        "num": 20
      }

      search = GoogleSearch(params)
      results = search.get_dict()

      for index, result in enumerate(results['organic_results']):

        
        if '.pdf' or '.docx' or '.epub' in result['link']:
            print(result["link"])

            """
            pdf_file = result['link']

            filename = str(pdf_file).split("/")[-1]

            # save PDF
            try:  
                fl = self.save_pdf(pdf_file,  filename=filename)

            except Exception as e:print(e)
            print(f'Saving PDF №{index}..')      
            
            """
        else: pass


  def save_pdf(self, url, filename):

    headers = {"User-Agent": DEFAULT_USER_AGENT}

    pdf = requests.get(url=url, headers=headers)

    with open(filename, 'wb') as resource:
      resource.write(pdf.content)
    
    return filename


r = Resources(apikey=os.getenv("SERP_API_KEY"))

r.google_get_resources(query="site:www.academia.edu Fraudulent app detection using sentiment analysis")
