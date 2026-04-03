from imports.get_shared_mem import get_shared_mem
from imports.get_extended_shared_mem import read_data_from_shared_memory

from obsws_python import ReqClient
import psutil, datetime
import time, os, shutil

    
global Config_settings
from imports import config
Config_settings = config.get_config_file()


def stop_recording_and_rename(client):
    # zastavit nahrávání
    client.stop_record()

    x = datetime.datetime.now()
    print("Recording stoped. Renaming file.")

    name = (x.strftime("%Y-%m-%d_%H-%M-%S")) + ".mkv"

    if os.path.exist(Config_settings.obs_path + name):
        print("Fname exist.")
        info = get_shared_mem()
        
        nname = f"{info.static.track}-{info.static.carModel}-{info.graphics.lastTime}-{x.strftime("%Y-%m-%d_%H-%M-%S")}" #<track>-<car>-<last-lap>-<time>
        
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



#Starting OBS
if not "obs64.exe" in (i.name() for i in psutil.process_iter()): #If OBS is not running
    print("Starting OBS")
    import imports.start_obs as start_obs
    
    start_obs.main()
    time.sleep(1)
print("OBS is open")

print("Connecting to OBS...")
client = ReqClient(host='localhost', port=Config_settings.obs_port, password=Config_settings.obs_pwd) #Connect to OBS with web socket
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
    while True:
        if event():
            main()
            
        #Every 10s update config
        now = datetime.datetime.now()
        if [*str(now.second)][1] == "0":
            Config_settings = config.get_config_file()
            
        
        time.sleep(d)
        
if __name__ == "__main__":
    delay = Config_settings.delay
    
    run(delay)