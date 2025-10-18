from bs4 import BeautifulSoup ,XMLParsedAsHTMLWarning
import warnings
import requests
from pdfminer.high_level import extract_text as pdf_extract_text
from io import IOBase

warnings.filterwarnings("ignore",category=XMLParsedAsHTMLWarning)
def extract_text_from_url(url :str):
    try:
        response = requests.get(url,timeout=(5,15),headers={"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"})
        response.raise_for_status()

    except Exception as e:
        print(f"Error in fetching the URL:{url} , error:{e} ")
        return None
       
    content_type = response.headers.get("Content-Type", "").lower() # To know the content type of scraped data so that we can diffrentiate the method of parcing diffrent types.
    
    #Handle PDF
    if "application/pdf" in content_type and url.endswith(".pdf"):
        try:
            pdf_text =pdf_extract_text(IOBase(response.content))
            return {
                "url": url,
                "title": url.split("/")[-1],#last name afer "/"
                "content": pdf_text.strip() if pdf_text else "No text extracted",
            }
        except Exception as e:
            print(f"Error in fetching this pdf of url : {url} error is {e}")
            return None



