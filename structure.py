import datetime, os, time
  
  
def main():
    print("Main")


def event():
    now = datetime.datetime.now() 
    return now.microsecond//100000 == 0


def run(d=0.01):
    while True:
        if event():
            main()
        else:
            os.system("cls")
            
        time.sleep(d)
            


run()