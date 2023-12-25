import random
import threading
from tkinter.messagebox import askokcancel
import textwrap
import pyperclip
from customtkinter import *
from tkinter.filedialog import askopenfilename
import socket
import requests
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
    askokcancel("Sorry Didn't work", "An ERROR occurred. Probably your Internet is turned off")
    quit()
print(local_ip)
def select_file():
    global PATH
    file = askopenfilename()
    if file != "":
        wrapper = textwrap.TextWrapper(width=30)
        shortened = textwrap.shorten(text=file, width=80)
        shortened_wrapped = wrapper.fill(text=shortened)
        file_lbl.configure(text=shortened_wrapped)
        PATH = file
        start_transfer.configure(state="normal")


def start():

    val = random.randint(10000, 99999)
    #os.system(f"python3 transferer.py {val} {file_lbl.cget('text')}")
    #transferer.main_password = str(val)
    #transferer.file_path = file_lbl.cget("text")
    print(f"python3 transferer.py {val} {PATH.encode('utf-8').hex()}")
    t1 = threading.Thread(target=lambda: os.system(f"python3 transferer.py {val} {PATH.encode('utf-8').hex()}"))
    t1.start()
    password_lbl.configure(text=f"Password: {val}")
    start_transfer.configure(state="disabled")
    select_file_btn.configure(state="disabled")
    stop_transfer.configure(state="normal")
    #print(transferer.app.config['SERVER_ADDR'])
    link_lbl.configure(text=f"http://{local_ip}:8000/")
    copy_link.bind("<Button-1>", copylink)
    copy_link.configure(text="Click here to copy the link")



def stop_server():
    try:
        requests.get(f"http://{local_ip}:8000/shutitdown")
    except Exception as e:
        print("Some Kind of error occured. I hope the server has successfully shut done gracefully")

    select_file_btn.configure(state="normal")
    stop_transfer.configure(state="disabled")
    copy_link.bind("<Button-1>", None)
    copy_link.configure(text="")
    password_lbl.configure(text="")
    link_lbl.configure(text="")

def copylink(e):
    pyperclip.copy(f"http://{local_ip}:8000/")

set_appearance_mode("auto")
set_default_color_theme("dark-blue")
root = CTk()
root.geometry("500x600")
root.title("File Transfer")
root.configure(fg_color=("#FCF7F8", "#2B3D41"))
root.resizable(False, False)

select_file_btn = CTkButton(root, text="Select a file", fg_color=("#4C5F6B", "#4C5F6B"), font=("SF Display", 26), width=364, height=58, hover_color=("#2B373E", "#56656F"), command=select_file)
select_file_btn.place(anchor=NW, x=68, y=89)

file_lbl = CTkLabel(root, text="Choose a file to see the path", font=("SF Display", 26), text_color=("#4C5F6B", "#FFFFFF"))
file_lbl.place(anchor=CENTER, relx=0.5, y=200)

start_transfer = CTkButton(root, text="Start Transfer", fg_color=("#4C5F6B", "#4C5F6B"), font=("SF Display", 26), width=364, height=58, hover_color=("#2B373E", "#56656F"), command=start, state="disabled")
start_transfer.place(anchor=NW, x=68, y=256)

stop_transfer = CTkButton(root, text="Stop Transfer", fg_color=("#E86252", "#E86252"), font=("SF Display", 26), width=364, height=58, hover_color=("#AD4A3E", "#E28277"), state="disabled", command=stop_server)
stop_transfer.place(anchor=NW, x=68, y=331)

link_lbl = CTkLabel(root, text="", font=("SF Display", 26), wraplength=364, text_color=("#4C5F6B", "#FFFFFF"))
link_lbl.place(anchor=CENTER, relx=0.5, y=425)

copy_link = CTkLabel(root, text="", font=("SF Display", 26), wraplength=364, text_color=("#E86252", "#E86252"))
copy_link.place(anchor=CENTER, relx=0.5, y=475)
#copy_link.bind("<Button-1>", copylink)

password_lbl = CTkLabel(root, text="", font=("SF Display", 26), wraplength=364, text_color=("#4C5F6B", "#FFFFFF"))
password_lbl.place(anchor=CENTER, relx=0.5, y=527)

root.mainloop()