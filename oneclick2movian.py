#!/usr/bin/env python3

import os
import platform
import queue as Queue
import socket
import socketserver
import subprocess as commands  # only python3
import sys
import threading
import time
import webbrowser

from http.server import HTTPServer, SimpleHTTPRequestHandler
from tkinter.filedialog import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import *

# Install via pip install -r /path/to/requirements.txt
import requests
from pythonping import ping

is_os = platform.system()

# Server Class
class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = server_queue
        self.is_server_running = False
        self.daemon = False

    def create_server(self, port=8000):
        self.server = HTTPServer((ip_address, port), SimpleHTTPRequestHandler)
        self.serv_info = self.server.socket.getsockname()

    def run(self):
        while True:
            if not self.queue.empty():
                i = self.queue.get()
                print(i)
                if i[0] == 'start':
                    self.create_server(port=int(i[1]))
                    self.is_server_running = True
                    print('SERVING @: {}:{}'.format(
                        self.serv_info[0], self.serv_info[1]))
                    self.server.serve_forever()
                elif i[0] == 'stop':
                    self.is_server_running = False
                    print('SERVER SHUTDOWN')
                    self.server = None

# Main Window Widgets
class Window(Frame):

    def __init__(self, def_path, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.def_path = def_path

    # Menu Bar GUI
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label='Mode.Zip', command=self.browse_zip)
        fileMenu.add_command(label='Log.File', command=self.save_log)
        fileMenu.add_command(label='Test.IP', command=self.test_ip)
        fileMenu.add_command(label="Exit", command=self.on_closing)
        menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menu)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        menu.add_cascade(label="Edit", menu=editMenu)

    # Commands - Buttons GUI
        self.pack(fill=BOTH, expand=1)
        btn0 = Button(self, text="Test IP", command=self.test_ip)
        btn0.place(x=10, y=110)
        btn1 = Button(self, text="Save Log", command=self.save_log)
        btn1.place(x=93, y=110)
        btn2 = Button(self, text="Choose ZIP", command=self.browse_zip)
        btn2.place(x=196, y=110)
        btn3 = Button(self, text="Exit", command=self.on_closing)
        btn3.place(x=288, y=110)
        btn4 = Button(self, text="About", command=self.about)
        btn4.place(x=371, y=110)
        rad1 = Radiobutton(self, text='.Zip   ',variable=var_toggle, value=1,
                           command=self.mode_zip) 
        rad1.grid(column=1, row=0)
        rad2 = Radiobutton(self, text='Http://',variable=var_toggle, value=2,
                           command=self.mode_url)
        rad2.grid(column=2, row=0)

        self.lb1 = Label(self, text="...")
        self.lb1.place(x=300, y=23)
        self.lb2 = Label(self)
        self.lb2.place(x=300, y=46)
        self.txt_box1 = Entry(self, width=30)
        self.txt_box1.insert(END, '10.0.0.6')
        self.txt_box1.place(x=3, y=23)
        self.txt_box2 = Entry(self, width=30)
        self.txt_box2.insert(END, 'http://')
        self.txt_box2.place(x=3, y=46)
        self.port_movian = '42000'

    def mode_zip(self):
        print("mode_zip")
        self.txt_box1.configure(state="normal")
        self.txt_box2.configure(state="disabled")
        self.txt_box1.update()
        self.txt_box2.update()
        self.lb1.configure(
                text="ZIP mode... !!")

    def mode_url(self):
        print("mode_url")
        self.txt_box1.configure(state="disabled")
        self.txt_box2.configure(state="normal")
        self.txt_box1.update()
        self.txt_box2.update()
        self.lb1.configure(
                text="URL mode... !!")


        # self.btn2.configure(text="Send Link", command=self.mode_url)
        # self.btn2.update()



    def manual_url(self):

        ext_url_base_name = self.txt_box2.get()

        if len(ext_url_base_name) >= 7:
            
            webbrowser.open(
                f'http://{ip_movian}:{self.port_movian}/showtime/open?url={ext_url_base_name}', new=1, autoraise=True)
            self.lb1.configure(text=f'{ext_url_base_name}')
        else:
            self.lb1.configure(
                text="Put the correct URL or use Zip mode... !!")

    def browse_zip(self):

        ip_movian = self.txt_box1.get()
        name = askopenfilename(initialdir="" + self.def_path, filetypes=(
            ("Zip File", "*.zip"), ("All Files", "*.*")), title="Choose Zip Plugin")
        dir_to_server = os.path.dirname(name)
        base_name = os.path.basename(name)
        os.chdir(dir_to_server)

        port = 0
        server_queue.put(('start', port))
        # wait for the server_thread to switch is_server_running = True
        while not server_thread.is_server_running:
            pass
        p = server_thread.serv_info[1]

        webbrowser.open(
            f'http://{ip_movian}:{self.port_movian}/showtime/open?url=http://{ip_address}:{p}/{base_name}', new=1, autoraise=True)
        self.lb1.configure(text=f'http://{ip_address}:{p}/{base_name}')

    def test_ip(self):

        ip_movian = self.txt_box1.get()
        if is_os == 'Windows':
            test_ping = str(commands.Popen(
                ["ping.exe", ip_movian], stdout=commands.PIPE).communicate()[0], 'utf-8')
            print(test_ping)

            if ('unreachable' in test_ping):
                print('server is down')
                self.lb1.configure(
                    text="No Connection... !!")
                self.lb2.configure(
                    background="red", width=2)
            else:
                print('server is up')
                self.lb1.configure(
                    text="Connection OK... !!")
                self.lb2.configure(
                    background="green",  width=2)

        elif is_os == 'Linux':
            test_ping = os.system('ping -w 1 %s' % ip_movian)

            if test_ping == 0:
                print('server is up')
                self.lb1.configure(
                    text="Connection OK... !!")
                self.lb2.configure(
                    background="green",  width=2)
            else:
                print('server is down')
                self.lb1.configure(
                    text="No Connection... !!")
                self.lb2.configure(
                    background="red", width=2)
        else:
            # need test ping on Darwin !!!!!!!!!!
            print('OS is Darwin')
            self.lb1.configure(
                text="OS is Darwin")

    def save_log(self):

        ip_movian = self.txt_box1.get()

        print(ip_movian)

        try:
            response = requests.get(
                f'http://{ip_movian}:{self.port_movian}', timeout=10)
        except:
            self.lb1.configure(text="No Connection... !!")
            return

        url_movian = (f'http://{ip_movian}:{self.port_movian}')
        recieve = requests.get(f'{url_movian}/api/logfile/0')
        f = asksaveasfile(mode='wb', filetypes=(
            ("Log File", "*.log"), ("All Files", "*.*")), title="Save Log File")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            print("askforfile failed")
            return
        f.write(recieve.content)
        f.close()
        print('Log file saved OK... !')
        self.lb1.configure(text="Log file saved OK... !!")

    def about(self):
        messagebox.showinfo(
            'About', 'Movian One Click Plugin Installer by nikkpap\n with the great help of Czz78 (thanks man)\n <<for MovianGR and Movian on Telegram>>\n ALU DEV TEAM @ 2019-20 ')

    def exit_program(self):
        server_queue.put(('stop', ''))
        os._exit(os.EX_OK)

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Do you want to quit..?"):
            self.exit_program



