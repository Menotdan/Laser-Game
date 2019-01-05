
#text shooter
#By Aaron Forsyth
#Server

import socket
import _thread
import time
hostname = socket.gethostname()    
IPAddr = '' #socket.gethostbyname(hostname)
dIP = socket.gethostbyname(hostname)
servername = input("Enter a name for the server(This will be displayed to the players): ")
try:
    maxX = int(input("Max X: ")) - 1
    maxY = int(input("Max Y: ")) - 1
except:
    maxX = 59
    maxY = 19
pnames = []
lmove = []
px = []
py = []
lx = []
ly = []
phits = []
rows = []
ldir = []
dataw = []
indata = ""
included = False
def loadrows():
    global rows
    rows = []
    global maxX
    global maxY
    global px
    global py
    global lx
    global ly
    global ldir
    for y in range(maxY):
        #load renderings
        row = []
        for q in range(maxX):
            row.append(" ")
        for m in range(maxX):
            for a in range(len(lx)):
                try:
                    if lx[a] == m and ly[a] == y:
                        if ldir[a] == "up" or ldir[a] == "down":
                            row[m] = "|"
                        else:
                            row[m] = "-"
                except:
                    print("Glitch handled")
            for b in range(len(pnames)):
                if px[b] == m and py[b] == y:
                    row[m] = "#"
        #print(''.join(row))
        rows.append(''.join(row))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IPAddr, 6301))
print("Server now listening on: " + dIP)
def onclient(conn,addr):
    global maxX
    global maxY
    global px
    global py
    global lx
    global ly
    global ldir
    global lmove
    global pnames
    global phit
    global servername
    global included

    dataw = []
    print("Data request from: " + str(addr))
    blah = []
    finalst = ""
    while "endmess" not in finalst:
        blah.append(conn.recv(1024).decode("utf-8"))
        finalst = ''.join(blah)
    indata = finalst.replace("endmess", "") #conn.recv(1024).decode("utf-8")
    print(indata)
    dataw = indata.split(" ")
    print(dataw)
    for i in range(len(dataw)):         #data handling
        if i == 0:
            for l in range(len(pnames)):
                if dataw[1] == "1":
                    if dataw[0] == pnames[l]:
                        included = True
                        print("WHATATATATATATAAA")
                        break
            if dataw[1] == "1":
                if included == False:
                    print(dataw[0] + " is not already in game, adding")
                    pnames.append(dataw[0])
                    px.append(5)
                    py.append(5)
                    lmove.append("right")
                    phits.append(0)
                    print(str(time.time()) + " DEBUG: Server sending")
                    #time.sleep(0.1)
                    conn.send(servername.encode("utf-8"))

                
        if i == 1:
            if dataw[i] == "1": #if trying to connect
                if included == True:
                    included = False
                    print(str(time.time()) + " DEBUG: Server sending")
                    conn.send("Error".encode("utf-8"))
                    break
            if dataw[i] == "2": #if already connected
                #Detecting actions sent by the client
                if dataw[2] == "up":
                    #loadrows()
                    #conn.send(','.join(rows).encode("utf-8"))
                    if py[pnames.index(dataw[0])] != 0:
                        py[pnames.index(dataw[0])] -= 1
                        #print(py[pnames.index(dataw[0])])
                        #print(pnames.index(dataw[0]))
                        #print(dataw[0])
                        lmove[pnames.index(dataw[0])] = "up"
                elif dataw[2] == "down":
                    #loadrows()
                    #conn.send(','.join(rows).encode("utf-8"))
                    if py[pnames.index(dataw[0])] != maxY - 1:
                        py[pnames.index(dataw[0])] += 1
                        lmove[pnames.index(dataw[0])] = "down"
                elif dataw[2] == "left":
                    #loadrows()
                    #conn.send(','.join(rows).encode("utf-8"))
                    if px[pnames.index(dataw[0])] != 0:
                        px[pnames.index(dataw[0])] -= 1
                        lmove[pnames.index(dataw[0])] = "left"
                elif dataw[2] == "right":
                    #loadrows()
                    #conn.send(','.join(rows).encode("utf-8"))
                    if px[pnames.index(dataw[0])] != maxX - 1:
                        px[pnames.index(dataw[0])] += 1
                        lmove[pnames.index(dataw[0])] = "right"
                elif dataw[2] == "shoot":    #Get the direction to move the laser
                    
                    if lmove[pnames.index(dataw[0])] == "up":
                        lx.append(px[pnames.index(dataw[0])])
                        ly.append(py[pnames.index(dataw[0])] - 1)
                        ldir.append("up")
                    elif lmove[pnames.index(dataw[0])] == "down":
                        lx.append(px[pnames.index(dataw[0])])
                        ly.append(py[pnames.index(dataw[0])] + 1)
                        ldir.append("down")
                    elif lmove[pnames.index(dataw[0])] == "left":
                        lx.append(px[pnames.index(dataw[0])] - 1)
                        ly.append(py[pnames.index(dataw[0])])
                        ldir.append("left")
                    elif lmove[pnames.index(dataw[0])] == "right":
                        lx.append(px[pnames.index(dataw[0])] + 1)
                        ly.append(py[pnames.index(dataw[0])])
                        ldir.append("right")
                    else:
                        print("WTF HAPPEND")
                #elif dataw[2] == "none":
                    #loadrows()
                    #conn.send(','.join(rows).encode("utf-8"))
            if dataw[i] == "3": #disconnect
                del px[pnames.index(dataw[0])]
                del py[pnames.index(dataw[0])]
                del lmove[pnames.index(dataw[0])]
                del phits[pnames.index(dataw[0])]
                del pnames[pnames.index(dataw[0])]
            if dataw[i] == "4": #would be chat
                print("No")
    for garbagedump in range(len(ly)):
        if garbagedump + 1 >= len(ly):
            if ly[garbagedump] - 1 >= maxY or ly[garbagedump] + 1 <= 0 or lx[garbagedump] + 1 <= 0 or lx[garbagedump] - 1 >= maxX:
                del ly[garbagedump]
                del lx[garbagedump]
                del ldir[garbagedump]
                print("laser deleted")
    for x in range(len(ly)):
        #move lasers
        #print(x)
        if ldir[x] == "up":
            ly[x] -= 1
        elif ldir[x] == "down":
            ly[x] += 1
        elif ldir[x] == "left":
            lx[x] -= 1
        elif ldir[x] == "right":
            lx[x] += 1
    for lascol in range(len(pnames)):
        for las in range(len(ldir)):
            if py[lascol] == ly[las] and px[lascol] == lx[las]:
                phits[lascol] += 1
    
    #loadrows()
    #for f in range(len(rows)):
    #    conn.send(rows[f].encode("utf-8"))
    #conn.send(str(shots).encode("utf-8"))
    loadrows()
    try:
        print(str(time.time()) + " DEBUG: Server sending")
        #time.sleep(0.1)
        conn.send(','.join(rows).encode("utf-8") + ",".encode("utf-8") + str(phits[pnames.index(dataw[0])]).encode("utf-8"))
        conn.send('endmess'.encode("utf-8"))
        #conn.close()
    except:
        print("Player disconnected: " + dataw[0])
    #try:
    #    print(str(time.time()) + " DEBUG: Server closing")
    #    conn.close()
    #except:
    #    print("Already disconencted: " + str(addr))
