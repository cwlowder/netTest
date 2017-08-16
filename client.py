import socket
import sys
from propertyHandler import set_property, get_property, get_command, set_command, get_recieve_len, set_recieve_len

from _thread import *

mySocket = None

def get_socket():
    return mySocket
def set_socket(mine):
    global mySocket
    mySocket = mine

listen_thread = None

def get_listen_thread():
    return listen_thread
def set_listen_thread(mine):
    global listen_thread
    listen_thread = mine

def threaded_listen(conn):
    while True:
        len = conn.recv(1)
        if not len:
            break
        data = ""
        print(len)
        #len = int(len,16)
        while len > 0:
            data = data + conn.recv(1).decode()
            len -= 1
        print('\r' + data)
    conn.close()
    set_socket(None)
    set_listen_thread(None)

def start_listening():
    try:
        if get_listen_thread() is None:
            listen_thread = start_new_thread(threaded_listen, (get_socket(),))
            set_listen_thread(listen_thread)
            return listen_thread
        else:
            return None
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return None

def create_connection(host, port):
    try:
        mySocket = socket.socket()
        mySocket.connect((host, port))
        set_socket(mySocket)
        return True
    except:
        e = sys.exc_info()[0]
        print("error:",e)
        return False

def send_command(command):
    message = get_command(command)
    get_socket().send(message.encode())


def parse_instruction(line):
    instructions = line.split()
    for i in range(0, len(instructions)):
        instruct = instructions[i].lower()
        if instruct == "set":
            prop = instructions[i + 1]
            val = instructions[i + 2]
            if prop == "command":
                name = val
                vals = instructions[i+3:]
                worked = set_command(name, vals)
            elif prop == "receive":
                name = val
                vals = instructions[i+3]
                worked = set_recieve_len(name, vals)
            else:
                worked = set_property(prop, val)
            return worked
        elif instruct == "get":
            prop = instructions[i + 1]
            if prop == "command":
                command = instructions[i + 2]
                ret = get_command(command)
                if ret is not None:
                    print(command + ":" + str(ret))
                    return True
                else:
                    return False
            if prop == "receive":
                command = instructions[i + 2]
                ret = get_recieve_len(command)
                if ret > -1:
                    print("receive length of " + command + " is " + str(ret) + " bytes")
                    return True
                else:
                    return False
            else:
                val = get_property(prop)
                if val is not None:
                    print(prop + ':' + str(val))
                    return True
                else:
                    print(prop + ' is undefined')
                    return False
        elif instruct == "connect":
            host = get_property("host")
            port = get_property("port")
            worked = create_connection(host, port)
            if worked:
                print("connected to " + host + ":" + str(port))
            return worked
        elif instruct == "listen":
            start_listening()
            return get_listen_thread() is not None
        elif instruct == "send":
            if get_socket() is None:
                return False
            else:
                command = instructions[i + 1]
                send_command(command)
                return True



def Main():
    while True:
        line = input(" -> ")
        try:
            worked = parse_instruction(line)
        except:
            e = sys.exc_info()[0]
            print("error:", e)
            worked = False
        if not worked:
            print("error occured")
            # create_connection(host, port)


if __name__ == '__main__':
    Main()