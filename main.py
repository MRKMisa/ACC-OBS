from imports import get_shared_mem
from imports import read_data_from_shared_memory

from obsws_python import ReqClient
import psutil, datetime, time

from imports import stop_recording_and_rename, check_recording_matching, start_recording, check_OBS_ready


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
    from imports import start_obs
    
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

print("Checking if OBS is ready...")
if not check_OBS_ready(client): exit()
print("OBS is ready to use.")



def event(last_state): # return if OBS should be recording
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
            time.sleep(0.1)
                
        return False, info.graphics.status # Return that OBS should not be recording


    if last_state != 2:
        print("Game is running...")
            
    
                        
        
    
    
    current_time = info.graphics.iCurrentTime # Get AC or ACC time i in front mean in miliseconds. So it not 0:00.123 but 123. It´s better working with.
    
    if current_time == "-:--.---": # AC or ACC will return this time when session doesn´t started yet. If ses does not stared we dont want to recording.
        return False, info.graphics.status # So we will return False
    elif not (current_time).isdigit(): # Just test. Because I dont know what will actually game return.
        print(f"Not digit - {current_time}")
        return False, info.graphics.status
    
    return True, info.graphics.status # There we can just return True because here we want to recording.





def run():
    global Config_settings, client
    last_config_update = time.time()
    last_state = None
    loop = True
    
    recording = False
    
    
    while loop:
        b, last_state = event(last_state)
        if b:
           if not recording:
                start_recording()
                
        else:
            if recording:
                stop_recording_and_rename(client, Config_settings)



        #Every 10s update config
        update_frequency = 10 #in seconds
        
        if time.time() > last_config_update+update_frequency:
            Config_settings = get_config_file(Config_settings)
            last_config_update = time.time()

        
        if not check_recording_matching(client, recording, Config_settings): exit() # Check if recording var match real OBS status
        time.sleep(float(Config_settings.loop_delay)) #Sleep time by config file - reduce CPU load
        
if __name__ == "__main__":
    run()