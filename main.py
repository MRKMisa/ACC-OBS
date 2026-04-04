from imports import get_shared_mem
from imports import read_data_from_shared_memory

from obsws_python import ReqClient
import psutil, datetime, time


global Config_settings
from imports import get_config_file, print_from_config_class
Config_settings = get_config_file()

print()
print("---Config settings---")
print_from_config_class(Config_settings)
print()


#Starting OBS
if not "obs64.exe" in (i.name() for i in psutil.process_iter()): #If OBS is not running
    print("Starting OBS...")
    from imports import start_obs, stop_recording_and_rename
    
    try:
        start_obs()
    except Exception as e:
        print("Can´t start OBS...")
        print(e)
        exit()
    time.sleep(1) #Wait till OBS starts
    
    if not "obs64.exe" in (i.name() for i in psutil.process_iter()): # If OBS isn´t running
        print("OBS isn´t still open...")
        max_wating_time_to_obs = 5 # in seconds
        
        print(f"Waiting to OBS open max {max_wating_time_to_obs}s...")
        start = time.time()
        while not "obs64.exe" in (i.name() for i in psutil.process_iter()):
            time.sleep(0.5)
            
            if time.time() > start+max_wating_time_to_obs:
                print(f"OBS did not start in {max_wating_time_to_obs}s...")
                print("Exiting script...")
                exit()



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
        stop_recording_and_rename(client)
    
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
            Config_settings = get_config_file()
            
        
        time.sleep(d)
        
if __name__ == "__main__":
    loop_delay = Config_settings.loop_delay
    
    run(loop_delay)