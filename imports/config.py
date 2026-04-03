import os

def delete_comments(config):
    new_config = []
    for line in config:
        if "#" in line:
            line = line.replace(line[line.find("#"):], "")

        new_config.append(line)


    return new_config

def get_config_file():

    if os.path.exists("config.ini"):
        print("Loading config.ini file...")
        
        #OBS password
        try:
            with open("config.ini", "r") as f:
                config = f.readlines()
            
            config = delete_comments(config) #Filtring comments
            
            #Is obs_pwd conf in file?
            obs_pwd = None
            for line in config:
                if "obs_pwd" in line:
                    obs_pwd = line.split("=")[1].strip()
                    
                    
                
            if obs_pwd == None:
               print("Can´t find obs_pwd arg in config.ini...")
               exit()
            
            if obs_pwd == "" or obs_pwd == None:
                print("Can´t get OBS password from config.ini file!!!")
                print("Maybe you let password blank.")
                exit()
                
        except Exception as e:
             print("Can´t get OBS password from config.ini file!!!")
             print(e)
             exit()
        
        #OBS port
        try:
            with open("config.ini", "r") as f:
                config = f.readlines()
            
            config = delete_comments(config) #Filtring comments
            
            #Is obs_port conf in file?
            obs_port = None
            for line in config:
                if "obs_port" in line:
                    obs_port = line.split("=")[1].strip()
                    
                    
                
            if obs_port == None:
               print("Can´t find obs_port in config.ini...")
            
            if obs_port == "" or obs_port == None:
                obs_port = "4455" #Default port
                print("OBS port set on default (4455)")
                
        except Exception as e:
             print("Can´t get OBS port from config.ini file...")
             print(e)
             exit()
        
        
        
        #OBS app path
        try:
            with open("config.ini", "r") as f:
                config = f.readlines()
            
            config = delete_comments(config) #Filtring comments
            
            #Is obs_app_path conf in file?
            obs_app_path = None
            for line in config:
                if "obs_app_path" in line:
                    obs_app_path = line.split("=")[1].strip()
                    
                    
                
            if obs_app_path == None:
               print("Can´t find obs_app_path in config.ini...")
            
            if obs_app_path == "" or obs_app_path == None:
                obs_app_path = r"C:\Program Files\obs-studio\bin\64bit" #Default path
                print(r"OBS app path set on default (C:\Program Files\obs-studio\bin\64bit)")
                
        except Exception as e:
             print("Can´t get OBS app path from config.ini file...")
             print(e)
             exit()
        
        
        #OBS output path
        try:
            with open("config.ini", "r") as f:
                config = f.readlines()
            
            config = delete_comments(config) #Filtring comments
            
            #Is obs_output_path conf in file?
            obs_output_path = None
            for line in config:
                if "obs_output_path" in line:
                    obs_output_path = line.split("=")[1].strip()
                    
                    
                
            if obs_output_path == None:
               print("Can´t find obs_output_path in config.ini...")
            
            if obs_output_path == "" or obs_output_path == None:
                obs_output_path = os.path.expanduser("~/Videos") #Default path
                print("OBS output path set on default (user videos folder)")
                
        except Exception as e:
             print("Can´t get OBS output path from config.ini file...")
             print(e)
             exit()
             
             
        #Motec path
        try:
            with open("config.ini", "r") as f:
                config = f.readlines()
                
            config = delete_comments(config) #Filtring comments
        
            #Is motec_path conf in file?
            motec_path = None
            for line in config:
                if "motec_path" in line:
                    motec_path = line.split("=")[1].strip()
                    
                    
                
            if motec_path == None:
               print("Can´t find motec_path in config.ini...")
            
            if motec_path == "" or motec_path == None:
                motec_path = "C:/MoTeC/Videos" #Default path
                print("Motec path set on default (C:/MoTeC/Videos)")
                
        except Exception as e:
             print("Can´t get Motec path from config.ini file...")
             print(e)
             exit()
            
            
        #Script loop delay
        try:
            with open("config.ini", "r") as f:
                config = f.readlines()
                
            config = delete_comments(config) #Filtring comments
        
            #Is loop_delay conf in file?
            loop_delay = None
            for line in config:
                if "loop_delay" in line:
                    loop_delay = line.split("=")[1].strip()
                    
                    
                
            if loop_delay == None:
               print("Can´t find loop_delay in config.ini...")
            
            if loop_delay == "" or loop_delay == None:
                loop_delay = 0.01 #Default delay
                print("Script loop delay set on default (0.01s)")
                
        except Exception as e:
             print("Can´t get Script loop delay from config.ini file...")
             print(e)
             exit()
            
                
                
    else:
        print("Can´t find config.ini file. Setting default settings...")
        
        
        #OBS password
        obs_pwd = input("PLEASE type OBS password...")
        print("OBS password set.")
        
        #OBS port
        obs_port = 4455
        print("OBS port set on default (4455).")
        
        
        #OBS app path
        obs_app_path = r"C:\Program Files\obs-studio\bin\64bit"
        print(r"OBS app path set on default (C:\Program Files\obs-studio\bin\64bit).")
        
        
        #OBS output path to default
        obs_output_path = os.path.expanduser("~/Videos") #Default path
        print("OBS output path set on default (user videos folder).")
        
        
        #Motec path to default
        motec_path = "C:/MoTeC/Videos" #Default path
        print("Motec path set on default (C:/MoTeC/Videos).")
        
        
        #Script loop delay
        delay = 0.01
        print("Script loop delay set on default. (0.01s)")
        

    class Config_settings:
        def __init__(self):
            self.obs_pwd = obs_pwd
            self.obs_port = obs_port
            
            self.obs_app_path = obs_app_path
            self.obs_output_path = obs_output_path
            self.motec_path = motec_path
            
            self.delay = delay
    
        
    return Config_settings()
    