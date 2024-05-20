import ppb
from ppb import Vector
from ppb.features.default_sprites import (
    TargetSprite,
    wasd_direction_key_bindings,
    KeyBoardMovementSprite,
    MouseTargetSprite
)
import ppb.events as events


def test_target_sprite_linear():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(3, 4)
    target_sprite.speed = 5.0
    target_sprite.on_update(ppb.events.Update(0.2), lambda x: None)

    assert target_sprite.position.isclose((0.6, 0.8))


def test_target_sprite_exponential():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(3, -4)
    target_sprite.speed = 0.0
    target_sprite.exponential_speed = 0.5
    target_sprite.on_update(ppb.events.Update(2.0), lambda x: None)

    assert target_sprite.position.isclose((2.25, -3.0))


def test_target_sprite_max_speed():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(-3, 4)
    target_sprite.speed = 500.0
    target_sprite.exponential_speed = 0.99
    target_sprite.max_speed = 1.0
    target_sprite.on_update(ppb.events.Update(2.0), lambda x: None)

    assert target_sprite.position.isclose((-1.2, 1.6))


def test_target_sprite_min_speed():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(-3, -4)
    target_sprite.speed = 0.0
    target_sprite.min_speed = 2.0
    target_sprite.on_update(ppb.events.Update(1.0), lambda x: None)

    assert target_sprite.position.isclose((-1.2, -1.6))


def test_keyboard_movement_sprite_move_left():

    keyboard_sprite = KeyBoardMovementSprite()

    keyboard_sprite.on_key_pressed(
        ppb.events.KeyPressed(key=ppb.keycodes.Left, mods={}),
        lambda x: None,
    )
    keyboard_sprite.on_update(ppb.events.Update(1), lambda x: None)

    assert keyboard_sprite.direction.isclose((-1, 0))
    assert keyboard_sprite.position.isclose((-1, 0))


def test_keyboard_movement_sprite_move_right():

    keyboard_sprite = KeyBoardMovementSprite()

    keyboard_sprite.on_key_pressed(
        ppb.events.KeyPressed(key=ppb.keycodes.Right, mods={}),
        lambda x: None,
    )
    keyboard_sprite.on_update(ppb.events.Update(1), lambda x: None)

    assert keyboard_sprite.direction.isclose((1, 0))
    assert keyboard_sprite.position.isclose((1, 0))


def test_keyboard_movement_sprite_move_up():

    keyboard_sprite = KeyBoardMovementSprite()

    keyboard_sprite.on_key_pressed(
        ppb.events.KeyPressed(key=ppb.keycodes.Up, mods={}),
        lambda x: None,
    )
    keyboard_sprite.on_update(ppb.events.Update(1), lambda x: None)

    assert keyboard_sprite.direction.isclose((0, 1))
    assert keyboard_sprite.position.isclose((0, 1))


def test_keyboard_movement_sprite_move_down():

    keyboard_sprite = KeyBoardMovementSprite()

    keyboard_sprite.on_key_pressed(
        ppb.events.KeyPressed(key=ppb.keycodes.Down, mods={}),
        lambda x: None,
    )
    keyboard_sprite.on_update(ppb.events.Update(1), lambda x: None)

    assert keyboard_sprite.direction.isclose((0, -1))
    assert keyboard_sprite.position.isclose((0, -1))


def test_keyboard_movement_sprite_move_down_wasd():

    keyboard_sprite = KeyBoardMovementSprite(key_bindings=wasd_direction_key_bindings)

    keyboard_sprite.on_key_pressed(
        ppb.events.KeyPressed(key=ppb.keycodes.S, mods={}),
        lambda x: None,
    )
    keyboard_sprite.on_update(ppb.events.Update(1), lambda x: None)

    assert keyboard_sprite.direction.isclose((0, -1))
    assert keyboard_sprite.position.isclose((0, -1))


def test_keyboard_movement_sprite_move_down_left_wasd():

    keyboard_sprite = KeyBoardMovementSprite(key_bindings=wasd_direction_key_bindings)

    keyboard_sprite.on_key_pressed(
        ppb.events.KeyPressed(key=ppb.keycodes.S, mods={}),
        lambda x: None,
    )

    keyboard_sprite.on_key_pressed(
        ppb.events.KeyPressed(key=ppb.keycodes.A, mods={}),
        lambda x: None,
    )
    keyboard_sprite.on_update(ppb.events.Update(1), lambda x: None)

    assert keyboard_sprite.direction.isclose((-1, -1))
    assert keyboard_sprite.position.isclose((-1/2**.5, -1/2**.5))


def test_mouse_target_sprite():
    sprite = MouseTargetSprite()

    mouse_position = Vector(123,456)
    sprite.on_mouse_motion(events.MouseMotion(mouse_position,Vector(0,0),buttons=[]), lambda x:None)
    assert sprite.target == mouse_position


