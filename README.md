# netTest
This python script allows for the sending and receiving of packets over tcp<br/>
This program can be run with `python3 client.py`

### Commands
#### list
Used to list either `commands` or `receives`.<br/>
example: `list commands`
#### connect
Used to connect to what ever host & port is set to
example: `connect`<br/>
#### listen
This command starts listening to the data being received. Requires an active connection.<br/>
example: `listen`<br/>
#### send
Sends whatever command is given as an argument. Requires an active connection.<br/>
example: `send test_command`<br/>
#### get
Used to get the properties and the format of the commands and receives<br/>
example: `get host`<br/>
example: `get receive 4`
#### set
Used to set the properties and the format of the commands and receives<br/>
example: `set port 25565`<br/>
example: `set command test 10`<br/>
###### Note:
setting receives is more complicated it involves three arguments
* `-l` the length of the the receive
* `-n` the name of the receive
* `-f` the format of the incoming receive<br/>

Together they can look like this:<br/>
`set receive -l 4 -n test_command -f [uint16]`
### Format of Receive
Formats are constructed using the following syntax:<br/>
`[type#number]`<br/>
type can be one of the following:
* uint8
* uint16
* uint32
* float
* double
* long

The `#number` represents the number of consecutive numbers that will be received of that type.
When omitted, it is implied only a single value exists. Multiple of these types can be strung together.
An example of this: `[uint8#2][double][uint32#4]`. This statement implies that 2 uint8s, then a double, then 4 uint32s will be received.

### Properties
This is a list of the properties that can be set, what they affect, and what type(int, float, etc) can they be set to.
* host
    * The host to be connected to
    * Can be set to a string
* port
    * The port to be connected to
    * Can be set to an int
* print
    * Should the data received when listening be printed?
    * Can be set to a boolean
* outfile
    * The file that will be printed to and overwritten
    * Can be set to a string

The rest of the properties should not be edited:
* sizeofuint8
    * Number of bytes in an uint8
    * Can be set to an int
* sizeofuint16
    * Number of bytes in an uint16
    * Can be set to an int
* sizeofuint32
    * Number of bytes in an uint32
    * Can be set to an int
* sizeoffloat
    * Number of bytes in a float
    * Can be set to an int
* sizeofdouble
    * Number of bytes in a double
    * Can be set to an int
* sizeoflong
    * Number of bytes in a long
    * Can be set to an int