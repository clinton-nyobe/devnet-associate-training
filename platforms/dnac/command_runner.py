import requests
import json
import authentication
import utils
import time

from datetime import datetime, timezone


DNAC_PARAMETERS = utils.get_dnac_env_variables()

def get_accepted_remote_commands(dnac_host:str, auth_token:str) -> list:
    """Function to get the list of valid read-only commands 

    Args:
        dnac_host (str): _description_
        auth_token (str): _description_
    """

    try:
        # Endpoint URL
        endpoint = "/dna/intent/api/v1/network-device-poller/cli/legit-reads"
        url = f"https://{dnac_host}{endpoint}"

        # Headers
        headers = {"x-auth-token": auth_token}

        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            print("Successfully pulled the list of read only commands")
            print(f"{response.json()["response"]}")
        
        else:
            print(f"Failed to get the commands from DNA-Center: {e}")
            return []
    
    except Exception as e:
        print(f"Failed to get the commands from DNA-Center: {e}")
        exit(1)
    

def send_remote_command(dnac_host:str, auth_token:str, commands:list, name:str, device_uuids:list) -> dict:
    """Function to send a read-only command to a device on DNAC

    Args:
        dnac_host (str): the domain name of the DNAC instance
        auth_token (str): the authentication
        commands (list): the list of the commands to send
        name (str): the name of the set of commands that we want to send
        device_uuids (list): the list of UUIDS of the target devices

    Returns:
        dict: a response dict in JSON format containing :
        {
            "taskId": <string>,
            "url": "<enpoint to task>
        }
    """
    try:
        # Endpoint URL
        endpoint = "/dna/intent/api/v1/network-device-poller/cli/read-request"
        url = f"https://{dnac_host}{endpoint}"

        # Headers
        headers = {
                    "x-auth-token": auth_token,
                    "Content-Type": "application/json"      
                  }

        # Body
        payload = {
            "name" : name,
            "commands" : commands,
            "deviceUuids" : device_uuids
        }

        response = requests.post(url=url, headers=headers, json=payload, verify=False)
        if response.status_code == 202: #
            print(f"Successfully launched the commands {commands} on devices {device_uuids}")
            print(f"{response.json()["response"]}")
            return response.json()["response"]

        
        else:
            print(f"Failed to launch the commands {commands} to devices {device_uuids} DNA-Center: {response.status_code} - {response.text}")
            return {}
    
    except Exception as e:
        print(f"Failed to launch the commands {commands} to devices {device_uuids} to DNA-Center: {e}")
        exit(1)

def monitor_task_completion(dnac_host:str, auth_token:str, taskId:str) -> dict :
    """To get the status of a task 

    Args:
        dnac_host (str): the domain name of the DNAC instance
        auth_token (str): the authentication token
        taskId (str): the task ID corresponding to a command launched before

    Returns:
        dict: a dictionnary corresponding to the response
         {
            "version": 1741036321004,
            "endTime": 1741036321004,
            "startTime": 1741036320777,
            "progress": "{\"fileId\":\"80a5c9c7-f023-4bc8-8ca3-650115a9210f\"}",
            "serviceType": "Command Runner Service",
            "username": "devnetuser",
            "lastUpdate": 1741036321004,
            "isError": false,
            "instanceTenantId": "6696f018a04cae65c3c37afb",
            "id": "4133a2eb-1473-4866-a3a8-d9b6f562c9db"
        }
    """
    
    try:
        # Endpoint URL
        endpoint = f"/dna/intent/api/v1/task/{taskId}"
        url = f"https://{dnac_host}{endpoint}"

        # Headers
        headers = {
                    "x-auth-token": auth_token,
                    "Content-Type": "application/json"      
                  }

        response = requests.get(url=url, headers=headers,verify=False)
        if response.status_code == 200: #
            print(f"Successfully got task with task ID {taskId}")
            response = response.json()["response"]

            # Convert timestamps into human readable
            for key, value in response.items():
                if isinstance(value, int) and len(str(value)) >= 13:  # Check if it's a timestamp
                    response[key] = datetime.fromtimestamp(value / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

            print(response)
            return response

        else:
            print(f"Failed get task with task ID {taskId}: {response.status_code} - {response.text}")
            return {}

    except Exception as e:
        print(f"Failed to get task with task ID {taskId}: {e}")
        exit(1)

def obtain_task_results(dnac_host:str, auth_token:str, fileId:str) -> list:
    """To obtain the result of a task 

    Args:
        dnac_host (str): the domain name of the DNAC instance
        auth_token (str): the authentication token
        fileId (str): the file ID corresponding to the result of a task 

    Returns:
        list: a list containing the result of the task

    """
    try:
        # Endpoint URL
        endpoint = f"/dna/intent/api/v1/file/{fileId}"
        url = f"https://{dnac_host}{endpoint}"

        # Headers
        headers = {
                    "x-auth-token": auth_token,
                    "Content-Type": "application/json"      
                  }

        response = requests.get(url=url, headers=headers,verify=False)
        if response.status_code == 200: #
            print(f"Successfully got task results corresponding to fileID: {fileId}")
            response = response.json()
            # pprint.pprint(response)
            return response

        else:
            print(f"Failed get task results with corresponding to fileID {fileId}: {response.status_code} - {response.text}")
            return {}

    except Exception as e:
        print(f"Failed get task results with corresponding to fileID {fileId}: {e}")
        exit(1)


def execute_command(dnac_host:str, auth_token:str, commands:list, name:str, device_uuids:list) -> bool:
    """To get the status of a task 

    Args:
        dnac_host (str): the domain name of the DNAC instance
        auth_token (str): the authentication token
        taskId (str): the task ID corresponding to a command launched before

    Returns:
        bool : True if the commands are successful and false otherwise
    """

    # Send the command
    response = send_remote_command(
        dnac_host=dnac_host,
        auth_token=auth_token,
        name=name,
        commands=commands,
        device_uuids=device_uuids)
    
    if not response:
        return False
    
    taskId = response["taskId"]
    
    # Verify that the command has ended
    task_completed = False
    timeout = 50
    while not task_completed or timeout > 0:
        response = monitor_task_completion(dnac_host=dnac_host, auth_token=auth_token, taskId=taskId)
        if not response:
            exit(1)
        
        # Check the progress of the task
        progress_data = json.loads(response["progress"])
        file_id = progress_data.get("fileId", None)

        # The task has ended
        if file_id:
            break

        time.sleep(10)
        print(f"Waiting for task {taskId} to end...")
        timeout = timeout - 10

    print(file_id)
    
    # Get the result 
    # TODO: Format well the output of the commands
    response = obtain_task_results(dnac_host=DNAC_PARAMETERS["host"], auth_token=auth_token, fileId=file_id)
    for result in response:
        if result["commandResponses"]["BLACKLISTED"] or result["commandResponses"]["FAILURE"]:
            print("There are FAILED and/or BLACKLISTED command results, please check the output")
            exit(1)
        
        for key in result["commandResponses"]["SUCCESS"]:
            print(f"{key} : { result["commandResponses"]["SUCCESS"][key]}")
        
        return True


if __name__ == "__main__":
    auth_token = authentication.get_auth_token()
    response = execute_command(
        dnac_host=DNAC_PARAMETERS["host"],
        auth_token=auth_token,
        name="show run",
        commands=["show ver | inc Software", "show clock"],
        device_uuids=["f2ee94ae-c1f7-4114-9a00-a4348240204f"])
