def size(state, pygame, set_public_global, w, h):
    state["_width"], state["_height"] = int(w), int(h)
    set_public_global("width", state["_width"])
    set_public_global("height", state["_height"])
    set_public_global("pixel_width", state["_width"])
    set_public_global("pixel_height", state["_height"])

    if state["_screen"] is not None:
        state["_screen"] = pygame.display.set_mode((state["_width"], state["_height"]))
        state["_screen"].fill((200, 200, 200))


def full_screen(state, pygame, set_public_global):
    state["_fullscreen_enabled"] = True

    if state["_screen"] is not None:
        info = pygame.display.Info()
        state["_width"], state["_height"] = int(info.current_w), int(info.current_h)
        state["_screen"] = pygame.display.set_mode((state["_width"], state["_height"]), pygame.FULLSCREEN)
        set_public_global("width", state["_width"])
        set_public_global("height", state["_height"])
        set_public_global("pixel_width", state["_width"])
        set_public_global("pixel_height", state["_height"])


def frame_rate(state, fps):
    state["_fps"] = int(fps)


def title(state, pygame, t):
    state["_title"] = str(t)
    if state["_screen"] is not None:
        pygame.display.set_caption(state["_title"])


def window_icon(state, apply_window_icon, path="icon.png"):
    state["_window_icon"] = str(path)
    if state["_screen"] is not None:
        apply_window_icon()


def request_input(input_manager, prompt="> "):
    return input_manager.request_input(prompt)


def input_pending(input_manager):
    return input_manager.input_pending()