# get my ip address
def get_ip_address():
    if is_os == 'Linux':
        ips = commands.getoutput("hostname -I")
        ip = ips.split()[0]
    elif is_os == 'Windows':
        ip = socket.gethostbyname(socket.gethostname())
    elif is_os == 'Darwin':
        ip = commands.getoutput("ipconfig getifaddr en0")
    else:
        ip = ''
        print('Couldn\'t get local ip')
    return ip


# Main app
if __name__ == "__main__":
    home = os.curdir
    if 'HOME' in os.environ:
        home = os.environ['HOME']
    elif is_os == 'Linux':
        home = os.path.expanduser("~/")
    elif is_os == 'Windows':
        if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    elif is_os == 'Darwin':
        print('OS is Darwin')
        self.lb1.configure(
            text="OS is Darwin")
        # home = os.path.expanduser("~/") ????????
    else:
        home = os.environ['HOMEPATH']

ip_address = get_ip_address()
print(ip_address)


# Start Server
server_queue = Queue.Queue()
server_thread = ServerThread()
server_thread.start()

# Gui
root = Tk()

var_toggle = StringVar()
var_toggle.set(1)

app = Window(home, root)
root.title("Movian One Click Plugin Installer v0.6")
root.geometry('500x150')
root.resizable(False, False)

root.mainloop()
