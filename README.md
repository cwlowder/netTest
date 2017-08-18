# netTest
This python script allows for the sending and receiving of packets over tcp<br/>
This program can be run with `python3 client.py`

### commands
#### list
Used to list either `commands` or `receives`.<br/>
example: `list commands`
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

The #number represents the number of consecutive numbers that will be received of that type.
When omitted, it is implied only a single value exists. Multiple of these types can be strung together.
An example of this: `[uint8#2][double][uint32#4]`. This statement implies that 2 uint8s, then a double, then 4 uint32s will be received.
