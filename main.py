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
        nname = ""
    else:
        print("Fname do not exist.")




if not "obs64.exe" in (i.name() for i in psutil.process_iter()):
    print("Starting OBS")
    import imports.start_obs as start_obs
    
    start_obs.main()
    time.sleep(1)
print("OBS is open")

print("Connecting to OBS...")
pwd = 'AkE5MGKgeBRAF3ti'
client = ReqClient(host='localhost', port=4455, password=pwd)
print("Connected to OBS")

# zapnout nahrávání
client.start_record()




