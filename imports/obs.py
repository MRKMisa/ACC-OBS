import subprocess, datetime, shutil, os, time

from imports import get_shared_mem

global name


def start_obs(cwd=r"C:\Program Files\obs-studio\bin\64bit"):

    subprocess.Popen(
        ["obs64.exe", "--minimize-to-tray"],
        cwd=cwd,
        shell=True
    )


def stop_recording_and_rename(client, Config_settings):
    global name
    # stop recording
    client.stop_record()
    print("Recording stoped. Renaming file.")

    print(f"Fname - {name}")
    if not os.path.exists(Config_settings.obs_output_path + name):
        print("Fname do not exist.")
        
        print("Waiting to file...")
        max_OBS_wait_time = 5 # In seconds
        
        start = time.time()
        
        while not os.path.exists(Config_settings.obs_output_path + name): # IF file exists...
            time.sleep(0.3)
            
            if time.time() >= start + max_OBS_wait_time: # If it´s waiting more than max wait time...
                print("Fname do not exist.")
                print(f"Waiting {max_OBS_wait_time}s")
                print(Config_settings.obs_output_path + name)
                print(os.listdir(Config_settings.obs_output_path))
                exit()
                
        
    

    if os.path.exists(Config_settings.obs_output_path + name):
        print("Fname exist.")
        info = get_shared_mem()
        
        nname = f'{info.static.track}-{info.static.carModel}-{info.graphics.lastTime}-{name}.mp4' #<track>-<car>-<last-lap>-<time>
        print(f"Nname - {nname}")
        
        try:
            print(f"Move {Config_settings.obs_output_path + name} > {Config_settings.motec_path + nname}")
            shutil.move(Config_settings.obs_output_path + name, Config_settings.motec_path + nname)
        except Exception as e:
            print("Can´t move file.")
            print(e)
            exit()
    else:
        print("Fname do not exist.")
        print(Config_settings.obs_output_path + name)
        print(os.listdir(Config_settings.obs_output_path))
        exit()


def check_recording_matching(client, recording, Config_settings, attemps=0):
    status = client.get_record_status().output_active
    pause_status = client.get_record_status().output_paused

    if recording == True and not status: # If var is True but OBS is not recording
        print("Recording var does not match real OBS status...")
        print(f"Recording: {recording}, OBS status: {status}")
        print(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            print("Trying to start recording...")
            start_recording(client) # Trying to start recording
            return check_recording_matching(client, recording, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            print("After 3 atemps. Stoping script...")
            print("Recording var still does not match real OBS status.")
            print(f"Recording: {recording}, OBS status: {status}")
            print(f"Atempt: {attemps}")
            return False
    
    elif recording == False and status:  # If var is False but OBS is recording
        print("Recording var does not match real OBS status...")
        print(f"Recording: {recording}, OBS status: {status}")
        print(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            print("Trying to stop recording...")
            stop_recording_and_rename(client, Config_settings) # Try to stop recording
            return check_recording_matching(client, recording, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            print("After 3 atemps. Stoping script...")
            print("Recording var still does not match real OBS status.")
            print(f"Recording: {recording}, OBS status: {status}")
            print(f"Atempt: {attemps}")
            return False
        
        
    elif recording == None and not status:  # If var is None(Pause) but OBS is not recording
        print("Recording var does not match real OBS status...")
        print(f"Recording: {recording}, OBS status: {status}")
        print(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            print("Trying to start and pause recording...")
            start_recording(client) # Trying to start recording
            pause_recording(client, recording)  # Trying to pause recording
            return check_recording_matching(client, recording, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            print("After 3 atemps. Stoping script...")
            print("Recording var still does not match real OBS status.")
            print(f"Recording: {recording}, OBS status: {status}")
            print(f"Atempt: {attemps}")
            return False
    
    
    
    elif recording == None and not pause_status:  # If var is None(Pause) but OBS is recording but not pause
        print("Recording var does not match real OBS status...")
        print(f"Recording: {recording}, OBS status: {status}")
        print(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            print("Trying to pause recording...")
            pause_recording(client, recording)  # Trying to pause recording
            return check_recording_matching(client, recording, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            print("After 3 atemps. Stoping script...")
            print("Recording var still does not match real OBS status.")
            print(f"Recording: {recording}, OBS status: {status}")
            print(f"Atempt: {attemps}")
            return False


    elif recording == None and not pause_status:  # If var is None(Pause) but OBS is recording but not pause
        print("Recording var does not match real OBS status...")
        print(f"Recording: {recording}, OBS status: {status}")
        print(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            print("Trying to pause recording...")
            pause_recording(client, recording)  # Trying to pause recording
            return check_recording_matching(client, recording, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            print("After 3 atemps. Stoping script...")
            print("Recording var still does not match real OBS status.")
            print(f"Recording: {recording}, OBS status: {status}")
            print(f"Atempt: {attemps}")
            return False
        
    elif recording != None and pause_status: # If var is not None(Pause) but OBS is recording and PAUSE
        print("Recording var does not match real OBS status...")
        print(f"Recording: {recording}, OBS status: {status}")
        print(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            print("Trying to unpause recording...")
            unpause_recording(client, recording)  # Trying to unpause recording
            return check_recording_matching(client, recording, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            print("After 3 atemps. Stoping script...")
            print("Recording var still does not match real OBS status.")
            print(f"Recording: {recording}, OBS status: {status}")
            print(f"Atempt: {attemps}")
            return False    
        
        
    else:
        return True # Otherwise just return True everything is ok :)

def start_recording(client):
    global name
    
    print("Starting recording...")
    status = client.get_record_status().output_active
    if status:
        print("OBS is already recording.")
        return
    
    client.start_record()
    
    x = datetime.datetime.now()
    name = (x.strftime("%Y-%m-%d_%H-%M-%S")) + ".mp4"
    print("Recording started.")

def pause_recording(client, recording):
    try:
        print("Pausing record...")
        client.pause_record()
        print("Record pause...")
    except Exception as e:
        print("Can´t pause record...")
        print("Recording: " + recording, "OBS status: " + client.get_record_status().output_active)
        print(e)
        

def unpause_recording(client, recording):
    try:
        print("Unpausing record...")
        client.resume_record()
        print("Record running...")
    except Exception as e:
        print("Can´t unpause record...")
        print("Recording: " + recording, "OBS status: " + client.get_record_status().output_active)
        print(e)




def check_OBS_ready(client):
    
    try:
        client.get_version() # Check if OBS is ready
        return True # If ready just return True to main
    except:
        print("OBS isn´t ready...") # If not start waiting
        
        
    print("Waiting to OBS...")
    max_OBS_waiting_time = 10 # In seconds
    
    start = time.time()
    
    while time.time() < start+max_OBS_waiting_time: # Waiting max 10 sec
        
        try:
            client.get_version() # Get OBS version. If OBS isn´t ready return error.
            return True # If OBS ready return True to main
        except:
            os.system("cls") # Clear terminal because OBS is spaming error messages.
            time.sleep(0.2) # Wait to OBS can start...
            
    print(f"OBS is not ready in {max_OBS_waiting_time}s...")
    print("Exiting script...")
    return False # Return False that OBS isn´t ready...


if __name__ == "__main__":
    #Get obs_app_path from config.ini
    from imports import get_config_file
    
    
    Config_settings = get_config_file()
    #cwd=r"C:\Program Files\obs-studio\bin\64bit"
    
    
    start_obs(Config_settings.obs_app_path)