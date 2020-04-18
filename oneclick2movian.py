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
import threading
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *
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
        self.http_server_started = False


    def OpenFile(self):

        ip_movian = self.txt_box1.get()
        name = askopenfilename(initialdir="" + self.def_path, filetypes=(("Zip File", "*.zip"), ("All Files", "*.*")), title="Choose a Plugin")
        dir_to_server = os.path.dirname(name)
        base_name = os.path.basename(name)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get a free port
        s.bind(('', 0))
        addr, port = s.getsockname()
        s.close()

        if not self.http_server_started:

            shs = self.startHTTPServer;
            daemon = threading.Thread(target=shs , args=(dir_to_server, port))
            #daemon.setDaemon(True) # Set as a daemon so it will be killed once the main thread is dead.
            daemon.start()

            webbrowser.open(f'http://{ip_movian}:{self.port_movian}/showtime/open?url=http://{addr}:{port}/{base_name}', new=1, autoraise=True)
            self.lbl.configure(text=f'http://{ip_movian}:{self.port_movian}/showtime/open?url=http://{self.myip}:{port}/{base_name}')


    def startHTTPServer(self,dir_to_server, port):

        os.chdir(dir_to_server)
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(('', port), Handler)
        print("serving at port", port)
        httpd.serve_forever()


    def test_ip(self):

        ip_movian = self.txt_box1.get()
        if os.name == 'nt':
            rep = os.system("ping -n 1 %s" % ip_movian)
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
        exit()




def main():

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


    # Socket
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket

    # Gui
    root = Tk()
    app = Window(home, root)
    root.title("Movian One Click Plugin Installer v0.2")
    root.geometry('600x300')
    root.resizable(False, False)
    root.mainloop()



if __name__ == "__main__":
    main()

