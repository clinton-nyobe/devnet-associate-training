import requests
import urllib3
import os 

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


# Load .env file from the path to the .env file
load_dotenv()
 
# Use this command to avoid having certificate warnings (since we don't enable SSL verification)
urllib3.disable_warnings()

# Use this function to get the environment variables
dnac_host = os.getenv("DNAC_HOST")
dnac_username = os.getenv("DNAC_USERNAME")
dnac_password = os.getenv("DNAC_PASSWORD")

def get_auth_token():
    """
    A function to get the authentication token
    """
    try:
        # Endpoint URL
        endpoint = "/dna/system/api/v1/auth/token"
        url = f"https://{dnac_host}{endpoint}"
        
        # Make the POST Request
        resp = requests.post(url, auth=HTTPBasicAuth(dnac_username, dnac_password), verify=False)
        
        # Retrieve the Token from the returned JSON
        token = resp.json().get('Token')
        
        # Print out the Token
        print(f"Token Retrieved: {token}")
    except Exception as e:
        print(f"Failed to get the token : {e}")
        exit(1)

    # Create a return statement to send the token back for later use
    return token

if __name__ == "__main__":
    get_auth_token()