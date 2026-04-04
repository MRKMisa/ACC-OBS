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

    if os.path.exist(Config_settings.obs_path + name):
        print("Fname exist.")
        info = get_shared_mem()
        
        nname = f'{info.static.track}-{info.static.carModel}-{info.graphics.lastTime}-{x.strftime("%Y-%m-%d_%H-%M-%S")}' #<track>-<car>-<last-lap>-<time>
        
        try:
            shutil.copy(Config_settings.obs_path + name, Config_settings.motec_path + nname)
        except Exception as e:
            print("Can´t copy file.")
            print(e)
            exit()
    else:
        print("Fname do not exist.")
        print(Config_settings.obs_path + name)
        print(os.listdir())
        exit()


if __name__ == "__main__":
    #Get obs_app_path from config.ini
    from imports import get_config_file
    
    
    Config_settings = get_config_file()
    #cwd=r"C:\Program Files\obs-studio\bin\64bit"
    
    
    start_obs(Config_settings.obs_app_path)