from bs4 import BeautifulSoup ,XMLParsedAsHTMLWarning
import warnings
import requests
from pdfminer.high_level import extract_text as pdf_extract_text
from io import BytesIO

warnings.filterwarnings("ignore",category=XMLParsedAsHTMLWarning)
def extract_text_from_url(url :str):
    try:
        response = requests.get(url,timeout=(5,15),headers={"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"})
        response.raise_for_status()

    except Exception as e:
        print(f"Error in fetching the URL:{url} , error:{e} ")
        return None
       
    content_type = response.headers.get("Content-Type").lower() # To know the content type of scraped data so that we can diffrentiate the method of parcing diffrent types.
    
    # Handle PDF
    if "application/pdf" in content_type or url.endswith(".pdf"):
        try:
            pdf_text =pdf_extract_text(BytesIO(response.content))
            return {
                "url": url,
                "title": url.split("/")[-1],#last name afer "/"
                "content": pdf_text.strip() if pdf_text else "No text extracted",
            }
        except Exception as e:
            print(f"Error in fetching this pdf of url : {url} error is {e}")
            return None

    # Handle XML(sitemaps and RSS)
    elif "xml" in content_type or url.endswith(".xml") or url.endswith(".rss"):
        try:
            soup = BeautifulSoup(response.text,"xml")
        except Exception as e:
            print(f"fallback for HTML conten of {url}")
            soup = BeautifulSoup(response.text,"html.parser")
            
        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "No Title"
        )
        text = soup.get_text(separator=" " ,strip=True)
        return {"url" : url ,"title" : title,"content":text}
    # Handle HTML  
    elif "text/html" in content_type or url.endswith(".html"):
        try:
            soup = BeautifulSoup(response.text,"html.parser")
            
            title =(
                    soup.title.string.strip()
                    if soup.title or soup.title.string
                    else
                    "No Title")
            
            # cleaning the html
            for script in soup(["script","style","noscript"]):
                script.extract()
            
            text = soup.get_text(strip=True,separator=" ")
            
            if len(text) < 50 or not text:
                return None
            
            return {"url" : url ,"title" : title,"content":text}        
            
        except Exception as e:
            print(f"Error in HTML parsing the URL:{url} , error:{e} ")
            return None
        
    else:
            print(f"There is not proper Formate to scrap.")
            return None
      

    

