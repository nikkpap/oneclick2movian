####################################################################
# Import modules
####################################################################
import requests
import http.server
import socketserver
import os
import socket
import webbrowser
import threading
import time
import platform
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter.ttk import *
from pythonping import ping


# Initialize first window0
window0 = Tk()

####################################################################
# Variable Declarations
####################################################################
window0.title("Movian One Click Plugin Installer v0.1")
window0.geometry('450x150')
window0.resizable(False, False)
lbl = Label(window0, text="Movian IP")
lbl.place(x=200, y=23)
lb2 = Label(window0, text="by nikkpap")
lb2.place(x=200, y=46)
txt_box1 = Entry(window0, width=30)
txt_box1.insert(END, '192.168.8.100')
txt_box1.place(x=3, y=23)
txt_box2 = Entry(window0, width=30)
txt_box2.insert(END, 'http://')
txt_box2.place(x=3, y=46)
is_windows = any(platform.win32_ver())

#########################END OF GUI ################################
#print("Your Computer IP Address is: " + IPAddr)
ip_movian = txt_box1.get()
port_movian = '42000'
url_movian = (f'http://{ip_movian}:{port_movian}')
period_of_time = 3  # sec
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
def_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket

####################################################################
# Functions
####################################################################

# File manager function


def OpenFile():

    name = askopenfilename(initialdir="" + def_path, filetypes=(
        ("Zip File", "*.zip"), ("All Files", "*.*")), title="Choose a Plugin")
    dir_to_server = os.path.dirname(name)
    base_name = os.path.basename(name)
    startHTTPServer(dir_to_server)
    webbrowser.open(f'{url_movian}/?url=http://{IPAddr}:8080/{base_name}')
    # Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name, 'r') as UseFile:
            print(UseFile.read())
    except:
        messagebox.showinfo('Error', 'Cancel')


def startHTTPServer(dir_to_server):
    PORT = 8080
    os.chdir(dir_to_server)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    # webbrowser.open(f'{url_movian}/?url=http://{IPAddr}:8080/torrent.zip') ????????????
    # can i use a timer to stop the server after 5 sec
    httpd.serve_forever()


def test_ip():
    rep = os.system('ping ' + ip_movian)
    if rep == 0:
        print('server is up')
        lbl.configure(text="Connection Established... !!")
    else:
        print('server is down')
        lbl.configure(text="No Connection... !!")


def down_log():
    response = requests.get(f'http://{ip_movian}:{port_movian}')
    if response:
        print('Download OK... !')
        recieve = requests.get(f'{url_movian}/api/logfile/0?mode=download')
        with open(f'{def_path}\movian0.log', 'wb') as fo:
            fo.write(recieve.content)
        lbl.configure(text="Download OK... !!")
    else:
        # print('An error has occurred.')
        lbl.configure(text="No Connection... !!")


def install_plugin():
    lbl.configure(text="Not yet... !!")


def about():
    messagebox.showinfo(
        'About', 'Movian One Click Plugin Installer by nikkpap @ 2019')

####################################################################
    # Menu Bar GUI
####################################################################


menu = Menu(window0)
window0.config(menu=menu)

file = Menu(menu)
file.add_command(label='Open', command=OpenFile)
file.add_command(label='D.Log', command=down_log)
file.add_command(label='Test.IP', command=test_ip)
file.add_command(label='Exit', command=lambda: exit())
menu.add_cascade(label='File', menu=file)

####################################################################
# Commands - Buttons GUI
####################################################################

btn0 = Button(window0, text="Test IP", command=test_ip)
btn0.place(x=10, y=110)
btn1 = Button(window0, text="Download Log", command=down_log)
btn1.place(x=90, y=110)
btn2 = Button(window0, text="Choose Path", command=OpenFile)
btn2.place(x=180, y=110)
btn3 = Button(window0, text="Exit", command=exit)
btn3.place(x=260, y=110)
btn4 = Button(window0, text="About", command=about)
btn4.place(x=340, y=110)
rad1 = Radiobutton(window0, text='.Zip   ', value=1, state='enable')
rad1.grid(column=1, row=0)
rad2 = Radiobutton(window0, text='Http://', value=2, state='enable')
rad2.grid(column=2, row=0)


window0.mainloop()
####################################################################
# EOF
####################################################################
