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

    client.stop_record() # Stop recording
    print("Recording stoped. Renaming file.")
    
    try:
        print(f"Fname - {name}") # If name of the file is saved by script...
        print("File name is saved.")
    except:
        print("Name of the file is not saved. Just stoping recording...") # If not script won´t be renaming and moving record...
        return
    
    #Checking if file exist and if not waiting
    if not os.path.exists(f"{Config_settings.obs_output_path}/{name}"):
        print("Fname do not exist.")
        
        print("Waiting to file...")
        max_OBS_wait_time = 10 # In seconds
        
        start = time.time()
        
        while not os.path.exists(f"{Config_settings.obs_output_path}/{name}"): # IF file exists...
            time.sleep(0.3)
            
            if time.time() >= start + max_OBS_wait_time: # If it´s waiting more than max wait time...
                print("Fname do not exist.")
                print(f"Waiting {max_OBS_wait_time}s")
                print(f"{Config_settings.obs_output_path}/{name}")
                print(os.listdir(Config_settings.obs_output_path))
                
                
                print()
                print()
                
                # Getting last video file from the folder...
                if os.path.exists(f"{Config_settings.obs_output_path}/{name}"): # Last chance if saved name exist in the path
                    print("File exist.")
                    break
                else:
                    print("Getting last file in folder...") # If file is not exists in folder. Script will get last file in the folder...
                    
                    
                    files = os.listdir(Config_settings.obs_output_path) # Get files
                    
                    videos = []
                    for file in files:
                        if file.endswith(".mp4"): # Append only mp4 files
                            videos.append(file) 
                    
                    try:
                        last_video = videos[-1]    # Get lastest mp4 file
                        print(f"Get last video...")
                        print(last_video)
                    except: # If can´t get last mp4 maybe in folder isn´t any... Shuting down script...
                        print("Can´t get last video...")
                        print(f"All files: {files}")
                        print(f"Videos: {videos}")
                        exit()
                        
                    
                    # Check if file match saved files date
                    
                    #V1
                    '''
                    def get_time_date_from_file_name(file_name):
                        
                        file_name = file_name.replace(".mp4", "")

                        date = file_name.split("_")[0]
                        y = date.split("-")[0]
                        m = date.split("-")[1]
                        d = date.split("-")[2]

                        time = file_name.split("_")[1]
                        h = time.split("-")[0]
                        m = time.split("-")[1]
                        s = time.split("-")[2]
                        
                        
                        return y, m, d, h, h, s
                    
                    try:
                        my_y, my_m, my_d, my_h, my_h, my_s = get_time_date_from_file_name(name)
                    except Exception as e:
                        print("Can´t get date and time from my file name...")
                        print(e)
                        exit()
                        
                    try:
                        last_video_y, last_video_m, last_video_d, last_video_h, last_video_h, last_video_s = get_time_date_from_file_name(last_video)
                    except Exception as e:
                        print("Can´t get date and time from last file name...")
                        print(e)
                        exit()
                        
                    if my_y != last_video_y:
                        print(f"My file name and last video name year does not match...")
                        print(f"{my_y} - {last_video_y}")
                        exit()
                        
                    '''
                        
                    #V2
                    my_date = datetime.datetime.strptime(name.replace(".mp4"), "%Y-%m-%d_%H-%M-%S")
                    
                    last_video_date = datetime.datetime.strptime(last_video.replace(".mp4"), "%Y-%m-%d_%H-%M-%S")
                    
                    diff = my_date - last_video_date
                    
                    max_diff = 10 # Max my name date difference to last video date from folder. In seconds
                    
                    if diff.total_seconds() > max_diff: # If difference from my name file and last file is greather than max script will not use this file. Because OBS name file by time where you stared recording. But I take date next to start_recording command. But there is some delay. So its can be like second of. That would make that script would not find file name in the folder. So I take last video file and check if it´s small diffence. Diff that would realisticly can be in this process. 10s is very big but it´s safe to use.
                        print(f"Last video from folder is older than my predicted time. Diff: {diff.total_seconds()}. Max: {max_diff}.") # If diff is greather script will stop. Because script think there should be file with this name. So if it´s not there is some issue.
                        print()
                        print("Stoping script...")
                        exit()


                    print(f"Get last file from folder. Diff is just: {diff}s. File: {last_video}")
                    name = last_video
                    break
            
    
                
        
    

    if os.path.exists(f"{Config_settings.obs_output_path}/{name}"):
        print("Name exist.")
        info = get_shared_mem()
        
        nname = f'{info.static.track}-{info.static.carModel}-{info.graphics.bestTime}{name}.mp4' #<track>-<car>-<best-lap>-<time>
        print(f"Nname - {nname}")
        print(f"Move {Config_settings.obs_output_path}/{name} > {Config_settings.motec_path}/{nname}")
        
        
        

        try:  # OBS can have file open for sec
            shutil.move(f"{Config_settings.obs_output_path}/{name}", f"{Config_settings.motec_path}/{nname}")
        except Exception as e:
            print("Can´t move file.")
            print(e)
            
        print("Waiting to move file...")
        
        max_OBS_wait_time = 10
        
        start = time.time()

        while time.time() < start + max_OBS_wait_time:
            time.sleep(0.3)
            
            try:
                shutil.move(f"{Config_settings.obs_output_path}/{name}", f"{Config_settings.motec_path}/{nname}")
                print(f"File moved!!!")
                return
            except Exception as e:
                print(f"Trying to move file... Time: {(time.time() - start)} / {max_OBS_wait_time}s")

        
        print("Moving file failed...") 
        print(f"Waiting {(time.time() - start)} / max{max_OBS_wait_time}s")
        
        print(f"Name: {name}, Nname: {nname}")
        print()
        
        print(f"Whole path: {Config_settings.obs_output_path}/{name} > {Config_settings.motec_path}/{nname}")
        print("Stoping script...")
        exit()




    else:
        print("Fname do not exist.")
        print(f"{Config_settings.obs_output_path}/{name}")
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
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
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
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
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
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
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
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
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
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
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
            time.sleep(0.1*attemps)
            return check_recording_matching(client, recording, Config_settings, attemps=attemps+1)
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