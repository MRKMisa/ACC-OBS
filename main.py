from imports.get_shared_mem import get_shared_mem
from imports.get_extended_shared_mem import read_data_from_shared_memory

from obsws_python import ReqClient
import psutil, datetime
import time, os

def stop_recording_and_rename(client):
    # zastavit nahrávání
    client.stop_record()

    x = datetime.datetime.now()
    print("Recordin stoped. Renaming file.")

    name = (x.strftime("%Y-%m-%d_%H-%M-%S")) + ".mkv"

    if os.path.exist("C:/MoTeC/Videos/"+name):
        print("Fname exist.")
        info = get_shared_mem()
        
        nname = f"{info.sttic.track}-{info.statci.carModel}-{info.graphics.lastTime}-{x.strftime("%Y-%m-%d_%H-%M-%S")}" #<track>-<car>-<last-lap>-<time>
        
        try:
            os.rename("C:/MoTeC/Videos/"+name, "C:/MoTeC/Videos/"+nname)
        except Exception as e:
            print("Cant rename file. {e}")
    else:
        print("Fname do not exist.")



#Starting OBS
if not "obs64.exe" in (i.name() for i in psutil.process_iter()): #If OBS is not running
    print("Starting OBS")
    import imports.start_obs as start_obs
    
    start_obs.main()
    time.sleep(1)
print("OBS is open")

print("Connecting to OBS...")
pwd = 'AkE5MGKgeBRAF3ti' #OBS password
client = ReqClient(host='localhost', port=4455, password=pwd) #Connect to OBS with web socket
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
    
    