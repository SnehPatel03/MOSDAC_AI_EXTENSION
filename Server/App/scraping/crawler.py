from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0 Safari/537.36"
}



def is_valid_url(url : str , base_domain:str) -> bool:
    parsed = urlparse(url)    
    return parsed.scheme in ('http','https') and  base_domain in  parsed.netloc 
    
def crawl_url(base_url : str , max_pages: int = 200):
    print("Entered")
    visited = set() #unique collection of webpages
    to_visit = [base_url] # to be visited Urls
    base_domain = urlparse(base_url).netloc
    
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        
        if url in visited:  
            continue # if already in visited panel then skip it.
        
        #fetching of page
        try:
            response = requests.get(url , headers=HEADERS,timeout=(5,15))
            response.raise_for_status() # raise error with HTTP Code != 200
        except Exception as e:
            print(f"Error in fetching {url}: {e}")
            continue # if error then skip this url and go for another
        
        visited.add(url)
        soup = BeautifulSoup(response.text,"html.parser")
        
        for link in soup.find_all("a",href=True):
            new_url = urljoin(url,link["href"])
            if is_valid_url(new_url,base_domain) and new_url not in visited:
                to_visit.append(new_url)
                
    return list(visited)

if __name__ == "__main__":
    urls = crawl_url("https://mosdac.gov.in")
    print(f"Urls Found in this Website are : {len(urls)}")
    for u in urls:
        print(u)
        
    

