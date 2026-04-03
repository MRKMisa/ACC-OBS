import subprocess

def main(cwd=r"C:\Program Files\obs-studio\bin\64bit"):

    subprocess.Popen(
        ["obs64.exe", "--minimize-to-tray"],
        cwd=cwd,
        shell=True
    )
    
    
if __name__ == "__main__":
    #Get obs_app_path from config.ini
    import config
    
    
    Config_settings = config.get_config_file()
    #cwd=r"C:\Program Files\obs-studio\bin\64bit"
    
    
    main(Config_settings.obs_app_path)