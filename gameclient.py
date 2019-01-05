#text shooter
#By Aaron Forsyth
#Client

#keyboard press detect
bad = False
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch

getch = _find_getch()

#Main code
#NOTE: This was actually written by me
#The part above is by someone else
#It's for taking keyboard input
import socket
import time
import threading
import _thread
servername = ""
cver = "0.1"
host = input("Server to connect to: ")
name = input("Pick a name. This will be used in game to identify you: ")
port = 6301
tsl = 0
timeout = 100

def connection_lost():
    global tsl
    global timeout
    global connected
    while True:
        tsl += 1
        if tsl > timeout and not connected == True:
            print("Timeout. Reconnecting...")
            try:
                s.close()
            except:
                print("Socket closed already.")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(name.encode("utf-8") + " 2 upendmess".encode("utf-8"))
            while "endmess" not in indat:
                try:
                    indat = s.recv(1024).decode("utf-8")
                    lsdata.append(indat.replace("endmess", ""))
                except:
                    print("", end="")
        time.sleep(0.1)

class gameUpdate(object):
    """ This is some code that runs a game updating function in the background.
    The code that executes my function is not written by me.
    """

    def __init__(self, interval=0.1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            time.sleep(self.interval)
            # Do something
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(name.encode("utf-8") + " 2 none".encode("utf-8"))
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            for i in range(10):
                data = s.recv(1024).decode("utf-8")
                print(data)
            s.close()
            print("Playing on server: " + servername)
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#game = gameUpdate()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(name.encode("utf-8") + " 1 noneendmess".encode("utf-8"))
data = s.recv(1024).decode("utf-8")
if data == "Error":
    print("Error! Name Already Taken! Exiting...")
    exit()
else:
    servername = data
s.close()
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    char = getch()
    tsl = 0
    connected = False
    if char == "w":
        s.send(name.encode("utf-8") + " 2 upendmess".encode("utf-8"))
    elif char == "s":
        s.send(name.encode("utf-8") + " 2 downendmess".encode("utf-8"))
    elif char == "a":
        s.send(name.encode("utf-8") + " 2 leftendmess".encode("utf-8"))
    elif char == "d":
        s.send(name.encode("utf-8") + " 2 rightendmess".encode("utf-8"))
    elif char == "e":
        s.send(name.encode("utf-8") + " 2 shootendmess".encode("utf-8"))
    elif char == "l":
        s.send(name.encode("utf-8") + " 3 noneendmess".encode("utf-8"))
        time.sleep(0.1)
        exit()
    else:
        s.send(name.encode("utf-8") + " 2 downendmess".encode("utf-8"))
    #s.send(name.encode("utf-8") + " 2 shoot".encode("utf-8"))
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    indat = "l"
    lsdata = []
    while "endmess" not in indat:
        try:
            indat = s.recv(1024).decode("utf-8")
            lsdata.append(indat.replace("endmess", ""))
        except:
            no = 1
    connected = True
    s.close()
    otherdata = ''.join(lsdata)
    array = otherdata.split(',')
    print("-" * len(array[0]))
    for i in range(len(array) - 1):
        print("|" + array[i] + "|")
    print("-" * len(array[0]))
    print("Playing on server: " + servername, end=" ")
    print("Client Version: " + cver, end=" ")
    print("You have been hit " + str(array[len(array) - 1]) + " times")
    time.sleep(0.05)
