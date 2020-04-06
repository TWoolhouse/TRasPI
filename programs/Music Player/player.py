import core
import colorsys
from animatedtext import AnimatedText
from volume import Volume
import pygame
import time


def constrain(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


class LocalPlayer(core.render.Window):

    core.asset.Image(
        "play", path=f"{core.sys.PATH}programs/Music Player/asset/play.icon")
    core.asset.Image(
        "pause", path=f"{core.sys.PATH}programs/Music Player/asset/pause.icon")
    core.asset.Image(
        "next", path=f"{core.sys.PATH}programs/Music Player/asset/next.icon")
    core.asset.Image(
        "rest", path=f"{core.sys.PATH}programs/Music Player/asset/prev.icon")

    def __init__(self, playlist):
        pygame.mixer.init()
        self.playlist = playlist
        self.track_number = 0
        self.state = 0
        self.pausestart = 0
        self.timeout = 0
        self.timeout_sync = 0
        # PLAYER OBJECTS
        self.trackinfo = AnimatedText((64, 35), "Loading", width=20)
        self.trackinfo.edit(self.playlist[self.track_number].description)
        self.volume = Volume()
        # PLAYER ELEMENTS
        self.centre = [core.asset.Image("pause"), core.asset.Image("play")]
        self.elements = [core.element.Image(core.Vector(44, 53),
                                            core.asset.Image("rest")),
                         core.element.Image(core.Vector(84, 53),
                                            core.asset.Image("next"))]
        # PLAYER START
        self.play()

    def render(self):
        if time.time() - self.timeout_sync > 1 and self.timeout <= 60:
            if self.timeout == 60:
                self.inactive()
            else:
                self.timeout +=1
                self.timeout_sync = time.time()
        if self.state == 2:
            if self.endpoint < time.time():
                res = self.skip()
                if not res:
                    self.back()
            core.element.Line(core.Vector(0, 40), core.Vector(constrain(
                self.playlist[self.track_number].length - (self.endpoint - time.time()), 0, self.playlist[self.track_number].length, 0, 128), 40), width=2).render()
        core.element.Text(core.Vector(115, 53), self.volume.get()).render()
        core.element.Image(core.Vector(64, 53),
                           self.centre[0 if self.state == 2 else 1]).render()
        core.element.Text(core.Vector(
            1, 53), f"{self.track_number+1}\{len(self.playlist)}", justify="L").render()
        core.element.Text(core.Vector(64, 5),
                          f"{self.playlist[self.track_number].name}"[:20]).render()
        self.trackinfo.update()
        for element in self.elements:
            element.render()

    @core.render.Window.focus
    def play(self):
        if self.state == 0:
            try:
                self.playlist[self.track_number].play()
                self.endpoint = self.playlist[self.track_number].length + time.time()
            except FileNotFoundError:
                yield core.std.Error("File not found")
                return
        elif self.state == 1:
            self.endpoint += (time.time() - self.pausestart)
            self.pausestart = 0
            pygame.mixer.music.unpause()
        self.state = 2

    def pause(self):
        self.pausestart = time.time()
        pygame.mixer.music.pause()
        self.state = 1

    def stop(self):
        pygame.mixer.music.stop()
        self.state = 0
        self.track_pos = 0

    def toggle(self):
        if self.state == 2:
            self.pause()
        elif self.track_number < len(self.playlist):
            self.play()

    @core.render.Window.focus
    def skip(self):
        if self.track_number + 1 < len(self.playlist):
            self.stop()
            self.track_number += 1
            self.play()
            self.trackinfo.edit(self.playlist[self.track_number].description)
            return True
        else:
            window = core.std.Info("End of Queue")
            yield window
            return False

    def back(self):
        self.finish()

    def active(self):
        R, G, B = colorsys.hsv_to_rgb(core.sys.Config(
            "std::system")["system_colour"]["value"] / 100, 1, 1)
        core.hardware.Backlight.fill(int(R * 255), int(G * 255), int(B * 255))
        self.timeout = 0

    def inactive(self):
        R, G, B = colorsys.hsv_to_rgb(core.sys.Config(
            "std::system")["system_colour"]["value"] / 100, 1, 0.3)
        core.hardware.Backlight.fill(int(R * 255), int(G * 255), int(B * 255))


class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = LocalPlayer

    def press(self):
        pygame.mixer.music.stop()
        self.window.finish()
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = LocalPlayer

    def press(self):
        self.window.toggle()
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = LocalPlayer

    def press(self):
        self.window.skip()
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = LocalPlayer

    def press(self):
        self.window.stop()
        self.window.track_pos = 0
        self.window.play()
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = LocalPlayer

    def press(self):
        self.window.volume.increse()
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = LocalPlayer

    def press(self):
        self.window.volume.decrese()
        self.window.active()
