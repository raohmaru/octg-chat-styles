# OCTGN Scripting Tools

Set of Python utilities to help in game plugin development.

## Installation

1. Download the file https://raw.githubusercontent.com/raohmaru/octgn-scripting-tools/master/api_ext.py.
1. Move the downloaded file to the scripts folder of your game plugin.
1. Add the path to this script to the `<script>` section of the [game definition XML](https://github.com/octgn/OCTGN/wiki/definition.xml#scripts) file of your game plugin.

## Chat Messages with Style

Bring color to [OCTGN](https://octgn.net/) chat messages sent via scripting.


It can be used in [game plugins](https://github.com/octgn/OCTGN/wiki#create-games-on-octgn) to display colorful messages in the player's chat box.
```
_extapi.whisper("Hello World!", "#FFCC00", True)
```
![Screenshot of OCTGN chat box with colorful messages.](/msgbox-with-colors.png)

### Usage

A new Python variable `_extapi` will be available in your game, which contains the following methods:

+ `_extapi.whisper(str, color = "#000000", bold = False)`  
  Sends a message with basic formatting to the local player.

+ `_extapi.notify(str, color = "#000000", bold = False)`  
  Sends a message with basic formatting to all players.

+ `_extapi.warning(str)`  
  Displays a message formatted like an error message.

+ `_extapi.system(str)`  
  Displays a message formatted like a system message.
  
  
### Examples
Send a message to the local user, text in black (default).
```
_extapi.whisper("You have been hit.")
```

Send a message to the local user, text in red.
```
_extapi.whisper("You have been hit.", "#FF0000")
```

Send a message to the local user, text in red and bold.
```
_extapi.whisper("Tap a soldier.", "#FF0000", True)
```

Send a message to all users, text in blue and bold.
```
_extapi.whisper("All your base are belong to us.", "#0000FF", True)
```
  
## License

Released under the GNU General Public License version 3.