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
print()


print("Connecting to OBS...")
try:
    global client
    client = ReqClient(host='localhost', port=Config_settings.obs_port, password=Config_settings.obs_pwd) #Connect to OBS with web socket
except Exception as e:
    print("Can´t connect to OBS...")
    print(e)
    exit()
print("Connected to OBS.")
print()


def event(last_current_time, last_state):
    info = get_shared_mem()
    
    
    if info.graphics.status != 2: # If game is not live
        if info.graphics.status == 0:
            if last_state != 0:
                print("Game is not running..")
            time.sleep(0.5)
        elif info.graphics.status == 1:
            if last_state != 1:
                print("Game is in replay...")
            time.sleep(0.3)            
        elif info.graphics.status == 3:
            if last_state != 3:
                print("Game is pause...")
                        
        return False, None, info.graphics.status
    
    
    current_time = info.graphics.currentTime
    
    if last_current_time == None:
        return False, current_time, None
    
    return current_time < last_current_time, current_time, None #If lap started. Because curr time is set to 0:00.00 when lap stared but last time would be greather.

def main(client, Config_settings):
    status = client.get_record_status().output_active
    if status:
        stop_recording_and_rename(client)
    
    client.start_record()
    
    
def run():
    global Config_settings, client
    last_current_time = get_shared_mem().graphics.currentTime #Current AC or ACC time
    last_config_update = time.time()
    last_state = None
    loop = True
    
    
    while loop:
        b, last_current_time, last_state = event(last_current_time, last_state)
        if b:
            main(client, Config_settings)
            
        #Every 10s update config
        update_frequency = 10 #in seconds
        
        if time.time() > last_config_update+update_frequency:
            Config_settings = get_config_file(Config_settings)
            last_config_update = time.time()
            
        
        time.sleep(float(Config_settings.loop_delay))
        
if __name__ == "__main__":
    run()