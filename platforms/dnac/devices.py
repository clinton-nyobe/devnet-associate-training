import requests

import authentication
import utils



# Use this function to get the environment variables
DNAC_PARAMETERS = utils.get_dnac_env_variables()

def get_network_devices(dnac_host:str, auth_token:str) -> list:
    """A function to return the list of all the devices in DNAC

    Args:
        dnac_host (dict): the domain name of the DNAC instance
        auth_token (str) : the authentication token

    Returns:
        list: the list of all the devices stored in the DNAC (without pagination) or empty list
    """

    try:
        # Endpoint URL
        endpoint = "/api/v1/network-device"
        url = f"https://{dnac_host}{endpoint}"


        # The header of the request
        headers = {
            "x-auth-token": auth_token 
        } 

        # The GET request
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            print("Request to get All Devices was successful")
            
            # Get the list of devices
            devices = response.json().get("response")
            return list(devices)

        else:
            print(f"Failed to get the Devices : {response.status_code} - {response.text}")
            return []
        
    
    except Exception as e:
        print(f"Failed to get the devices, unusual behaviour : {e}")
        exit(1)

def print_device_list(device_list:list):
    """Function to print the device list in a pretty way

    Args:
        device_list (list): The device list returned by the function get_network_devices()
    """
    # TODO: Use a correct table to display this information

    # Print the header
    print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
          format("hostname", "mgmt IP", "serial","platformId", "SW Version", "role", "Uptime"))
    
    for device in device_list:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]
        for (serialNumber, platformId) in serialPlatformList:
            print("{0:42}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(device['hostname'],
                         device['managementIpAddress'],
                         serialNumber,
                         platformId,
                         device['softwareVersion'],
                         device['role'], uptime))
    


    
# def get_network_device_by_ip()
    
    

if __name__ == "__main__":
    auth_token = authentication.get_auth_token()
    devices = get_network_devices(dnac_host=DNAC_PARAMETERS["host"], auth_token=auth_token)
    print_device_list(device_list=devices)
