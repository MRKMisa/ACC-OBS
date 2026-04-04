from imports.get_shared_mem import get_shared_mem
from imports.get_extended_shared_mem import read_data_from_shared_memory

from obsws_python import ReqClient
import psutil, datetime
import time

    
global Config_settings
from imports import config
Config_settings = config.get_config_file()


#Starting OBS
if not "obs64.exe" in (i.name() for i in psutil.process_iter()): #If OBS is not running
    print("Starting OBS...")
    import imports.obs as obs
    
    try:
        obs.start_obs()
    except Exception as e:
        print("Can´t start OBS...")
        print(e)
        exit()
    time.sleep(1)
print("OBS is open.")

print("Connecting to OBS...")
try:
    client = ReqClient(host='localhost', port=Config_settings.obs_port, password=Config_settings.obs_pwd) #Connect to OBS with web socket
except Exception as e:
    print("Can´t connect to OBS...")
    print(e)
    exit()
print("Connected to OBS")



last_current_time = get_shared_mem().graphics.currentTime #Current ACC time
def event(last_current_time):
    info = get_shared_mem()
    
    current_time = info.graphics.currentTime
    
    return current_time < last_current_time #If lap started. Because curr time is set to 0:00.00 when lap stared but last time would be greather.

def main():
    status = client.get_record_status().output_active
    if status:
        obs.stop_recording_and_rename(client)
    
    client.start_record()
    
    
def run(d=0.01):
    global Config_settings
    loop = True
    
    while loop:
        if event():
            main()
            
        #Every 10s update config
        now = datetime.datetime.now()
        if [*str(now.second)][1] == "0":
            Config_settings = config.get_config_file()
            
        
        time.sleep(d)
        
if __name__ == "__main__":
    delay = Config_settings.delay
    
    run(delay)