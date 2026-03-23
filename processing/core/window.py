import os


def resolve_icon_path(base_dir, path):
    if os.path.isabs(path):
        return path

    if os.path.exists(path):
        return path

    pkg_path = os.path.join(base_dir, path)
    if os.path.exists(pkg_path):
        return pkg_path

    return path


def apply_window_icon(state, pygame, base_dir):
    resolved = resolve_icon_path(base_dir, state["_window_icon"])
    try:
        icon_surface = pygame.image.load(resolved)
        pygame.display.set_icon(icon_surface)
    except Exception:
        # Keep startup robust if icon path is invalid or image can't be loaded.
        pass


def init_window(state, pygame, set_public_global, apply_window_icon_func):
    pygame.init()
    print("... and hello from processing-python")
    pygame.font.init()
    info = pygame.display.Info()
    set_public_global("display_width", int(info.current_w))
    set_public_global("display_height", int(info.current_h))

    flags = 0
    if state["_fullscreen_enabled"]:
        state["_width"], state["_height"] = int(info.current_w), int(info.current_h)
        flags = pygame.FULLSCREEN

    state["_screen"] = pygame.display.set_mode((state["_width"], state["_height"]), flags)
    state["_millis_start"] = pygame.time.get_ticks()
    apply_window_icon_func()
    pygame.display.set_caption(state["_title"])
    state["_clock"] = pygame.time.Clock()

    # Set default background to light gray (Processing default)
    state["_screen"].fill((200, 200, 200))

    set_public_global("width", state["_width"])
    set_public_global("height", state["_height"])
    set_public_global("pixel_width", state["_width"])
    set_public_global("pixel_height", state["_height"])
    set_public_global("focused", True)
