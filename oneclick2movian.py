#!/usr/bin/env python

import requests
import socketserver
import os
import socket
import webbrowser
import threading
import time
import platform
import threading
import queue as Queue
import subprocess as commands # only python3
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
from tkinter import messagebox
from tkinter.ttk import *
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
                    print('SERVING @: {}:{}'.format(self.serv_info[0],self.serv_info[1]))
                    self.server.serve_forever()
                elif i[0] == 'stop':
                    self.is_server_running=False
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
        fileMenu.add_command(label='Open', command=self.OpenFile)
        fileMenu.add_command(label='D.Log', command=self.down_log)
        fileMenu.add_command(label='Test.IP', command=self.test_ip)
        fileMenu.add_command(label="Exit", command=self.exitProgram)
        menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menu)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        menu.add_cascade(label="Edit", menu=editMenu)

        # Commands - Buttons GUI
        self.pack(fill=BOTH, expand=1)
        btn0 = Button(self, text="Test IP", command=self.test_ip)
        btn0.place(x=10, y=110)
        btn1 = Button(self, text="Download Log", command= self.down_log)
        btn1.place(x=93, y=110)
        btn2 = Button(self, text="Choose Path", command= self.OpenFile)
        btn2.place(x=196, y=110)
        btn3 = Button(self, text="Exit", command=self.exitProgram)
        btn3.place(x=288, y=110)
        btn4 = Button(self, text="About", command=self.about)
        btn4.place(x=371, y=110)
        rad1 = Radiobutton(self, text='.Zip   ', value=1, state='enable')
        rad1.grid(column=1, row=0)
        rad2 = Radiobutton(self, text='Http://', value=2, state='enable')
        rad2.grid(column=2, row=0)

        self.lbl = Label(self, text="Movian IP")
        self.lbl.place(x=300, y=23)
        self.lb2 = Label(self, text="by nikkpap")
        self.lb2.place(x=300, y=46)
        self.txt_box1 = Entry(self, width=30)
        self.txt_box1.insert(END, '192.168.8.100')
        self.txt_box1.place(x=3, y=23)
        txt_box2 = Entry(self, width=30)
        txt_box2.insert(END, 'http://')
        txt_box2.place(x=3, y=46)
        self.port_movian = '42000'


    def OpenFile(self):

        ip_movian = self.txt_box1.get()
        name = askopenfilename(initialdir="" + self.def_path, filetypes=(("Zip File", "*.zip"), ("All Files", "*.*")), title="Choose a Plugin")
        dir_to_server = os.path.dirname(name)
        base_name = os.path.basename(name)
        os.chdir(dir_to_server)

        port=0
        server_queue.put(('start', port))
        # wait for the server_thread to switch is_server_running = True
        while not server_thread.is_server_running:
            pass
        p = server_thread.serv_info[1]

        webbrowser.open(f'http://{ip_movian}:{self.port_movian}/showtime/open?url=http://{ip_address}:{p}/{base_name}', new=1, autoraise=True)
        self.lbl.configure(text=f'http://{ip_address}:{p}/{base_name}')


    def test_ip(self):

        ip_movian = self.txt_box1.get()

        if os.name == 'nt':
            rep = str(subprocess.Popen(["ping.exe",ip_movian],stdout = subprocess.PIPE).communicate()[0], 'utf-8')
            print(rep)

            if ('unreachable' in rep):
                print('server is down')
                self.lbl.configure(text="No Connection... !!")
            else: 
                print('server is up')
                self.lbl.configure(text="Connection Established... !!")
        else :
            rep = os.system('ping -w 1 %s' % ip_movian)

            if rep == 0:
                print('server is up')
                self.lbl.configure(text="Connection Established... !!")
            else:
                print('server is down')
                self.lbl.configure(text="No Connection... !!")



    def down_log(self):

        ip_movian = self.txt_box1.get()

        print (ip_movian)

        try:
            response = requests.get(f'http://{ip_movian}:{self.port_movian}', timeout=10 )
        except:
            self.lbl.configure(text="No Connection... !!")
            return

        url_movian = (f'http://{ip_movian}:{self.port_movian}')
        recieve = requests.get(f'{url_movian}/api/logfile/0')
        f = asksaveasfile(mode='wb' , defaultextension='*.*')
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            print("askforfile failed")
            return
        f.write(recieve.content)
        f.close()
        print('Download OK... !')
        self.lbl.configure(text="Download OK... !!")

    def install_plugin(self):
        self.lbl.configure(text="Not yet... !!")


    def about(self):
        messagebox.showinfo('About', 'Movian One Click Plugin Installer by nikkpap @ 2019')


    def exitProgram(self):
        server_queue.put(('stop', ''))
        os._exit(os.EX_OK)





# get my ip address
def get_ip_address():
    if os.name == 'posix':
        ip = commands.getoutput("hostname -I")
    elif os.name == 'nt':
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = ''
        print('Couldn\'t get local ip')
    return ip



if __name__ == "__main__":

    home = os.curdir
    if 'HOME' in os.environ:
        home = os.environ['HOME']
    elif os.name == 'posix':
        home = os.path.expanduser("~/")
    elif os.name == 'nt':
        if 'HOMEPATH' in os.environ and 'HOMEDRIVE' in os.environ:
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        home = os.environ['HOMEPATH']



    ip_address = get_ip_address().split()[0]

    print(ip_address)


    # Gui
    root = Tk()
    app = Window(home, root)
    root.title("Movian One Click Plugin Installer v0.2")
    root.geometry('600x300')
    root.resizable(False, False)


    server_queue = Queue.Queue()
    server_thread = ServerThread()
    server_thread.start()

    root.mainloop()


