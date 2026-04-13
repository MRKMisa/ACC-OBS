import datetime, os


global file_name
now = datetime.datetime.now()
file_name = f'{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'

global logging
logging = 0 # Default


# Only write log. Mainly for defs below. But it can be maybe used in code.
def write_log(log):
    global file_name # Get file name
    
    try:
        with open(f"logs/{file_name}", "a") as f:
            f.write(log)
    except Exception as e:
        print(f"Can´t log to file: logs/{file_name}")
        print(e)


# Log for errors will print string and write to log file if logging is 1 or more...
def error_log(string):
    global logging
    print(string)
    
    if logging >= 1: write_log(f"{string}\n")

# Log for basics prints will print string and write to log file if logging 2 or more...
def print_log(string):
    global logging
    print(string)
    
    if logging >= 2: write_log(f"{string}\n")

# Log for cycle prints will print string and write to log file if logging is 3 (It can be annoying for basic use. So it´s for debuging)...
def cycle_log(string):
    global logging
    
    if logging >= 3:
        print(string)
        write_log(f"{string}\n") 
        









# Settup logging rate from the script. If not called default 0
def set_logging(inp_logging):
    global logging
    
    logging = inp_logging
    
    if logging == 0: 
        print("Logging set to none...")
        return
    
    if logging == 1: mess = f"Logging set to only errors..."
    if logging == 2: mess = f"Logging set to errors and basics prints..."
    if logging == 3: mess = f"Logging set to errors, basics prints and cycles prints..."
    
    print(mess)
    
    
    write_log(mess + "\n")



# Clear old logs allways called in import
def clear_last_logs(max_logs=10):
    files = os.listdir("./logs") # Get logs
    
    logs_num = len(files)
    
    print_log(f"Records count: {logs_num}/{max_logs}")
    
    if logs_num > max_logs:
        error_log(f"Deleting last {logs_num-max_logs} logs")
        for i, last_file in enumerate(files):
            if (logs_num-i) > max_logs:
                try:
                    os.remove(f"./logs/{last_file}")
                    error_log(f"REMOVED log numer: {logs_num-i} file name: {last_file}")
                except Exception as e:
                    error_log(f"CAN´T REMOVE log number: {logs_num-i} file name: {last_file}!!!")
                    error_log(e) 
clear_last_logs() #Removing old logs







# Only def to log setting from Config class. But only if logging is 2 or more
def log_config_setting(Config_settings):
    global logging
    
    if logging >= 2:
        write_log("\n")
        
        write_log("---Config settings---\n")
        
        
        write_log("OBS pwd: " + Config_settings.obs_pwd + "\n")
        write_log("OBS port: " + Config_settings.obs_port + "\n")
        
        write_log("OBS app path: " + Config_settings.obs_app_path + "\n")
        write_log("OBS output path: " + Config_settings.obs_output_path + "\n")
        write_log("Motec path: " + Config_settings.motec_path + "\n")
        
        write_log("Script loop delay: " + Config_settings.loop_delay)
        
        
        
        write_log("\n")



     
                
    


if __name__ == "__main__": # Testing env. You can try some def with testing inputs and get output. This will run only if it´s run in this file so if it´s imported this will not run...
   
    set_logging(2)
    
    
    print_log("a")
    
    error_log("b")