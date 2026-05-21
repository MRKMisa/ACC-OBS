import os

# Import if this file is imported from another script. You can get in readme.md why this must be there.
if __name__ != "__main__": from .log import set_logging, write_log, log_config_setting, print_log, error_log, cycle_log



# Get config from config.ini or just get default settings. If get argument with class - will run in update mode = load config.ini and just print changes.
def get_config_file(Last_Config_settings=None):
    if Last_Config_settings != None: update_mode = True       # if dont get any args its update mode
    else: update_mode = False                    # otherwise its not update mode
    #Update mode means script will not printing every detail but will only tell what change from Last_Config_settings




    # If file exists
    if os.path.exists("config.ini"):
        if not update_mode: print_log("Loading config.ini file...") # Printing if it´s not updating mode. If it´s updating it will be just spam print.
        
        
        try:  # Get config file
            with open("config.ini", "r") as f:
                config = f.readlines()
                if not update_mode: print_log("Loaded config.ini file.") # Printing if it´s not updating mode. If it´s updating it will be just spam print.
        except Exception as e:
            error_log("CAN´T OPEN config.ini!!!")
            error_log(e)
            config = None
        
        if config != None or config != "":  # If open file and file is not empty
            def delete_comments(config): # Just aid to clear comments and tites from config file :)
                new_config = []
                for line in config:
                    if "#" in line:
                        line = line.replace(line[line.find("#"):], "") # if on line is # it will remore every char from # to the end
                    if str(line).startswith("["):
                        line = line.replace(line[line.find("["):], "") # if on line is [ it will remore every char from [ to the end

                    new_config.append(line)


                return new_config

            config = delete_comments(config) #Filtring comments
        
        
            
        
        
        
            #OBS password
            try:
                #Is obs_pwd conf in file? 
                obs_pwd = None
                for line in config:
                    if "obs_pwd" in line: # if obs_pwd is in line
                        obs_pwd = line.split("=")[1].strip() # We will take everything after =. And strip it to dont have any spaces or tabs # We will take everything after =. And strip it to dont have any spaces or tabs
                        
                        
                    
                if obs_pwd == None:
                    error_log("Can´t find row obs_pwd in config.ini...")
                    error_log("Exiting script...")
                    exit() # We will exit scritp because password is necessarily.
                
                if obs_pwd == "":
                    error_log("Can´t get OBS password from config.ini file!!!")
                    error_log("Maybe you let password blank.")
                    error_log("Password is necessarily. Exiting script...")
                    exit() # We will exit scritp because password is necessarily.
                    
            except Exception as e:
                error_log("Can´t get OBS password from config.ini file!!!")
                error_log(e)
                error_log("Exiting script...")
                exit()
            
            #OBS port
            try:
                #Is obs_port conf in file?
                obs_port = None
                for line in config:
                    if "obs_port" in line: # if obs_port is in line
                        obs_port = line.split("=")[1].strip() # We will take everything after =. And strip it to dont have any spaces or tabs # We will take everything after =. And strip it to dont have any spaces or tabs
                        
                        
                    
                if obs_port == None:
                    if not update_mode: error_log("Can´t find row obs_port in config.ini!!!")
                
                if obs_port == "" or obs_port == None:
                    obs_port = "4455" #Default port
                    if not update_mode: print_log("OBS port set on default (4455)")
                
                else:
                    if not str(obs_port).isdigit(): # If obs_port is not digit - default port
                        if not update_mode: error_log(f"Invalid OBS port in config: {obs_port}. OBS port set on default (4455)")
                        obs_port = "4455" #Default port
                    
            except Exception as e:
                error_log("Can´t get OBS port from config.ini file...")
                error_log(e)
                error_log("Exiting script...")
                exit()
            
            
            
            #OBS app path
            try:                
                #Is obs_app_path conf in file?
                obs_app_path = None
                for line in config:
                    if "obs_app_path" in line:  # if obs_app_path is in line
                        obs_app_path = line.split("=")[1].strip() # We will take everything after =. And strip it to dont have any spaces or tabs
                        
                        
                    
                if obs_app_path == None:
                    if not update_mode: error_log("Can´t find row obs_app_path in config.ini...")
                
                if obs_app_path == "" or obs_app_path == None:
                    obs_app_path = r"C:\Program Files\obs-studio\bin\64bit" #Default path
                    if not update_mode: print_log(r"OBS app path set on default (C:\Program Files\obs-studio\bin\64bit)")
                    
            except Exception as e:
                error_log("Can´t get OBS app path from config.ini file...")
                error_log(e)
                error_log("Exiting script...")
                exit()
            
            
            #OBS output path
            try:
                #Is obs_output_path conf in file?
                obs_output_path = None
                for line in config:
                    if "obs_output_path" in line:  # if obs_output_path is in line
                        obs_output_path = line.split("=")[1].strip() # We will take everything after =. And strip it to dont have any spaces or tabs
                        
                        
                    
                if obs_output_path == None:
                    if not update_mode: error_log("Can´t find row obs_output_path in config.ini...")
                
                if obs_output_path == "" or obs_output_path == None:
                    obs_output_path = os.path.expanduser("~\Videos") #Default path
                    if not update_mode: print_log("OBS output path set on default (user videos folder)")
                    
            except Exception as e:
                error_log("Can´t get OBS output path from config.ini file...")
                error_log(e)
                error_log("Exiting script...")
                exit()
                
                
            #Motec path
            try:           
                #Is motec_path conf in file?
                motec_path = None
                for line in config:
                    if "motec_path" in line:  # if motec_path is in line
                        motec_path = line.split("=")[1].strip() # We will take everything after =. And strip it to dont have any spaces or tabs
                        
                        
                    
                if motec_path == None:
                    if not update_mode: error_log("Can´t find row motec_path in config.ini...")
                
                if motec_path == "" or motec_path == None:
                    motec_path = "C:/MoTeC/Videos" #Default path
                    if not update_mode: print_log("Motec path set on default (C:/MoTeC/Videos)")
                    
            except Exception as e:
                error_log("Can´t get Motec path from config.ini file...")
                error_log(e)
                error_log("Exiting script...")
                exit()
                
                
            #Script loop delay
            try:
                #Is loop_delay conf in file?
                loop_delay = None
                for line in config:
                    if "loop_delay" in line:  # if loop_delay is in line
                        loop_delay = line.split("=")[1].strip() # We will take everything after =. And strip it to dont have any spaces or tabs
                        
                        
                    
                if loop_delay == None:
                    if not update_mode: error_log("Can´t find row loop_delay in config.ini...")
                
                if loop_delay == "" or loop_delay == None:
                    loop_delay = 0.1 #Default delay
                    if not update_mode: print_log("Script loop delay set on default (0.1s)")
                    
                else:
                    if not str(loop_delay).replace(".", "").isdigit():
                        if not update_mode: error_log(f"Invalid script loop delay in config: {loop_delay}. Script loop delay set on default (0.1s)")
                        loop_delay = 0.1 #Default delay
                    
            except Exception as e:
                error_log("Can´t get Script loop delay from config.ini file...")
                error_log(e)
                error_log("Exiting script...")
                exit()
              
              
              
                
            #Script logging
            try:
                #Is logging conf in file?
                logging = None
                for line in config:
                    if "logging" in line:   # if logging is in line
                        logging = line.split("=")[1].strip() # We will take everything after =. And strip it to dont have any spaces or tabs
                        
                        
                    
                if logging == None:
                    if not update_mode: error_log("Can´t find row logging in config.ini...")
                
                if logging == "" or logging == None:
                    logging = 2 #Default logging
                    if not update_mode: print_log("Logging set on default (2)")
                    
                else:
                    if not str(logging).isdigit(): # if logging is NOT number
                        if not update_mode: error_log(f"Invalid logging in config: {logging}. Logging is not digit. Logging set on default (2)")
                        logging = 2 #Default logging

                    else: # if logging IS number
                        logging = int(logging)  # than we can make int from str
                    
                        if logging != 0 or logging != 1 or logging != 2 or logging != 3: # If is not 0, 1, 2, 3 other options isnt there so we will set default value
                            if not update_mode: error_log(f"Invalid logging in config: {logging}. Logging set on default (2)")
                            logging = 2 #Default logging
                    
            except Exception as e:
                error_log("Can´t get logging from config.ini file...")
                error_log(e)
                error_log("Exiting script...")
                exit()




    # If file is not exist or if it´s failed to open or if it´s empty... Will set default configs. If in update mode. Will just return old settings because. If file is not exist we will run default setting so we dont have to update...
    if not os.path.exists("config.ini") or config == None or config == "":
        if update_mode: #If script can´t find config.ini it´s useless to update config setting because it will be same - default. So we will just return old settings.
            return Last_Config_settings
        
        # Printing errors
        if not os.path.exists("config.ini"): error_log("FILE config.ini does not exists!!!")
        if config == None: error_log("CAN´T OPEN config.ini!!!")
        if config == "": error_log("FILE config.ini IS EMPTY!!!")
        
        
            
            
        error_log("Can´t find config.ini file. Setting default settings...")
        
        
        #OBS password
        obs_pwd = input("PLEASE type OBS password>") # Password is necessarily. So we want input from terminal
        error_log("OBS password set.")
        
        ### !!!!! We want input but we might not have terminal. Have to solve
        
        #OBS port
        obs_port = 4455
        error_log("OBS port set on default (4455).")
        
        
        #OBS app path
        obs_app_path = r"C:\Program Files\obs-studio\bin\64bit"
        error_log(r"OBS app path set on default (C:\Program Files\obs-studio\bin\64bit).")
        
        
        #OBS output path to default
        obs_output_path = os.path.expanduser("~\Videos") #Default path
        error_log("OBS output path set on default (user videos folder).")
        
        
        #Motec path to default
        motec_path = "C:/MoTeC/Videos" #Default path
        error_log("Motec path set on default (C:/MoTeC/Videos).")
        
        
        #Script loop delay
        loop_delay = 0.1
        error_log("Script loop delay set on default. (0.1s)")
        
        #Logging
        logging = 2
        error_log("Logging set on default (2)")
        


    # Class with all configs
    class Config_settings:
        def __init__(self):
            self.obs_pwd = obs_pwd
            self.obs_port = obs_port
            
            self.obs_app_path = obs_app_path
            self.obs_output_path = obs_output_path
            self.motec_path = motec_path
            
            self.loop_delay = loop_delay
            self.logging = logging
    
    
    #Tell what changed... In update mode...
    if update_mode:
        if Last_Config_settings.obs_pwd != Config_settings().obs_pwd: print_log(f"Config change saved. OBS password: {Last_Config_settings.obs_pwd} >> {Config_settings().obs_pwd}")
        if Last_Config_settings.obs_port != Config_settings().obs_port: print_log(f"Config change saved. OBS port: {Last_Config_settings.obs_port} >> {Config_settings().obs_port}")
        
        if Last_Config_settings.obs_app_path != Config_settings().obs_app_path: print_log(f"Config change saved. OBS app path: {Last_Config_settings.obs_app_path} >> {Config_settings().obs_app_path}")
        if Last_Config_settings.obs_output_path != Config_settings().obs_output_path: print_log(f"Config change saved. OBS output path: {Last_Config_settings.obs_output_path} >> {Config_settings().obs_output_path}")
        if Last_Config_settings.motec_path != Config_settings().motec_path: print_log(f"Config change saved. Motec path: {Last_Config_settings.motec_path} >> {Config_settings().motec_path}")
        
        if Last_Config_settings.loop_delay != Config_settings().loop_delay: print_log(f"Config change saved. Script loop delay: {Last_Config_settings.loop_delay} >> {Config_settings().loop_delay}")
        if Last_Config_settings.logging != Config_settings().logging: print_log(f"Config change saved. Logging: {Last_Config_settings.logging} >> {Config_settings().logging}")


    return Config_settings() # Return configs



# Simple def to print configs from class
def print_from_config_class(Config_settings):
    print("OBS pwd: " + Config_settings.obs_pwd)
    print("OBS port: " + Config_settings.obs_port)
    
    print("OBS app path: " + Config_settings.obs_app_path)
    print("OBS output path: " + Config_settings.obs_output_path)
    print("Motec path: " + Config_settings.motec_path)
    
    print("Script loop delay: " + Config_settings.loop_delay)
    print(f"Logging: {Config_settings.logging}")
    
    
    
    
if __name__ == "__main__": # Testing env. You can try some def with testing inputs and get output. This will run only if it´s run in this file so if it´s imported this will not run...
    from log import set_logging, write_log, log_config_setting, print_log, error_log, cycle_log
       
    import time
    
    print("---First get---")
    Config_settings = get_config_file()
    
    #print_from_config_class(Config_settings)

    exit()
    time.sleep(2)
    
    print("---Second get (in update mode)---")
    Config_settings = get_config_file(Config_settings)
    
    print_from_config_class(Config_settings)
    