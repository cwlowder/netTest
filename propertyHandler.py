import json

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
        return None

def get_recieve_len(id):
    try:
        length = get_properties()["receive_len"][id]
        return length
    except:
        return -1

def set_recieve_len(id, length):
    try:
        props = get_properties()
        props["receive_len"][id] = int(length)
        set_properties(props)
        return True
    except:
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
        return False

    set_properties(properties)
    return True





def get_properties():
    try:
        with open('props.json') as data_file:
            props = json.load(data_file)
        return props
    except:
        return None

def set_properties(new_props):
    try:
        with open('props.json', 'w') as outfile:
            json.dump(new_props, outfile)
        return True
    except:
        return False