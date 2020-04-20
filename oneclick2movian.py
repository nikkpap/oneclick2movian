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

import requests
from pythonping import ping


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


class Window(Frame):
    def __init__(self, def_path, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.def_path = def_path

        # Menu Bar GUI
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label='Mode.Zip', command=self.mode_zip)
        fileMenu.add_command(label='Log.File', command=self.save_log)
        fileMenu.add_command(label='Test.IP', command=self.test_ip)
        fileMenu.add_command(label="Exit", command=self.exit_program)
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
        btn2 = Button(self, text="Choose Zip", command=self.mode_zip)
        btn2.place(x=196, y=110)
        btn3 = Button(self, text="Exit", command=self.exit_program)
        btn3.place(x=288, y=110)
        btn4 = Button(self, text="About", command=self.about)
        btn4.place(x=371, y=110)
        rad1 = Radiobutton(self, text='.Zip   ', value=1, state='enable')
        rad1.grid(column=1, row=0)
        rad2 = Radiobutton(self, text='Http://', value=2, state='enable')
        rad2.grid(column=2, row=0)

        self.lbl = Label(self, text="...")
        self.lbl.place(x=300, y=23)
        self.lb2 = Label(self, text="by nikkpap")
        self.lb2.place(x=300, y=46)
        self.txt_box1 = Entry(self, width=30)
        self.txt_box1.insert(END, '10.0.0.6')
        self.txt_box1.place(x=3, y=23)
        txt_box2 = Entry(self, width=30)
        txt_box2.insert(END, 'http://')
        txt_box2.place(x=3, y=46)
        self.port_movian = '42000'
    # def mode_url():
    #     print ("mode_url")
    #     btn2.configure(text = "Send Link", command=mode_zip)

    def mode_zip(self):

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
        self.lbl.configure(text=f'http://{ip_address}:{p}/{base_name}')

    def test_ip(self):

        ip_movian = self.txt_box1.get()
        if os.name == 'nt':
            #rep = os.system("ping -n 1 %s" % ip_movian)
            rep = str(commands.Popen(
                ["ping.exe", ip_movian], stdout=commands.PIPE).communicate()[0], 'utf-8')
            print(rep)

            if ('unreachable' in rep):
                print('server is down')
                self.lbl.configure(
                    text="No Connection... !!", background="red")
            else:
                print('server is up')
                self.lbl.configure(
                    text="Connection OK... !!", background="green")
        else:
            rep = os.system('ping -w 1 %s' % ip_movian)

            if rep == 0:
                print('server is up')
                self.lbl.configure(
                    text="Connection OK... !!", background="green")
            else:
                print('server is down')
                self.lbl.configure(
                    text="No Connection... !!", background="red")

    def save_log(self):

        ip_movian = self.txt_box1.get()

        print(ip_movian)

        try:
            response = requests.get(
                f'http://{ip_movian}:{self.port_movian}', timeout=10)
        except:
            self.lbl.configure(text="No Connection... !!")
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
        self.lbl.configure(text="Log file saved OK... !!")

    def mode_url(self):

        ext_url_base_name = self.txt_box2.get()

        if len(ext_url_base_name) >= 7:
            bnt2.configure(text="Send Link", command=mode_url)
            webbrowser.open(
                f'http://{ip_movian}:{self.port_movian}/showtime/open?url={ext_url_base_name}', new=1, autoraise=True)
            self.lbl.configure(text=f'{ext_url_base_name}')
        else:

            self.lbl.configure(
                text="Put the correct URL or use Zip mode... !!")

    def about(self):
        messagebox.showinfo(
            'About', 'Movian One Click Plugin Installer by nikkpap\n with the great help of Czz78 (thanks man)\n <<for MovianGR and Movian on Telegram>>\n ALU DEV TEAM @ 2019-20 ')

    def exit_program(self):
        server_queue.put(('stop', ''))
        os._exit(os.EX_OK)


# get my ip address
def get_ip_address():
    if platform.system == 'Linux':
        ips = commands.getoutput("hostname -I")
        ip = ips.split()[0]
    elif platform.system == 'Windows':
        ip = socket.gethostbyname(socket.gethostname())
    elif platform.system == 'Darwin':
        ip = commands.getoutput("ipconfig getifaddr en0")
    else:
        ip = ''
        print('Couldn\'t get local ip')
    return ip


if __name__ == "__main__":

    home = os.curdir
    if 'HOME' in os.environ:
        home = os.environ['HOME']
    elif platform.system == 'Linux':
        home = os.path.expanduser("~/")
    elif platform.system == 'Windows':
        if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        home = os.environ['HOMEPATH']

    ip_address = get_ip_address()
    print(ip_address)

    # Gui
    root = Tk()
    app = Window(home, root)
    root.title("Movian One Click Plugin Installer v0.5")
    root.geometry('500x150')
    root.resizable(False, False)

    server_queue = Queue.Queue()
    server_thread = ServerThread()
    server_thread.start()

    root.mainloop()
