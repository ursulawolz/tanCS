#!/usr/bin/python
#-------------------------------------------------------------------------------
# Clutter_HelloWorld.py
#
# A basic reference example to demonstrate how to use Clutter with Python's 
# GObject-Introspection capabilities.
#
# by: Dinh Bowman
#-------------------------------------------------------------------------------

from gi.repository import Clutter
import sys

# An easy way to debug clutter and cogl without having to type the
# command line arguments
#DEBUG = True
DEBUG = False
debugArgs = ['--clutter-debug=all', '--cogl-debug=all']


# Define some standard colors to make basic color assigments easier
colorWhite = Clutter.Color.new(255,255,255,255)
colorMuddyBlue = Clutter.Color.new(49,78,108,255)
colorBlack = Clutter.Color.new(0,0,0,255)


class GUI:
    def __init__(self):
        """
        Build the user interface.
        """
        self.mainStage = Clutter.Stage.get_default()
        self.mainStage.set_color(colorBlack)
        self.mainStage.set_title("Python Clutter")
        self.mainStage.set_size(400, 150)
        self.mainStage.set_reactive(True)

        # Create a main layout manager
        self.mainLayoutManager = Clutter.BoxLayout()
        self.mainLayoutManager.set_vertical(True)
        self.mainLayoutManager.set_homogeneous(False)
        self.mainLayoutManager.set_pack_start(False)
        
        # Create the main window
        # mainStage 
        #  mainWindow :: mainLayoutManager
        self.mainWindow = Clutter.Box.new(self.mainLayoutManager)
        self.mainWindow.set_color(colorBlack)
        self.mainStage.add_actor(self.mainWindow)

        # Make the main window fill the entire stage
        mainGeometry = self.mainStage.get_geometry()
        self.mainWindow.set_geometry(mainGeometry)

        # Create some text
        self.renderText()

        # Create a rectangle
        self.renderRect()
        self.clutterRectangle.set_reactive(True)
        self.clutterRectangle.connect('button-press-event',self.success)

        # Setup some key bindings on the main stage
        self.mainStage.connect_after("key-press-event", self.onKeyPress)

        # Present the main stage (and make sure everything is shown)
        self.mainStage.show_all()

    def success(self,widget,data):
        print 'hooray'

    def renderText(self):
        """
        Create a ClutterText with the phrase Hello World
        """
        txtFont = "Mono 10"
        self.clutterText = Clutter.Text.new_full(txtFont, "Hello World", colorWhite)
        Clutter.Container.add_actor(self.mainWindow, self.clutterText)
        self.clutterText.set_position(5,5)
        self.clutterText.show()


    def renderRect(self):
        """
        Create a basic colored rectangle
        """
        self.clutterRectangle = Clutter.Rectangle.new_with_color(colorMuddyBlue)
        self.clutterRectangle.set_size(200,50)
        Clutter.Container.add_actor(self.mainWindow, self.clutterRectangle)
        self.clutterRectangle.show()

        
    def destroy(self):
        Clutter.main_quit()


    def onKeyPress(self, actor=None, event=None, data=None):
        """
        Basic key binding handler
        """
        try:
            pressed = chr(event.key.keyval)

            # Evaluate the key modifiers
            state = event.get_state()
            if (state & state.SHIFT_MASK == state.SHIFT_MASK):
                modShift = True
            else:
                modShift = False

            if (state & state.CONTROL_MASK == state.CONTROL_MASK):
                modControl = True
            else:
                modControl = False

            if (state & state.META_MASK == state.META_MASK):
                modMeta = True
            else:
                modMeta = False

            if (pressed == 'q'):
                print "Quitting"
                self.destroy()
            elif (pressed == 'j'):
                print "Down"
            elif (pressed == 'k'):
                print "Up"
            elif (pressed == 'i'):
                print "Interrupt - Debug"
                try:
                    import ipdb as pdb
                except:
                    import pdb
                pdb.set_trace()
        except:
            pass


################################################################################
# Main
################################################################################
def main():
    if DEBUG:
        Clutter.init(debugArgs)
    else:
        Clutter.init(sys.argv)
    app = GUI()
    Clutter.main()
    
if __name__ == "__main__":
    sys.exit(main())