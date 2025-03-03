# 1. Obtain target device UUID
# 2. Initiate the remote commands 
# 3. Wait until task completes
# 4. Obtain the results

import authentication
import command_runner
import devices
import utils

DNAC_PARAMETERS = utils.get_dnac_env_variables()

if __name__ == "__main__":
    auth_token = authentication.get_auth_token()

    # 1. Obtain target device UUID
    device = devices.get_network_device_by_ip_address(auth_token=auth_token, dnac_host=DNAC_PARAMETERS["host"], ip_address="10.10.20.177")
    if device:
        print("DEVICE: ", device)
        device_uuid = device["instanceUuid"]
    else:
        exit(1)
    
    # 2. Initiate the remote commands 

    command_succeeded = command_runner.execute_command(
        dnac_host=DNAC_PARAMETERS["host"],
        auth_token=auth_token,
        device_uuids=[device_uuid],
        name="show ver",
        commands=["show version"]
        )
    
    if command_succeeded:
        print("The commands were successfully executed")
        exit(0)
    
    print("Something went wrong in the execution of the commands")

