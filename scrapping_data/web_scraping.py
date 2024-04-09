import requests
from bs4 import BeautifulSoup

def get_webpage_data(url, usn=None, email=None, pwd=None):
 
    # Send an HTTP request to the URL
    response = requests.get(url)

    status = response.status_code

    print(response.status_code)
  
    if status == 200:
        pass

    elif status == 403:

        if usn is not None or email is not None:
            response = webpage_login(url, usn, email, pwd)
            if response is not None:
                pass
            else:
                print("The request was denied."); return
        
        else: return

    else:
        print("The request was denied."); return

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, "html.parser")
    print("1")


def webpage_login(url, usn, email, pwd):

    # Create a session to persist cookies
    session = requests.Session()

    login_data = {
        "username": usn,
        "email": email,
        "password": pwd
    }
    login_data = {k:v for k,v in login_data.items() if v is not None}
    login_response = session.post(url, data=login_data)

    if login_response.status_code == 200:
        return session.get(url)
    
    else:
        return None
        
    
if __name__=="__main__":
    
    # url = "https://www.vesselfinder.com/vessels/details/9580390"
    # email = "theolyber@gmail.com"
    # pwd = "theo123!@#"

    url = "https://www.marinetraffic.com/en/ais/details/ships/shipid:760998/mmsi:538009898/imo:9580390/vessel:SEAWAYS_EAGLE"

    get_webpage_data(url)  # None, email, pwd