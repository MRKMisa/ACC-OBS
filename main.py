from imports import get_shared_mem

from obsws_python import ReqClient
import psutil, time

from imports import stop_recording_and_rename, check_recording_matching, start_recording, check_OBS_ready, pause_recording, unpause_recording

global Config_settings
from imports import get_config_file, print_from_config_class

# Import loggings defs
from imports import set_logging, write_log, log_config_setting, print_log, error_log, cycle_log



##### Maybe I should try return False if last time is greather than live!!!!!!
def event(info, last_state, last_current_time): # return if OBS should be recording
    #print(f"Event def: Time: {info.graphics.iCurrentTime}, Last time: {last_current_time}, Curr game status: {info.graphics.status}, Last game status: {last_state}")
    cycle_log(f"Event def: Time: {info.graphics.iCurrentTime}, Last time: {last_current_time}, Curr game status: {info.graphics.status}, Last game status: {last_state}\n")
    
    
    if info.graphics.status != 2: # If game is not live
        if info.graphics.status == 0:
            if last_state != 0:
                print_log("Game is not running...")
            time.sleep(0.5)
        elif info.graphics.status == 1:
            if last_state != 1:
                print_log("Game is in replay...")
            time.sleep(0.3)
        elif info.graphics.status == 3:
            if last_state != 3:
                print_log("Game is pause...")
            time.sleep(0.1)
                
        return False, info.graphics.status, None # Return that OBS should not be recording


    if last_state != 2:
        print_log("Game is running...")

    

        
    
    
    current_time = info.graphics.iCurrentTime # Get AC or ACC time i in front mean in miliseconds. So it not 0:00.123 but 123. It´s better working with.
    
    
    if current_time == "-:--.---" or current_time == None or last_current_time == None or last_current_time == current_time: # AC or ACC will return this time when session doesn´t started yet. If ses does not stared we dont want to recording.
        if current_time != None and last_current_time != current_time:
            print_log("Session does not started...")
        return False, info.graphics.status, current_time # So we will return False
    
    else:
        pass
    
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
        b, last_state, last_current_time = event(get_shared_mem(), last_state, last_current_time)
        cycle_log(f"B: {b}, Bs: {bs}")
        
        if b:
            if bs < 0:
                bs = 0
                
            bs += 1
        else:
            if bs > 0:
                bs = 0
            
            bs -= 1
        
        
        
        if bs >= 3: # Should be recording
            if recording == False: # But if it´s not recording
                start_recording(client) # Start recording
                recording = True
                
                
                
            if recording == None: # But if it´s pause
                unpause_recording(client, recording) # unpause
                recording = True
                
        elif bs <= -4: # Should not be recording
            if recording == True:  # But if it´s recording
                if last_state == 0: # If game is not running
                    print_log("Game is not running...")
                    stop_recording_and_rename(client, Config_settings) # Stop and save
                    recording = False
                    
                if last_state == 1: # If game is in replay
                    print_log("Game is in replay pausing recording...")
                    pause_recording(client, recording) # Pause record. We don´t want to record replay...
                    recording = None # None - pause
                
                if last_state == 2: # If game is running
                    print_log("Game is running. But maybe session does not started yet. Stoping and saving record...")
                    stop_recording_and_rename(client, Config_settings) # Stop recording. Because session maybe ended and another session does not started yet. So we will stop move and start recordning will be in another step.
                    recording = False
                    
                if last_state == 3: # If game is paused
                    print_log("Game is pause. Pausing recording...")
                    pause_recording(client, recording) # Pause record. We don´t want to record pause screen...
                    recording = None # None - pause
                    
            if recording == None: # But record is pause
                if last_state == 0: # If game is not running...
                    print_log("Game is not running...")
                    stop_recording_and_rename(client, Config_settings) # Just stop recording
                    recording = False        

                if last_state == 2: # If game is running
                    print_log("Game is running. But maybe session does not started yet. Record is pause. Stoping and saving record...")
                    stop_recording_and_rename(client, Config_settings) # Stop recording. Because session maybe ended and another session does not started yet. So we will stop move and start recordning will be in another step.
                    recording = False                  



        #Every 10s update config
        update_frequency = 10 #in seconds
        
        if time.time() > last_config_update+update_frequency:
            Config_settings = get_config_file(Config_settings)
            last_config_update = time.time()

        
        time.sleep(float(Config_settings.loop_delay)) #Sleep time by config file - reduce CPU load
        if not check_recording_matching(client, recording, Config_settings): exit() # Check if recording var match real OBS status
        
if __name__ == "__main__":
    script_logging = 3 # 0 - no logging, 1 - just error logging, 2 - errors and prints logging, 3 - errors, prints and cycle logging
    set_logging(script_logging)
    
    
    # Getting config setting
    Config_settings = get_config_file()
    
    
    print()
    print("---Config settings---")
    print_from_config_class(Config_settings)
    print()
    
    # Log Config settings
    log_config_setting(Config_settings)
    print_log("")



    #Starting OBS
    if not "obs64.exe" in (i.name() for i in psutil.process_iter()): #If OBS is not running
        print_log("Starting OBS...")
        from imports import start_obs
        
        try:
            start_obs()
        except Exception as e:
            error_log("Can´t start OBS...")
            error_log("Exiting script...")
            error_log(e)
            exit()
        time.sleep(1) #Wait till OBS starts
        
        if not "obs64.exe" in (i.name() for i in psutil.process_iter()): # If OBS isn´t running
            print_log("OBS isn´t still open...")
            max_wating_time_to_obs = 5 # in seconds
            
            print_log(f"Waiting to OBS open max {max_wating_time_to_obs}s...")
            start = time.time()
            
            while not "obs64.exe" in (i.name() for i in psutil.process_iter()):
                time.sleep(0.5)
                
                if time.time() > start+max_wating_time_to_obs:
                    error_log(f"OBS did not start in {max_wating_time_to_obs}s...")
                    error_log("Exiting script...")
                    exit()
            


    print_log("OBS is open.\n")


    print_log("Connecting to OBS...")
    try:
        global client
        client = ReqClient(host='localhost', port=Config_settings.obs_port, password=Config_settings.obs_pwd) #Connect to OBS with web socket
    except Exception as e:
        error_log("Can´t connect to OBS...")
        error_log("Exiting script...")
        error_log(e)
        exit()
    print_log("Connected to OBS.")
    print_log("")

    print_log("Checking if OBS is ready...")
    if not check_OBS_ready(client): exit()
    print_log("OBS is ready to use.\n\n")
    
    
    
    
    
    
    run()