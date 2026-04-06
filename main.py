from imports import get_shared_mem
from imports import read_data_from_shared_memory

from obsws_python import ReqClient
import psutil, datetime, time

from imports import stop_recording_and_rename, check_recording_matching, start_recording, check_OBS_ready, pause_recording, unpause_recording


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



def event(last_state, last_current_time): # return if OBS should be recording
    info = get_shared_mem()
    #print(f"Time: {info.graphics.iCurrentTime}, Last time: {last_current_time}, Curr game status: {info.graphics.status}, Last game status: {last_state}")
    
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
                
        return False, info.graphics.status, None # Return that OBS should not be recording


    if last_state != 2:
        print("Game is running...")

    

        
    
    
    current_time = info.graphics.iCurrentTime # Get AC or ACC time i in front mean in miliseconds. So it not 0:00.123 but 123. It´s better working with.
    
    
    if current_time == "-:--.---" or current_time == None or last_current_time == None or last_current_time == current_time: # AC or ACC will return this time when session doesn´t started yet. If ses does not stared we dont want to recording.
        if current_time != None and last_current_time != current_time:
            print("Session does not started...")
        return False, info.graphics.status, current_time # So we will return False
    
    else:
        if last_current_time == None or last_current_time == "-:--.---" or current_time == last_current_time:
            print("Session just started...")
    
    return True, info.graphics.status, current_time  # There we can just return True because here we want to recording.





def run():
    global Config_settings, client
    last_config_update = time.time()
    last_current_time = None
    
    last_state = None
    loop = True
    
    recording = False # False - not recording, True - recording, None - recording is pause
    bs = 0
    
    while loop:
        b, last_state, last_current_time = event(last_state, last_current_time)
        if b:
            if bs < 0:
                bs = 0
                
            bs += 1
        else:
            if bs > 0:
                bs = 0
            
            bs -= 1
        
        
        #print(f"Bs: {b}")
        if bs > 2:
            if recording == False:
                start_recording(client)
                recording = True
                
            if recording == None:
                unpause_recording(client, recording)
                recording = True
                
        elif bs < -3:
            if recording == True:
                if last_state == 0:
                    print("Game is not running...")
                    stop_recording_and_rename(client, Config_settings)
                    recording = False
                    
                if last_state == 1:
                    print("Game is in replay pausing recording...")
                    pause_recording(client, recording)
                    recording = None # None - pause
                
                if last_state == 2:
                    print("Game is running. But maybe session does not started yet. Stoping and saving record...")
                    stop_recording_and_rename(client, Config_settings)
                    recording = False
                    
                if last_state == 3:
                    print("Game is pause. Pausing recording...")
                    pause_recording(client, recording)
                    recording = None # None - pause
                    
            if recording == None:
                if last_state == 0:
                    print("Game is not running...")
                    stop_recording_and_rename(client, Config_settings)
                    recording = False        
                    



        #Every 10s update config
        update_frequency = 10 #in seconds
        
        if time.time() > last_config_update+update_frequency:
            Config_settings = get_config_file(Config_settings)
            last_config_update = time.time()

        
        time.sleep(float(Config_settings.loop_delay)) #Sleep time by config file - reduce CPU load
        if not check_recording_matching(client, recording, Config_settings): exit() # Check if recording var match real OBS status
        
if __name__ == "__main__":
    run()