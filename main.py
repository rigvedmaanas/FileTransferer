import random
import threading
from tkinter.messagebox import askokcancel
import textwrap

import PIL
import pyperclip
from customtkinter import *
from tkinter.filedialog import askopenfilename
import socket
import requests
import qrcode


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
    img = qrcode.make(f"http://{local_ip}:8000/")

    root.img = PIL.ImageTk.PhotoImage(img)

    qr_lbl.configure(image=root.img)


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
    qr_lbl.configure(image="")


def copylink(e):
    pyperclip.copy(f"http://{local_ip}:8000/")

set_appearance_mode("auto")
set_default_color_theme("Extreme/extreme.json")
root = CTk()
root.geometry("854x600+100+100")
root.title("File Transferer")
root.configure()
#root.resizable(False, False)



control_panel = CTkFrame(root)
control_panel.pack(padx=10, pady=10, expand=True, fill="both", side="left")

QR_panel = CTkFrame(root, width=400)
QR_panel.pack(padx=(0, 10), pady=10, expand=True, fill="y", side="left")

qr_lbl = CTkLabel(QR_panel, text="")
qr_lbl.place(anchor=CENTER, relx=0.5, rely=0.5)

select_file_btn = CTkButton(control_panel, text="Select a file", font=CTkFont(size=26), width=364, height=58, command=select_file)
select_file_btn.pack(padx=20, pady=20)

file_lbl = CTkLabel(control_panel, text="Choose a file to see the path", font=CTkFont(size=26))
file_lbl.pack(padx=20, pady=20)

start_transfer = CTkButton(control_panel, text="Start Transfer", font=CTkFont(size=26), width=364, height=58, command=start, state="disabled")
start_transfer.pack(padx=20, pady=20)

stop_transfer = CTkButton(control_panel, text="Stop Transfer", fg_color=("#E86252", "#E86252"), font=("SF Display", 26), width=364, height=58, hover_color=("#AD4A3E", "#E28277"), state="disabled", text_color_disabled=("grey40", "grey40"), command=stop_server)
stop_transfer.pack(padx=20, pady=20)

link_lbl = CTkLabel(control_panel, text="", font=("SF Display", 26), wraplength=364, text_color=("#4C5F6B", "#FFFFFF"))
link_lbl.pack(padx=20, pady=20)

copy_link = CTkLabel(control_panel, text="", font=("SF Display", 26), wraplength=364, text_color=("#E86252", "#E86252"))
copy_link.pack(padx=20, pady=10)

password_lbl = CTkLabel(control_panel, text="", font=("SF Display", 26), wraplength=364, text_color=("#4C5F6B", "#FFFFFF"))
password_lbl.pack(padx=20, pady=10)

def on_closing():
    try:
        requests.get(f"http://{local_ip}:8000/shutitdown")
    except Exception as e:
        print("Some Kind of error occured. I hope the server has successfully shut done gracefully")

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()