from fastapi import FastAPI, Request, Query, status, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Annotated
import os, random, string, time, json
import requests




from resource_scraper import Resources
from gpt import GalaxyGPTModel
from cloudinary_conf import cloudinary

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

resource_obj = Resources(apikey=os.getenv("SERP_API_KEY2"))
gpt_obj = GalaxyGPTModel(apikey=os.getenv("OPEN_AI_SECRET_KEY"))
hard_coded_apod = {'title': 'Plane, Clouds, Moon, Spots, Sun', 
                    'explanation': "What's that in front of the Sun?  The closest object is an airplane, visible just below the Sun's center and caught purely by chance.  Next out are numerous clouds in Earth's atmosphere, creating a series of darkened horizontal streaks. Farther out is Earth's Moon, seen as the large dark circular bite on the upper right. Just above the airplane and just below the Sun's surface are sunspots. The main sunspot group captured here, AR 2192, was in 2014 one of the largest ever recorded and had been crackling and bursting with flares since it came around the edge of the Sun a week before. This show of solar silhouettes was unfortunately short-lived.  Within a few seconds the plane flew away. Within a few minutes the clouds drifted off. Within a few hours the partial solar eclipse of the Sun by the Moon was over. Fortunately, when it comes to the Sun, even unexpected  alignments are surprisingly frequent. Perhaps one will be imaged this Saturday when a new partial solar eclipse will be visible from much of North and South America.    APOD editor to speak: in Houghton, Michigan on Thursday, October 12 at 6 pm", 
                    'url': 'https://apod.nasa.gov/apod/image/2310/PlaneEclipse_Slifer_1756.jpg'
                }

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    #logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time)
    response.headers["X-Process-Time"] = str(process_time)
    #formatted_process_time = '{0:.2f}'.format(process_time)
    #logger.info("returning response")
    return response


@app.get("/q/question")
async def ask_question(question: Annotated[str, Query(max_length=101)] = None):
    gpt_resp = await gpt_obj.gpt_question(question=question)

    pdf_resources = await resource_obj.google_get_resources_pdf(query=question)
    video_resources = await resource_obj.google_get_resources_videos(query=question)

    response_object = {
        "texts": gpt_resp["content"], 
        "pdfs": pdf_resources,
        "videos": video_resources
    }

    return JSONResponse(content=response_object, status_code=status.HTTP_200_OK)


@app.get("/{questionId}/question", response_description="get the response for a particular domain specific question using it's static id")
async def domain_specific_questions(questionId: int):

    dsq_map = {
        1: "astronomy picture of the day",
        2: "dataset of earthquakes since 1995",
        3: "plot magnitude of earthquakes since 1995", 
        4: "make a timeseries plot of earthquakes since 1995 based on their longitude and latitude", 
        5: "make a scatter plot of earthquakes since 1995 based on longitude and latitude",
    }

    dsq_assets = {
        1: "https://apod.nasa.gov/apod/image/2310/PlaneEclipse_Slifer_1756.jpg", 
        2: "",
        3: "https://res.cloudinary.com/dgkdru5it/image/upload/v1696760559/z2btcrsgupb4ak2bldi3.png",
        4: "https://res.cloudinary.com/dgkdru5it/image/upload/v1696760539/btpz7j3hxhwz4ufhwmaj.png",
        5: "https://res.cloudinary.com/dgkdru5it/image/upload/v1696760527/tixmovnjvsifywtey318.png"
    }

    if questionId == 1:
        try:
            data = await getAPOD()
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content=hard_coded_apod, status_code=status.HTTP_200_OK)
    elif questionId == 2:
        pass
    elif questionId == 3:
        time.sleep(1)
        resp = {
            "title": "Plot of Earthquakes and their magnitudes since 1995",
            "explanation": "The image represents a plot of earthquakes, their occurences as well as their magnitudes since the year 1995. The graph is plotted with the magnitude on the x-axis and frequency on the y-axis", 
            "url": dsq_assets[3]
        }
        return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
    elif questionId == 4:
        time.sleep(1)
        resp = {
            "title": "Timeseries plot of earthquakes since 1995 based on their longitude and latitude",
            "explanation": "The graph represents a time series representation of earthquake occurences based on their date and magnitude. A time series is a sequence of data points or observations collected, recorded, or measured at successive points in time, typically at evenly spaced intervals.", 
            "url": dsq_assets[4]
        }
        return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
    elif questionId == 5:
        time.sleep(1)
        resp = {
            "title": "Scatter plot of earthquakes since 1995 based on longitude and latitude",
            "explanation": "This image represents a graphical depiction of earthquake occurences since 1995. The graph is plotted based on the longitude and latitude of each earthquake occurence.", 
            "url": dsq_assets[5]
        }
        return JSONResponse(content=resp, status_code=status.HTTP_200_OK)        


@app.get("/detect/landmark", response_description="detect a particular landmark")
async def detect_landmark( proof: Annotated[UploadFile, File()]):
    try:
        # Upload the file to Cloudinary
        upload_result = cloudinary.uploader.upload(proof.file)

        # You can access the Cloudinary URL for the uploaded file
        file_url = upload_result['secure_url']
    except Exception as err:
        pass

async def getAPOD():
    uri = f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_API_KEY')}"
    try:
        resp = requests.get(uri)

        obj = resp.json()
        return {
            "title": obj["title"], 
            "explanation": obj["explanation"],
            "url": obj["hdurl"]
        }

    except Exception as err:
        uri = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

        try:
            obj = resp.json()
            return {
                "title": obj["title"], 
                "explanation": obj["explanation"],
                "url": obj["hdurl"]
            }
        except Exception as err:
            raise "error fetching astronomy pic"