def connlisten():
    global s
    while True:
        s.listen()
        c, addr = s.accept()
        print(str(time.time()) + " DEBUG: Server has accepted a connection")
        _thread.start_new_thread(onclient,(c,addr))
_thread.start_new_thread(connlisten,())
while True:
    s.listen()
    c, addr = s.accept()
    print(str(time.time()) + " DEBUG: Server has accepted a connection")
    _thread.start_new_thread(onclient,(c,addr))
##    with conn:
##        dataw = []
##        print("Data request from: " + str(addr))
##        indata = conn.recv(1024).decode("utf-8")
##        dataw = indata.split(" ")
##        for i in range(len(dataw)):         #data handling
##            if i == 0:
##                for l in range(len(pnames)):
##                    if dataw[1] == "1":
##                        if dataw[0] == pnames[l]:
##                            included = True
##                            print("WHATATATATATATAAA")
##                            break
##                if dataw[1] == "1":
##                    if included == False:
##                        print(dataw[0] + " is not already in game, adding")
##                        pnames.append(dataw[0])
##                        px.append(5)
##                        py.append(5)
##                        lmove.append("right")
##                        phits.append(0)
##                        conn.∑
##send(servername.encode("utf-8"))
##
##                    
##            if i == 1:
##                if dataw[i] == "1": #if trying to connect
##                    if included == True:
##                        included = False
##                        conn.send("Error".encode("utf-8"))
##                        conn.close()
##                        break
##                if dataw[i] == "2": #if already connected
##                    #Detecting actions sent by the client
##                    if dataw[2] == "up":
##                        #loadrows()
##                        #conn.send(','.join(rows).encode("utf-8"))
##                        if py[pnames.index(dataw[0])] != 0:
##                            py[pnames.index(dataw[0])] -= 1
##                            #print(py[pnames.index(dataw[0])])
##                            #print(pnames.index(dataw[0]))
##                            #print(dataw[0])
##                            lmove[pnames.index(dataw[0])] = "up"
##                    elif dataw[2] == "down":
##                        #loadrows()
##                        #conn.send(','.join(rows).encode("utf-8"))
##                        if py[pnames.index(dataw[0])] != maxY - 1:
##                            py[pnames.index(dataw[0])] += 1
##                            lmove[pnames.index(dataw[0])] = "down"
##                    elif dataw[2] == "left":
##                        #loadrows()
##                        #conn.send(','.join(rows).encode("utf-8"))
##                        if px[pnames.index(dataw[0])] != 0:
##                            px[pnames.index(dataw[0])] -= 1
##                            lmove[pnames.index(dataw[0])] = "left"
##                    elif dataw[2] == "right":
##                        #loadrows()
##                        #conn.send(','.join(rows).encode("utf-8"))
##                        if px[pnames.index(dataw[0])] != maxX - 1:
##                            px[pnames.index(dataw[0])] += 1
##                            lmove[pnames.index(dataw[0])] = "right"
##                    elif dataw[2] == "shoot":    #Get the direction to move the laser
##                        
##                        if lmove[pnames.index(dataw[0])] == "up":
##                            lx.append(px[pnames.index(dataw[0])])
##                            ly.append(py[pnames.index(dataw[0])] - 1)
##                            ldir.append("up")
##                        elif lmove[pnames.index(dataw[0])] == "down":
##                            lx.append(px[pnames.index(dataw[0])])
##                            ly.append(py[pnames.index(dataw[0])] + 1)
##                            ldir.append("down")
##                        elif lmove[pnames.index(dataw[0])] == "left":
##                            lx.append(px[pnames.index(dataw[0])] - 1)
##                            ly.append(py[pnames.index(dataw[0])])
##                            ldir.append("left")
##                        elif lmove[pnames.index(dataw[0])] == "right":
##                            lx.append(px[pnames.index(dataw[0])] + 1)
##                            ly.append(py[pnames.index(dataw[0])])
##                            ldir.append("right")
##                        else:
##                            print("WTF HAPPEND")
##                    #elif dataw[2] == "none":
##                        #loadrows()
##                        #conn.send(','.join(rows).encode("utf-8"))
##                if dataw[i] == "3": #disconnect
##                    del px[pnames.index(dataw[0])]
##                    del py[pnames.index(dataw[0])]
##                    del lmove[pnames.index(dataw[0])]
##                    del pnames[pnames.index(dataw[0])]
##        #for garbagedump in range(len(ly)):
##        #    if ly[garbagedump] - 1 >= maxY or ly[garbagedump] + 1 <= 0 or lx[garbagedump] + 1 <= 0 or lx[garbagedump] - 1 >= maxX:
##        #        del ly[garbagedump]
##        #        del lx[garbagedump]
##        #        del ldir[garbagedump]
##        for x in range(len(ly)):
##            #move lasers
##            #print(x)
##            if ldir[x] == "up":
##                ly[x] -= 1
##            elif ldir[x] == "down":
##                ly[x] += 1
##            elif ldir[x] == "left":
##                lx[x] -= 1
##            elif ldir[x] == "right":
##                lx[x] += 1
##        for lascol in range(len(pnames)):
##            for las in range(len(ldir)):
##                if py[lascol] == ly[las] and px[lascol] == lx[las]:
##                    phits[lascol] += 1
##        
##        #loadrows()
##        #for f in range(len(rows)):
##        #    conn.send(rows[f].encode("utf-8"))
##        #conn.send(str(shots).encode("utf-8"))
##        loadrows()
##        try:
##            conn.send(','.join(rows).encode("utf-8") + ",".encode("utf-8") + str(phits[pnames.index(dataw[0])]).encode("utf-8"))
##        except:
##            print("Player disconnected: " + dataw[0])
##        try:
##            conn.close()
##        except:
##            print("Already disconencted: " + str(addr))
##

