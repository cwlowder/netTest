import json
import sys
import pprint

def get_type(val):
    try:
        int(val)
        return "int"
    except:
        pass
    try:
        float(val)
        return "float"
    except:
        pass
    try:
        if val == "true" or val == "false" or val == "t" or val == "f":
            return "boolean"
    except:
        pass
    return "string"

valid_props = {"host":"string",
               "port":"int",
                "print":"boolean",
                "outfile":"string"
                }

def get_property(prop):
    try:
        if prop in valid_props.keys():
            val = get_properties()[prop]
            type = valid_props[prop]
            if type == "boolean":
                if val == "true" or val == "t":
                    val = True
                else:
                    val = False
            elif type == "int":
                val = int(val)
            elif type == "float":
                val = float(val)
            return val
        elif prop == "help":
            return get_properties()["help"]
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return None


def get_command(command):
    try:
        command = get_properties()["commands"][command]

        val = command

        type = get_type(command)
        if type == "boolean":
            if val == "true" or val == "t":
                val = True
            else:
                val = False
        elif type == "int":
            val = int(val)
        elif type == "float":
            val = float(val)

        return val
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return None

def props_list(what):
    try:
        prop = get_properties()
        if what == "commands":
            print(prop["commands"])
            return True
        elif what == "receives":
            print(prop["receives"])
            return True
        return False
    except:
        return False
def get_receive(id):
    try:
        prop = get_properties()["receives"][id]
        return prop
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return None


def parseFormat(format):
    import re
    fields = re.findall('\[([^[\]]*)\]', format)
    template = []
    for field in fields:
        field = field.split("#")
        type = field[0]
        if len(field) > 1:
            number = int(field[1])
        else:
            number = 1
        template.append({"type":type,"number":1})
    return template

def set_receive(id, values):
    try:
        props = get_properties()
        if id not in props["receives"]:
            props["receives"][id] = {}

        for i in range(0,len(values)):
            if values[i] == "-l" or values[i] == "-length":
                props["receives"][id]["len"] = values[i+1]
                i+=1
            elif values[i] == "-n" or values[i] == "-name":
                props["receives"][id]["name"] = values[i+1]
                i+=1
            elif values[i] == "-f" or values[i] == "-format":
                format = values[i+1]
                props["receives"][id]["format"] = parseFormat(format)
                i+=1

        set_properties(props)
        return True
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return False


def set_command(command, values):
    try:
        final_value = ""
        for value in values:
            final_value = final_value + value + " "

        properties = get_properties()

        properties["commands"][command] = final_value

        set_properties(properties)
        return True
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return False


def set_property(prop, val):
    properties = get_properties()

    try:
        if prop in valid_props.keys() and valid_props[prop] is get_type(val):
                if get_type(val) == bool:
                    if val == "true" or val == "t":
                        val = True
                    else:
                        val = False
                properties[prop] = val
        else:
            return False
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return False

    set_properties(properties)
    return True


def get_properties():
    try:
        with open('props.json') as data_file:
            props = json.load(data_file)
        return props
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return None

def set_properties(new_props):
    try:
        with open('props.json', 'w') as outfile:
            json.dump(new_props, outfile)
        return True
    except:
        e = sys.exc_info()[0]
        print("error:", e)
        return False