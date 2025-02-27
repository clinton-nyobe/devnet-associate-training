import urllib3
import os
from dotenv import load_dotenv


def get_dnac_env_variables():
    """
    Returns the parameters for a connection to DNAC, ensuring required variables are set.
    """
    load_dotenv()
    urllib3.disable_warnings()

    dnac_host = os.getenv("DNAC_HOST")
    dnac_username = os.getenv("DNAC_USERNAME")
    dnac_password = os.getenv("DNAC_PASSWORD")

    # Ensure all values are set
    if not all([dnac_host, dnac_username, dnac_password]):
        raise ValueError("Missing one or more DNAC environment variables!")

    return {"host": dnac_host, "username": dnac_username, "password": dnac_password}



if __name__ == "__main__":
    print(get_dnac_env_variables())