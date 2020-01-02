import json
import os
import core

@core.render.Window.focus
def execute(element, window):
    try:

        if element.data == 0:       #Custom Python Commands
            core.render.close()
            quit()

        os.system(element.data)
        yield core.std.Info("Executed")
    except:
        yield core.std.Error("Unknown Error")

class CommandCenter(core.std.Menu):

    self.data = []

    def __init__(self):
        with open(f"{core.sys.PATH}programs/command_center/commands.json", "r") as file:
            self.data[0] = json.load(file)

        for key, value in self.data.items():
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), key, justify="L"),
                data = value,
                select = execute))
        super().__init__(*elements, title="Imported Commands")

    @core.render.Window.focus
    def show(self):
        super().show()
        core.hardware.Backlight.fill(225, 0, 0)

main = CommandCenter()