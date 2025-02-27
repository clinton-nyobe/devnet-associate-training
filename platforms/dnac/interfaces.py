import requests

import authentication
import utils

DNAC_PARAMETERS = utils.get_dnac_env_variables()


def get_interfaces_on_device(dnac_host:str, auth_token:str, device_id:str) -> list:
    """ Function to get all the interfaces on a device
    Args:
        dnac_host (str): the domain name of DNAC instance
        auth_token (str): the authentication token
        device_id (int): the ID of the device on which we want to get interfaces

    Returns:
        list: the list of interfaces
    """
    try:
        # Endpoint URL
        endpoint = "/api/v1/interface"
        url = f"https://{dnac_host}{endpoint}"

        # Headers
        headers = {"x-auth-token": auth_token}

        # Build the query parameters
        query_params = {"deviceId": device_id}

        # Perform the GET Request
        response = requests.get(url=url, headers=headers, params=query_params, verify=False)
        if response.status_code == 200:
            print(f"Successfully got the interface for the device ID {device_id}")
            return list(response.json()["response"])

        else:
            print(f"Failed to get interfaces of device with ID {device_id}")
            print(f"{response.status_code} - {response.text}")
            return []
        
    except Exception as e:
        print(f"Failed to get interfaces of device with ID {device_id}: {e}")
        exit(1)

def print_interface_info(interfaces:list):
    """Function to print interfaces details

    Args:
        interfaces (list): A list of interfaces returned by the function get_interfaces_on_device()
    """
    print("{0:42}{1:17}{2:12}{3:18}{4:17}{5:10}{6:15}".
          format("portName", "vlanId", "portMode", "portType", "duplex", "status", "lastUpdated"))
    for int in interfaces:
        print("{0:42}{1:10}{2:12}{3:18}{4:17}{5:10}{6:15}".
              format(str(int['portName']),
                     str(int['vlanId']),
                     str(int['portMode']),
                     str(int['portType']),
                     str(int['duplex']),
                     str(int['status']),
                     str(int['lastUpdated'])))



if __name__ == "__main__":
    auth_token = authentication.get_auth_token()
    interfaces = get_interfaces_on_device(dnac_host=DNAC_PARAMETERS["host"], auth_token=auth_token, device_id="04591e4f-de5e-4683-8b89-cb5dc5699df2")
    print_interface_info(interfaces)