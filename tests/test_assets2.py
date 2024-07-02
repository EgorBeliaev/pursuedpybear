import pytest
from unittest.mock import patch, MagicMock
import sdl2.ext
from ppb.assets import _create_surface, BLACK, MAGENTA

from sdl2 import (
    SDL_Point,  # https://wiki.libsdl.org/SDL_Point
    SDL_CreateRGBSurface,  # https://wiki.libsdl.org/SDL_CreateRGBSurface
    SDL_FreeSurface,  # https://wiki.libsdl.org/SDL_FreeSurface
    SDL_SetColorKey,  # https://wiki.libsdl.org/SDL_SetColorKey
    SDL_CreateSoftwareRenderer,  # https://wiki.libsdl.org/SDL_CreateSoftwareRenderer
    SDL_DestroyRenderer,  # https://wiki.libsdl.org/SDL_DestroyRenderer
    SDL_SetRenderDrawColor,  # https://wiki.libsdl.org/SDL_SetRenderDrawColor
    SDL_RenderFillRect,  # https://wiki.libsdl.org/SDL_RenderFillRect
    SDL_GetRendererOutputSize,  # https://wiki.libsdl.org/SDL_GetRendererOutputSize
)

@pytest.fixture
def mock_sdl_call():
    with patch('ppb.assets.sdl_call') as mock:
        yield mock

@pytest.fixture
def mock_prepare_color():
    with patch('ppb.assets.sdl2.ext.prepare_color') as mock:
        yield mock

@pytest.fixture
def mock_fill():
    with patch('ppb.assets.sdl2.ext.fill') as mock:
        yield mock

def test_create_surface_with_black_color(mock_sdl_call, mock_prepare_color, mock_fill):
    mock_surface = MagicMock()
    mock_sdl_call.return_value = mock_surface

    surface = _create_surface(BLACK)

    assert mock_sdl_call.call_count == 2
    assert mock_prepare_color.call_count == 1
    assert mock_fill.call_count == 1

    assert surface == mock_surface
    color_key = MAGENTA
    color = sdl2.ext.Color(*color_key)
    mock_prepare_color.assert_called_once_with(color, mock_surface.contents)

def test_create_surface_with_non_black_color(mock_sdl_call, mock_prepare_color, mock_fill):
    mock_surface = MagicMock()
    mock_sdl_call.return_value = mock_surface
    non_black_color = (255, 0, 0)

    surface = _create_surface(non_black_color)

    assert mock_sdl_call.call_count == 2
    assert mock_prepare_color.call_count == 1
    assert mock_fill.call_count == 1

    assert surface == mock_surface
    color_key = BLACK
    color = sdl2.ext.Color(*color_key)
    mock_prepare_color.assert_called_once_with(color, mock_surface.contents)

def test_sdl_call_error_handling(mock_sdl_call, mock_prepare_color, mock_fill):
    mock_surface = MagicMock()
    mock_surface.contents = MagicMock()  # Ensure mock surface has 'contents' attribute

    def sdl_call_side_effect(func, *args, **kwargs):
        if func == SDL_CreateRGBSurface:
            return mock_surface
        elif func == SDL_SetColorKey:
            return -1  # Simulate error
        return 0

    mock_sdl_call.side_effect = sdl_call_side_effect

    # Modify _check_error to raise RuntimeError if error condition is met
    def raise_runtime_error_on_failure(func, *args, _check_error, **kwargs):
        result = sdl_call_side_effect(func, *args, **kwargs)
        if _check_error(result):
            raise RuntimeError("SDL call failed")
        return result

    mock_sdl_call.side_effect = raise_runtime_error_on_failure

    with pytest.raises(RuntimeError, match="SDL call failed"):
        _create_surface(BLACK)

    assert mock_sdl_call.call_count == 2
    assert mock_prepare_color.call_count == 1
    assert mock_fill.call_count == 0

@pytest.mark.parametrize("color, expected_color_key", [
    (BLACK, MAGENTA),
    ((255, 0, 0), BLACK),
])
def test_color_conversion(color, expected_color_key, mock_sdl_call, mock_prepare_color, mock_fill):
    mock_surface = MagicMock()
    mock_surface.contents = MagicMock()  # Ensure mock surface has 'contents' attribute
    mock_sdl_call.side_effect = lambda func, *args, **kwargs: mock_surface if func == SDL_CreateRGBSurface else 0

    _create_surface(color)

    color_obj = sdl2.ext.Color(*expected_color_key)
    mock_prepare_color.assert_called_once_with(color_obj, mock_surface.contents)

    assert mock_sdl_call.call_count == 2
    mock_fill.assert_called_once_with(mock_surface.contents, color_obj)
