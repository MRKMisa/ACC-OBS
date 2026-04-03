from obsws_python import ReqClient

import time, psutil



#Starting OBS
if not "obs64.exe" in (i.name() for i in psutil.process_iter()): #If OBS is not running
    print("Starting OBS")
    import imports.start_obs as start_obs
    
    start_obs.main()
    time.sleep(1)
print("OBS is open")

print("Connecting to OBS...")
pwd = 'AkE5MGKgeBRAF3ti' #OBS password
client = ReqClient(host='localhost', port=4455, password=pwd) #Connect to OBS with web socket
print("Connected to OBS")

status = client.get_record_status().output_active
    
print()