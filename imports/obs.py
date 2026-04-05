import subprocess, datetime, shutil, os

from imports import get_shared_mem


def start_obs(cwd=r"C:\Program Files\obs-studio\bin\64bit"):

    subprocess.Popen(
        ["obs64.exe", "--minimize-to-tray"],
        cwd=cwd,
        shell=True
    )


def stop_recording_and_rename(client, Config_settings):
    # stop recording
    client.stop_record()

    x = datetime.datetime.now()
    print("Recording stoped. Renaming file.")

    name = (x.strftime("%Y-%m-%d_%H-%M-%S")) + ".mkv"
    print(f"Fname - {name}")

    if os.path.exists(Config_settings.obs_output_path + name):
        print("Fname exist.")
        info = get_shared_mem()
        
        nname = f'{info.static.track}-{info.static.carModel}-{info.graphics.lastTime}-{x.strftime("%Y-%m-%d_%H-%M-%S")}' #<track>-<car>-<last-lap>-<time>
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


def check_recording_matching(client, recording, attemps=0):
    status = client.get_record_status().output_active

    if recording and not status:
        print("Recording var does not match real OBS status")
        print("Recording: " + recording, "OBS status: " + status)
        print("Atempt " + attemps)
        if attemps <= 3:
            if recording and not status:
                start_recording(client)
                return check_recording_matching(client, recording, attemps=attemps+1)
        else:
            return False
        
        
        
    else:
        return True

def start_recording(client):
    print("Starting recording...")
    status = client.get_record_status().output_active
    if status:
        print("OBS is already recording.")
        return
    
    client.start_record()
    print("Recording started.")


if __name__ == "__main__":
    #Get obs_app_path from config.ini
    from imports import get_config_file
    
    
    Config_settings = get_config_file()
    #cwd=r"C:\Program Files\obs-studio\bin\64bit"
    
    
    start_obs(Config_settings.obs_app_path)