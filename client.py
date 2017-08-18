import socket
import sys
import struct
from propertyHandler import set_property, get_property, get_command, set_command, get_receive, set_receive, props_list
from printer import *
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

def parseReceived(data, format):
    try:
        values = []
        item = 0
        olditem = 0
        for form in format:
            type = form["type"]
            size = get_property("sizeof"+type)
            string = ""
            while item < form["number"]*size + olditem:
                #print(item)
                raw = data[item:item+size]
                raw = b''.join(raw)

                if type == "double" or type == "float":
                    value = struct.unpack('d',raw)[0]
                elif type == "char":
                    value = raw.decode()
                    pass
                else:
                	value = int.from_bytes(raw, byteorder='little', signed=True)
                
                item += size
                if type != "char":
                    values.append(value)
                else:
                    string +=value
            if type == "char":
                values.append(string)
            olditem = item
        return values
    except:
        e = sys.exc_info()[0]
        print("error parsingInput:", e)
        return None

def end_conn():
    try:
        conn = get_socket()
        conn.close()
        set_socket(None)
        set_listen_thread(None)
    except:
        e = sys.exc_info()[0]
        print("error ending :", e)

def threaded_listen(conn):
    if get_property('print'):
        fclear()
    while True:
        id = conn.recv(1)
        if not id:
            break
        data = ""
        id = ord(id)
        recieve = get_receive(str(id))
        if recieve is None:
            length = 0
        else:
            length = int(recieve["len"])

        data = []
        while length > 0:
            try:
                data.append(conn.recv(1))
                length -= 1
            except:
                break
        if len(data) > 0:
            format = recieve.get("format",None)
            if format is not None:
                parsed = parseReceived(data, recieve["format"])
            else:
                parsed = data
            message = '\r' + recieve["name"] + "> " + str(parsed)
            if get_property('print'):
                fprint(message)
            print(message)
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
    message = message.to_bytes(1, 'big')
    get_socket().send(message)


def parse_instruction(line):
    instructions = line.split()
    for i in range(0, len(instructions)):
        instruct = instructions[i].lower()
        if instruct == "list":
            what = instructions[i+1]
            return props_list(what)
        if instruct == "set":
            prop = instructions[i + 1]
            val = instructions[i + 2]
            if prop == "command":
                name = val
                vals = instructions[i+3:]
                worked = set_command(name, vals)
            elif prop == "receive":
                id = val
                vals = instructions[i+3:]
                worked = set_receive(id, vals)
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
                ret = get_receive(command)
                if ret is not None:
                    print("receive for id " + command + " is " + str(ret))
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
        elif instruct == "exit" or instruct == "quit":
            end_conn()
            exit()
            return True


def Main():
    while True:
        line = input(" -> ")
        try:
            line = line.split('&')
            for command in line:
                worked = parse_instruction(command)
        except:
            e = sys.exc_info()[0]
            print("error:", e)
            worked = False
        if not worked:
            print("error occured")
            # create_connection(host, port)


if __name__ == '__main__':
    Main()
