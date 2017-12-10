import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def recieving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                data = data.decode('utf-8')
                print(str(data))
        except:
                pass
        finally:
                tLock.release()

host = socket.gethostname()
port = 0

server = ('10.50.18.254', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=recieving, args=("RecvThread", s))
rT.start()

alias = input("Name: ")
message = input(alias + "-> ")

while message != 'q':
    if message != '':
        message = alias + ": " + message
        s.sendto(message.encode('utf-8'), server)
    tLock.acquire()
    message = input(alias + "-> ")
    tLock.release()
    time.sleep(0.2)

shutdown = True
rT.join()
s.close()

