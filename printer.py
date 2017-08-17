from propertyHandler import get_property

def fclear():
    file = get_property('outfile')
    file = open(file, 'w')
    print('', end="", file=file)

def fprint(statement):
    file = get_property('outfile')
    file = open(file, 'a')
    print(statement+'\n', end="", file = file)