import random
import threading
import pyperclip
import socket
import requests
import rumps
import subprocess
import os


PATH = None
def get_local_ip():
    try:
        # Create a socket to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Connect to a known external server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return None

local_ip = get_local_ip()
if local_ip == None:
    rumps.alert("An ERROR occurred. Probably your Internet is turned off")
    quit()


@rumps.clicked("Select File")
def select_file(_):
    global PATH
    cmd = b"""choose file with prompt "Please select a file to transfer" """
    proc = subprocess.Popen(["osascript", '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    file_path, _ = proc.communicate(cmd)
    print(file_path)
    file_path = file_path.decode("utf-8").replace("alias Macintosh HD", '').replace('\n', '').replace(':', '/')
    if proc.returncode == 0:
        print(file_path)
        PATH = file_path
        app.menu["Start Transfer"].set_callback(start)



@rumps.clicked("Start Transfer")
def start(_):

    val = random.randint(10000, 99999)
    #os.system(f"python3 transferer.py {val} {file_lbl.cget('text')}")
    #transferer.main_password = str(val)
    #transferer.file_path = file_lbl.cget("text")
    print(f"python3 transferer.py {val} {PATH.encode('utf-8').hex()}")
    t1 = threading.Thread(target=lambda: os.system(f"python3 transferer.py {val} {PATH.encode('utf-8').hex()}"))
    t1.start()

    app.menu["Pwd: None"].title = f"Pwd: {val}"
    app.menu["Select File"].set_callback(None)
    app.menu["Stop Transfer"].set_callback(stop_server)
    app.menu["Start Transfer"].set_callback(None)
    app.menu["Link: None"].title = f"Link: http://{local_ip}:8000/"
    app.menu["Link: None"].set_callback(copylink)



@rumps.clicked("Stop Transfer")
def stop_server(_):
    try:
        requests.get(f"http://{local_ip}:8000/shutitdown")
    except Exception as e:
        print("Some Kind of error occured. I hope the server has successfully shut done gracefully")
    app.menu["Select File"].set_callback(select_file)

    app.menu["Start Transfer"].set_callback(None)
    app.menu["Stop Transfer"].set_callback(None)
    app.menu["Link: None"].title = "Link: None"
    app.menu["Link: None"].set_callback(None)
    app.menu["Pwd: None"].title = "Pwd: None"



def copylink(_):
    pyperclip.copy(f"http://{local_ip}:8000/")

@rumps.events.before_start.register
def before_start():
    #app.menu['Action'].state = 1
    app.menu["Start Transfer"].set_callback(None)
    app.menu["Stop Transfer"].set_callback(None)

if __name__ == "__main__":
    app = rumps.App("File Transfer", menu=["Select File", "Start Transfer", "Stop Transfer", "Pwd: None", "Link: None"], quit_button=None)
    app.run()

