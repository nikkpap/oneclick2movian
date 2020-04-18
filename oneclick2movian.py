####################################################################
# Import modules
####################################test################################
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
        btn1 = Button(self, text="Download Log", command=self.down_log)
        btn1.place(x=93, y=110)
        btn2 = Button(self, text="Choose Path", command=self.OpenFile)
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
        #ip_movian = self.txt_box1.get()
        self.port_movian = '42000'
        #url_movian = (f'http://{ip_movian}:{self.port_movian}')
        #period_of_time = 3  # sec


    def OpenFile(self):

        name = askopenfilename(initialdir="" + self.def_path, filetypes=(("Zip File", "*.zip"), ("All Files", "*.*")), title="Choose a Plugin")
        dir_to_server = os.path.dirname(name)
        base_name = os.path.basename(name)
        self.startHTTPServer(dir_to_server)
        webbrowser.open(f'{self.url_movian}/?url=http://{IPAddr}:8080/{base_name}')
        # Using try in case user types in unknown file or closes without choosing a file.
        try:
            with open(name, 'r') as UseFile:
                print(UseFile.read())
        except:
            self.messagebox.showinfo('Error', 'Cancel')


    def startHTTPServer(self,dir_to_server):

        PORT = 8080
        os.chdir(dir_to_server)
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        print("serving at port", PORT)
        # webbrowser.open(f'{url_movian}/?url=http://{IPAddr}:8080/torrent.zip') ????????????
        # can i use a timer to stop the server after 5 sec
        httpd.serve_forever()


    def test_ip(self):

        ip_movian = self.txt_box1.get()

        rep = os.system('ping -w 1 ' + ip_movian)
        if rep == 0:
            print('server is up')
            self.lbl.configure(text="Connection Established... !!")
        else:
            print('server is down')
            self.lbl.configure(text="No Connection... !!")


    def down_log(self):

        ip_movian = self.txt_box1.get()

        try:
            response = requests.get(f'http://{ip_movian}:{self.port_movian}', timeout=5 )
            if response:
                print('Download OK... !')
                url_movian = (f'http://{ip_movian}:{self.port_movian}')
                recieve = requests.get(f'{url_movian}/api/logfile/0?mode=download')
                with open(f'{self.def_path}\movian0.log', 'wb') as fo:
                    fo.write(recieve.content)
                self.lbl.configure(text="Download OK... !!")
        except:
            self.lbl.configure(text="No Connection... !!")


    def install_plugin(self):
        self.lbl.configure(text="")
        self.lbl.configure(text="Not yet... !!")


    def about(self):
        messagebox.showinfo('About', 'Movian One Click Plugin Installer by nikkpap @ 2019')


    def exitProgram(self):
        exit()





# check if is windows
is_windows = any(platform.win32_ver())

# Default path
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

# we need to fix the path for linux/unix
def_path = os.path.join(os.path.join(home), 'Desktop')


# Socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket


# Gui
root = Tk()
app = Window(def_path,root)
root.title("Movian One Click Plugin Installer v0.2")
root.geometry('600x300')
root.resizable(False, False)
root.mainloop()

