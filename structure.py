import threading

event = threading.Event()

def worker():
    print("Čekám...")
    event.wait()  # tady to čeká bez CPU zatížení
    print("Událost nastala!")

t = threading.Thread(target=worker)
t.start()

input("Stiskni Enter...")
event.set()  # vyvolá event