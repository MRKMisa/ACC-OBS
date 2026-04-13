import subprocess, datetime, shutil, os, time

from .get_shared_mem import get_shared_mem

from .log import set_logging, write_log, log_config_setting, print_log, error_log, cycle_log

global file_name # File name of video


def start_obs(cwd=r"C:\Program Files\obs-studio\bin\64bit"):

    # Stared OBS but just in minimized mode
    subprocess.Popen(
        ["obs64.exe", "--minimize-to-tray"],
        cwd=cwd,
        shell=True
    )


def stop_recording_and_rename(client, Config_settings):
    global file_name

    client.stop_record() # Stop recording
    print_log("Recording stoped. Renaming file.")
    
    # If name of the file is saved by script...
    try:
        print_log(f"Fname - {file_name}") # If script was not saved file name before this will end in error. In this situation we want to just end recording because it´s not our.
        print_log("File name is saved.")
    except:
        error_log("Name of the file is not saved. Just stoping recording...") # If not script won´t be renaming and moving record...
        return
    
    
    
    
    
    #Checking if file exist and if not waiting
    if not os.path.exists(f"{Config_settings.obs_output_path}/{file_name}"):
        print_log("Fname do not exist.")
        
        print_log("Waiting to file...")
        max_OBS_wait_time = 10 # In seconds
        
        start = time.time()
        
        while not os.path.exists(f"{Config_settings.obs_output_path}/{file_name}"): # If file exists...
            time.sleep(0.3)
            
            if time.time() >= start + max_OBS_wait_time: # If it´s waiting more than max wait time...
                print_log("Fname do not exist.")
                print_log(f"Waited {max_OBS_wait_time}s")
                print_log(f"{Config_settings.obs_output_path}/{file_name}")
                print_log(os.listdir(Config_settings.obs_output_path))
                
                
                print_log("")
                print_log("")
                
                # Getting last video file from the folder...
                if os.path.exists(f"{Config_settings.obs_output_path}/{file_name}"): # Last chance if saved name exist in the path
                    print_log("File exist.")
                    break
                else:
                    print_log("Getting last file in folder...") # If file is not exists in folder. Script will get last file in the folder...
                    
                    
                    files = os.listdir(Config_settings.obs_output_path) # Get files
                    
                    videos = []
                    for file in files:
                        if file.endswith(".mp4"): # Append only mp4 files
                            videos.append(file) 
                    
                    try:
                        last_video = videos[-1]    # Get lastest mp4 file
                        print_log(f"Get last video...")
                        print_log(last_video)
                    except: # If can´t get last mp4 maybe in folder isn´t any... Shuting down script...
                        error_log("Can´t get last video...")
                        error_log(f"All files: {files}")
                        error_log(f"Videos: {videos}")
                        error_log("Exiting script...")
                        exit()
                        
                    
                    # Check if file match saved files date
                    my_date = datetime.datetime.strptime(file_name.replace(".mp4"), "%Y-%m-%d_%H-%M-%S")
                    
                    last_video_date = datetime.datetime.strptime(last_video.replace(".mp4"), "%Y-%m-%d_%H-%M-%S")
                    
                    diff = my_date - last_video_date
                    
                    max_diff = 10 # Max my name date difference to last video date from folder. In seconds
                    
                    if diff.total_seconds() > max_diff: # If difference from my name file and last file is greather than max script will not use this file. Because OBS name file by time where you stared recording. But I take date next to start_recording command. But there is some delay. So its can be like second of. That would make that script would not find file name in the folder. So I take last video file and check if it´s small diffence. Diff that would realisticly can be in this process. 10s is very big but it´s safe to use.
                        error_log(f"Last video from folder is older than my predicted time. Diff: {diff.total_seconds()}. Max: {max_diff}.") # If diff is greather script will stop. Because script think there should be file with this name. So if it´s not there is some issue.
                        error_log()
                        error_log("Exiting script...")
                        exit()


                    print_log(f"Get last file from folder. Diff is just: {diff}s. File: {last_video}")
                    file_name = last_video # Setting file name to last video in folder
                    break
            
    
                
        
    

    if os.path.exists(f"{Config_settings.obs_output_path}/{file_name}"):
        print_log("Name exist.")
        info = get_shared_mem()
        
        nname = f'{info.static.track}-{info.static.carModel}-{info.graphics.bestTime}{file_name}.mp4' #<track>-<car>-<best-lap>-<time>
        print_log(f"Nname - {nname}")
        print_log(f"Move {Config_settings.obs_output_path}/{file_name} > {Config_settings.motec_path}/{nname}")
        
        
        

        try:  # OBS can have file open for sec
            shutil.move(f"{Config_settings.obs_output_path}/{file_name}", f"{Config_settings.motec_path}/{nname}") # Moving old OBS output to motec folder with new name...
            print_log(f"File moved!!!")
            return
        except Exception as e:
            error_log("Can´t move file!!!")
            print(e)
            
        print_log("Waiting to move file...")
        
        max_OBS_wait_time = 10
        
        start = time.time()

        while time.time() < start + max_OBS_wait_time:
            time.sleep(0.3)
            
            try:
                shutil.move(f"{Config_settings.obs_output_path}/{file_name}", f"{Config_settings.motec_path}/{nname}")
                print_log(f"File moved!!!")
                return
            except Exception as e:
                print_log(f"Trying to move file... Time: {(time.time() - start)} / {max_OBS_wait_time}s")

        
        error_log("Moving file failed...") 
        error_log(f"Waited {(time.time() - start)} / max{max_OBS_wait_time}s")
        
        error_log(f"Name: {file_name}, Nname: {nname}")
        error_log()
        
        error_log(f"Whole path: {Config_settings.obs_output_path}/{file_name} > {Config_settings.motec_path}/{nname}")
        error_log("Exiting script...")
        exit()




    else:
        error_log("Fname do not exist.")
        error_log(f"{Config_settings.obs_output_path}/{file_name}")
        error_log(os.listdir(Config_settings.obs_output_path))
        error_log("Exiting script...")
        exit()


