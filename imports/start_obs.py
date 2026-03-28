import subprocess

def main():

    subprocess.Popen(
        ["obs64.exe", "--minimize-to-tray"],
        cwd=r"C:\Program Files\obs-studio\bin\64bit",
        shell=True
    )