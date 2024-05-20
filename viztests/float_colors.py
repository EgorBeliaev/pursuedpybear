"""Provide floats for color arguments. Shouldn't crash"""

import ppb

class MyScene(ppb.Scene):
    background_color = (200.5, 125.6, 127.8)

def setup(scene):
    scene.add(ppb.Sprite(image=ppb.Square(123.5, 200.8, 156.22)))

ppb.run(setup, starting_scene=MyScene)