def check_recording_matching(client, recording, Config_settings, attemps=0):
    status = client.get_record_status().output_active
    pause_status = client.get_record_status().output_paused

    if recording == True and not status: # If var is True but OBS is not recording
        error_log("Recording var does not match real OBS status...")
        error_log(f"Recording: {recording}, OBS status: {status}")
        error_log(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            error_log("Trying to start recording...")
            start_recording(client) # Trying to start recording
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            error_log("After 3 atemps. Stoping script...")
            error_log("Recording var still does not match real OBS status.")
            error_log(f"Recording: {recording}, OBS status: {status}")
            error_log(f"Atempt: {attemps}")
            error_log("Exiting script...")
            return False # Return False to exit script...
    
    elif recording == False and status:  # If var is False but OBS is recording
        error_log("Recording var does not match real OBS status...")
        error_log(f"Recording: {recording}, OBS status: {status}")
        error_log(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            error_log("Trying to stop recording...")
            stop_recording_and_rename(client, Config_settings) # Try to stop recording
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            error_log("After 3 atemps. Stoping script...")
            error_log("Recording var still does not match real OBS status.")
            error_log(f"Recording: {recording}, OBS status: {status}")
            error_log(f"Atempt: {attemps}")
            error_log("Exiting script...")
            return False
        
        
    elif recording == None and not status:  # If var is None(Pause) but OBS is not recording
        error_log("Recording var does not match real OBS status...")
        error_log(f"Recording: {recording}, OBS status: {status}")
        error_log(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            error_log("Trying to start and pause recording...")
            start_recording(client) # Trying to start recording
            pause_recording(client, recording)  # Trying to pause recording
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            error_log("After 3 atemps. Stoping script...")
            error_log("Recording var still does not match real OBS status.")
            error_log(f"Recording: {recording}, OBS status: {status}")
            error_log(f"Atempt: {attemps}")
            error_log("Exiting script...")
            return False
    
    
    
    elif recording == None and not pause_status:  # If var is None(Pause) but OBS is recording but not pause
        error_log("Recording var does not match real OBS status...")
        error_log(f"Recording: {recording}, OBS status: {status}")
        error_log(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            error_log("Trying to pause recording...")
            pause_recording(client, recording)  # Trying to pause recording
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            error_log("After 3 atemps. Stoping script...")
            error_log("Recording var still does not match real OBS status.")
            error_log(f"Recording: {recording}, OBS status: {status}")
            error_log(f"Atempt: {attemps}")
            error_log("Exiting script...")
            return False



    elif recording != None and pause_status: # If var is not None(Pause) but OBS is recording and PAUSE
        error_log("Recording var does not match real OBS status...")
        error_log(f"Recording: {recording}, OBS status: {status}")
        error_log(f"Atempt: {attemps}")
        if attemps <= 3: # If it´s not more than 3 attemps. To not loop script.
            error_log("Trying to unpause recording...")
            unpause_recording(client, recording)  # Trying to unpause recording
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
        else: # After 3 attemps just exit script...
            error_log("After 3 atemps. Stoping script...")
            error_log("Recording var still does not match real OBS status.")
            error_log(f"Recording: {recording}, OBS status: {status}")
            error_log(f"Atempt: {attemps}")
            error_log("Exiting script...")
            return False
        
        
    else:
        return True # Otherwise just return True everything is ok :)

def start_recording(client):
    global file_name
    
    print_log("Starting recording...")
    status = client.get_record_status().output_active
    if status:
        print_log("OBS is already recording.")
        return
    
    client.start_record()
    
    x = datetime.datetime.now()
    file_name = (x.strftime("%Y-%m-%d_%H-%M-%S")) + ".mp4"
    print_log("Recording started.")

def pause_recording(client, recording):
    try:
        print_log("Pausing record...")
        client.pause_record()
        print_log("Record pause...")
    except Exception as e:
        error_log("Can´t pause record...")
        error_log("Recording: " + recording, "OBS status: " + client.get_record_status().output_active)
        error_log(e)
        

def unpause_recording(client, recording):
    try:
        print_log("Unpausing record...")
        client.resume_record()
        print_log("Record running...")
    except Exception as e:
        error_log("Can´t unpause record...")
        error_log("Recording: " + recording, "OBS status: " + client.get_record_status().output_active)
        error_log(e)




def check_OBS_ready(client):
    
    try:
        client.get_version() # Check if OBS is ready
        return True # If ready just return True to main
    except:
        print_log("OBS isn´t ready...") # If not start waiting
        
        
    print_log("Waiting to OBS...")
    max_OBS_waiting_time = 10 # In seconds
    
    start = time.time()
    
    while time.time() < start+max_OBS_waiting_time: # Waiting max 10 sec
        
        try:
            client.get_version() # Get OBS version. If OBS isn´t ready return error.
            return True # If OBS ready return True to main
        except:
            os.system("cls") # Clear terminal because OBS is spaming error messages.
            time.sleep(0.2) # Wait to OBS can start...
            
    error_log(f"OBS is not ready in {max_OBS_waiting_time}s...")
    error_log("Exiting script...")
    return False # Return False that OBS isn´t ready...


if __name__ == "__main__":
    
    
    exit()
    #Get obs_app_path from config.ini
    from imports import get_config_file
    
    
    Config_settings = get_config_file()
    #cwd=r"C:\Program Files\obs-studio\bin\64bit"
    
    
    start_obs(Config_settings.obs_app_path)