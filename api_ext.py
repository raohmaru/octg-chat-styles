# This python script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this script. If not, see <http://www.gnu.org/licenses/>.

#---------------------------------------------------------------------------
# Extended API that invokes methods from OCTGN C# API
#---------------------------------------------------------------------------

import re

try:
   # IronPython bindings
   import clr
   clr.AddReference("Octgn")
   clr.AddReference("Octgn.Core")
   clr.AddReference("Octgn.JodsEngine")
   import Octgn
   import System
except (IOError, ImportError):
   whisper("There was an error while starting the game and some functionalities won't be available.\nPlease restart OCTGN.")


class ChatColors(object):
   Black = "#000000"

   @staticmethod
   def hexToRGB(hex):
      """
      Transform a color hex value (like "#FFCC000") into its RGB components as a list.
      """
      hex = hex.lstrip("#")
      return list(int(hex[i:i+2], 16) for i in (0, 2, 4))


class ChatPlayer(Octgn.Core.Play.IPlayPlayer):
   """
   Dummy player object, to format text messages in the chat box.
   """
   id = 1000  # Assign an ID high enough so it does not mess with the actual players
   
   def __init__(self, color = ChatColors.Black):
      # `color` is a System.Windows.Media.Color C# object, which is not available as a Python object
      self.color = Octgn.Core.Play.BuiltInPlayer.Notify.Color.FromRgb(*ChatColors.hexToRGB(color))
      self.name = u"\u200B"  # Zero-width space character
      ChatPlayer.id += 1
      self.id = ChatPlayer.id
      
   # Getters that IronPython calls when getting a property ("get_" + property name)
   def get_Color(self):
      return self.color
      
   def get_Name(self):
      return self.name
      
   def get_Id(self):
      return self.id
      
   def get_State(self):
      return Octgn.Core.Play.PlayerState.Connected
      
   def ToString(self):
      return self.name
   
   
class ExtendedApi(object):
   """
   An extended API with methods that directly call IronPython C# methods.
   """
   
   RgxReplaceIds = re.compile(r"\{#(\d+)\}")

   def __replaceIDsWithNames(self, string):
      """
      Replaces a card ID in the given string (e.g. {#66526}) with the card name.
      """
      return re.sub(ExtendedApi.RgxReplaceIds, lambda match: Card(int(match.group(1))).Name, string)


   def __addMessage(self, message):
      """
      Uses internal C# method to publish messages with formatted text.
      """
      try:
         Octgn.Program.GameMess.AddMessage(message)
      except AttributeError:
         whisper(message.Message)
      
      
   def warning(self, str):
      """
      Displays a message formatted like an error message.
      """
      self.__addMessage(Octgn.Core.Play.WarningMessage(self.__replaceIDsWithNames(str), {}))
      
            
   def system(self, str):
      """
      Displays a message formatted like a system message.
      """
      self.__addMessage(Octgn.Core.Play.SystemMessage(self.__replaceIDsWithNames(str), {}))
      
      
   def whisper(self, str, color = ChatColors.Black, bold = False):
      """
      Sends a message with basic formatting to the local player.
      """
      msg = self.__replaceIDsWithNames(str)
      dummyPlayer = ChatPlayer(color)
      if bold:
         dummyPlayer.name = msg
         msg = ""
      update()  # If invoked from a remote call, it makes next function work
      self.__addMessage(Octgn.Core.Play.PlayerEventMessage(dummyPlayer, msg, {}))
      del dummyPlayer
      
      
   def notify(self, str, color = ChatColors.Black, bold = False):
      """
      Sends a message with basic formatting to all players.
      """
      self.whisper(str, color, bold)
      if len(players) > 1:
         remoteCall(players[1], "_extapi_whisper", [str, color, bold])


# Make it global
_extapi = ExtendedApi()
# Alias to use _extapi.whisper from remoteCall()
_extapi_whisper = _extapi.whisper
