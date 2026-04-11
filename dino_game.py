from processing import run, size, frame_rate, title, background, fill, rect, line, arc
from processing import image, text_size, text, load_image, no_fill, stroke, stroke_weight, no_stroke, millis
from processing import width, height, key, key_code, random
from processing import PI, TWO_PI
import pygame
import shared
import math

# Dino game assets
DINO_IMG = load_image("assets/dino-transparant.png")
DINO_OOPS_IMG = load_image("assets/dino-oops-transparant.png")
DINO_DUCK_IMG = load_image("assets/dino-duck-transparant.png")
COWBOY_IMG = load_image("assets/cowboy-transparant.png")
COWBOY_RUN_IMG = load_image("assets/cowboy-run-transparant.png")
COWBOY_FALL_IMG = load_image("assets/cowboy-fall-transparant.png")
COWBOY_DUCK_IMG = load_image("assets/cowboy-duck-transparant.png")
ROADRUNNER_IMG = load_image("assets/roadrunner-transparant.png")
ROADRUNNER_OOPS_IMG = load_image("assets/roadrunner-oops-transparant.png")
ROADRUNNER_DUCK_IMG = load_image("assets/roadrunner-duck-transparant.png")
AIRPLANE_IMG = load_image("assets/airplane-transparant.png")
BIRD_IMG = load_image("assets/bird-transparant.png")
SNAKE_IMG = load_image("assets/snake-transparant.png")
CACTUS_IMGS = [
    load_image("assets/cactus-transparant.png"),
    load_image("assets/3Cacti-transparant.png")
]

# Dino properties
DINO_X = 100
DINO_Y = 400
DINO_W = 60
DINO_H = 60
DUCK_H = 30
GRAVITY = 1.2
JUMP_VELOCITY = -18
HIGH_JUMP_VELOCITY = -22
HIGH_JUMP_WINDOW_MS = 500
FAST_FALL_EXTRA_GRAVITY = 2.0
BASE_SCROLL_SPEED = 6.0
LEVEL_SCORE_STEP = 10
LEVEL_SPEED_FACTOR = 1.1
LEVEL_BLINK_DURATION_MS = 1200
LEVEL_BLINK_INTERVAL_MS = 120
HIGH_JUMP_WARNING_DURATION_MS = 1800
AIRPLANE_WARNING_DURATION_MS = 1800
FLIGHT_PIPE_GAP_H = 150
FLIGHT_PIPE_WIDTH = 72
FLIGHT_PIPE_SPAWN_BASE_MS = 1500
FLIGHT_PLANE_SPEED = 5.0
FLIGHT_PIPE_POINTS = 2
GROUND_Y = 460

# Collision hitbox tuning (smaller than visual sprite for fair gameplay)
DINO_HITBOX_INSET_LEFT = 12
DINO_HITBOX_INSET_RIGHT = 12
DINO_HITBOX_INSET_TOP = 8
DINO_HITBOX_INSET_BOTTOM = 8
DINO_HITBOX_Y_OFFSET = 3

DINO_DUCK_HITBOX_INSET_LEFT = 8
DINO_DUCK_HITBOX_INSET_RIGHT = 8
DINO_DUCK_HITBOX_INSET_TOP = 6
DINO_DUCK_HITBOX_INSET_BOTTOM = 4
DINO_DUCK_HITBOX_Y_OFFSET = 2

OBSTACLE_CONFIG = {
    "cactus_low": {
        "img": CACTUS_IMGS[0],
        "w": 50,
        "h": 60,
        "y": 400,
        "hitbox_insets": (7, 7, 6, 4),  # left, right, top, bottom
        "points": 1,
    },
    "cactus_high": {
        "img": CACTUS_IMGS[0],
        "w": 56,
        "h": 88,
        "y": 372,
        "hitbox_insets": (8, 8, 8, 4),
        "points": 2,
    },
    "cactus_tower": {
        # 2x zo hoog als de lage cactus; doorgaans high jump nodig.
        "img": CACTUS_IMGS[0],
        "w": 72,
        "h": 120,
        "y": 340,
        "hitbox_insets": (10, 10, 8, 4),
        "points": 4,
    },
    "snake": {
        "img": SNAKE_IMG,
        "w": 54,
        "h": 30,
        "y": 430,
        "hitbox_insets": (6, 6, 6, 3),
        "extended_w": 108,
        "extended_hitbox_insets": (10, 10, 6, 3),
        "points": 5,
    },
    "bird_low": {
        "img": BIRD_IMG,
        "w": 56,
        "h": 34,
        "y": 390,
        "hitbox_insets": (8, 8, 6, 6),
        "points": 3,
        "requires_duck_score": True,
    },
    "airplane_pickup": {
        "img": AIRPLANE_IMG,
        "w": 120,
        "h": 44,
        "y": 378,
        "hitbox_insets": (8, 8, 6, 4),
        "points": 0,
    },
}

INFO_TEXT = [
    "SPACE of A: start / herstart",
    "Pijl omhoog: springen",
    "Pijl omlaag: duiken / sneller vallen in de lucht",
    "High jump: buk en spring binnen 0.5s",
    "Pijl links/rechts: character kiezen",
    "Punten: lage cactus +1, hoge cactus +2, torencactus +4",
    "Punten: bukken onder lage vogel +3, slang +5",
    "Vanaf level 5: spring op vliegtuig voor flight mode",
    "Flight mode: pijltjes bewegen, ontwijk pijpen",
    "P: pauze",
    "D: debug hitboxen",
    "I: dit infoscherm",
    "Q of ESC: afsluiten",
]

CHARACTER_ORDER = ["dino", "cowboy", "roadrunner"]
CHARACTER_CONFIG = {
    "dino": {
        "label": "Dino",
        "stand": DINO_IMG,
        "duck": DINO_DUCK_IMG,
        "oops": DINO_OOPS_IMG,
        "theme": {
            "bg": (245, 245, 245),
            "ground_fill": (200, 200, 200),
            "ground_line": (120, 120, 120),
            "text": (30, 30, 30),
            "accent": (70, 70, 70),
        },
    },
    "cowboy": {
        "label": "Cowboy",
        "stand": COWBOY_IMG,
        "run": COWBOY_RUN_IMG,
        "duck": COWBOY_DUCK_IMG,
        "oops": COWBOY_FALL_IMG,
        "theme": {
            "bg": (245, 220, 170),
            "ground_fill": (220, 175, 120),
            "ground_line": (150, 98, 50),
            "text": (60, 35, 20),
            "accent": (178, 84, 28),
        },
    },
    "roadrunner": {
        "label": "Roadrunner",
        "stand": ROADRUNNER_IMG,
        "duck": ROADRUNNER_DUCK_IMG,
        "oops": ROADRUNNER_OOPS_IMG,
        "theme": {
            "bg": (154, 214, 242),
            "ground_fill": (214, 200, 150),
            "ground_line": (121, 104, 76),
            "text": (16, 58, 88),
            "accent": (0, 112, 163),
        },
    },
}

# Game state
obstacle_x = 800
obstacle_type = "cactus_low"
bird_duck_scored = False

dino_y = DINO_Y
velocity_y = 0
on_ground = True
game_over = False
game_started = False
score = 0
JUMP_SOUND = None
CRASH_SOUND = None
HISS_SOUND = None
isDebugMode = False
is_ducking = False
game_paused = False
selected_character_idx = 0
active_character_key = "dino"
duck_jump_expires_ms = 0
is_fast_falling = False
current_level = 1
scroll_speed = BASE_SCROLL_SPEED
next_level_score = LEVEL_SCORE_STEP
level_blink_until_ms = 0
high_jump_warning_until_ms = 0
airplane_warning_until_ms = 0
pending_airplane_spawn = False
flight_mode = False
flight_plane_x = 0.0
flight_plane_y = 0.0
flight_pipe_spawn_due_ms = 0
flight_pipes = []
fly_left_pressed = False
fly_right_pressed = False
fly_up_pressed = False
fly_down_pressed = False
snake_hiss_played_for_current = False


def reset_game(show_splash=False):
    global dino_y, velocity_y, on_ground, score, game_over, game_started
    global is_ducking, game_paused, bird_duck_scored, duck_jump_expires_ms, is_fast_falling
    global current_level, scroll_speed, next_level_score, level_blink_until_ms
    global high_jump_warning_until_ms, airplane_warning_until_ms, pending_airplane_spawn
    global flight_mode, flight_plane_x, flight_plane_y, flight_pipe_spawn_due_ms, flight_pipes
    global fly_left_pressed, fly_right_pressed, fly_up_pressed, fly_down_pressed
    global snake_hiss_played_for_current
    dino_y = DINO_Y
    velocity_y = 0
    on_ground = True
    score = 0
    game_over = False
    game_started = not show_splash
    is_ducking = False
    game_paused = False
    bird_duck_scored = False
    duck_jump_expires_ms = 0
    is_fast_falling = False
    current_level = 1
    scroll_speed = BASE_SCROLL_SPEED
    next_level_score = LEVEL_SCORE_STEP
    level_blink_until_ms = 0
    high_jump_warning_until_ms = 0
    airplane_warning_until_ms = 0
    pending_airplane_spawn = False
    flight_mode = False
    flight_plane_x = 0.0
    flight_plane_y = 0.0
    flight_pipe_spawn_due_ms = 0
    flight_pipes = []
    fly_left_pressed = False
    fly_right_pressed = False
    fly_up_pressed = False
    fly_down_pressed = False
    snake_hiss_played_for_current = False
    spawn_obstacle("cactus_low")


def setup():
    global JUMP_SOUND, CRASH_SOUND, HISS_SOUND
    size(800, 500)
    frame_rate(60)
    title("Dino Game")
    reset_game(show_splash=True)

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception:
        return

    try:
        JUMP_SOUND = pygame.mixer.Sound("assets/audio/jump.wav")
    except Exception:
        JUMP_SOUND = None

    try:
        CRASH_SOUND = pygame.mixer.Sound("assets/audio/crash.wav")
    except Exception:
        CRASH_SOUND = None

    try:
        HISS_SOUND = pygame.mixer.Sound("assets/audio/hiss.wav")
    except Exception:
        HISS_SOUND = None


def get_dino_hitbox():
    dino_draw_y = get_dino_draw_y()
    if is_ducking and on_ground and not game_over:
        dino_h = DUCK_H
        inset_left = DINO_DUCK_HITBOX_INSET_LEFT
        inset_right = DINO_DUCK_HITBOX_INSET_RIGHT
        inset_top = DINO_DUCK_HITBOX_INSET_TOP
        inset_bottom = DINO_DUCK_HITBOX_INSET_BOTTOM
        y_offset = DINO_DUCK_HITBOX_Y_OFFSET
    else:
        dino_h = DINO_H
        inset_left = DINO_HITBOX_INSET_LEFT
        inset_right = DINO_HITBOX_INSET_RIGHT
        inset_top = DINO_HITBOX_INSET_TOP
        inset_bottom = DINO_HITBOX_INSET_BOTTOM
        y_offset = DINO_HITBOX_Y_OFFSET

    return (
        DINO_X + inset_left,
        dino_draw_y + inset_top + y_offset,
        DINO_W - inset_left - inset_right,
        dino_h - inset_top - inset_bottom,
    )


def choose_obstacle_type():
    if pending_airplane_spawn:
        return "airplane_pickup"

    # Level 1: nog geen slang.
    if current_level < 2:
        roll = int(random(0, 100))
        if roll < 52:
            return "cactus_low"
        if roll < 84:
            return "cactus_high"
        return "bird_low"

    # Level 2: slang komt erbij.
    if current_level < 3:
        roll = int(random(0, 100))
        if roll < 36:
            return "cactus_low"
        if roll < 66:
            return "cactus_high"
        if roll < 84:
            return "snake"
        return "bird_low"

    roll = int(random(0, 100))
    if roll < 35:
        return "cactus_low"
    if roll < 58:
        return "cactus_high"
    if roll < 68:
        return "cactus_tower"
    if roll < 82:
        return "snake"
    return "bird_low"


def spawn_obstacle(force_type=None):
    global obstacle_x, obstacle_type, bird_duck_scored
    global high_jump_warning_until_ms, airplane_warning_until_ms, pending_airplane_spawn
    global snake_hiss_played_for_current
    obstacle_type = force_type or choose_obstacle_type()
    obstacle_x = width + random(100, 300)
    bird_duck_scored = False
    snake_hiss_played_for_current = False
    if obstacle_type == "airplane_pickup":
        pending_airplane_spawn = False
        airplane_warning_until_ms = millis() + AIRPLANE_WARNING_DURATION_MS
    if obstacle_type == "cactus_tower":
        high_jump_warning_until_ms = millis() + HIGH_JUMP_WARNING_DURATION_MS


def get_flight_plane_rect():
    return (flight_plane_x, flight_plane_y, 88, 36)


def spawn_flight_pipe():
    gap_top = int(random(90, GROUND_Y - FLIGHT_PIPE_GAP_H - 50))
    flight_pipes.append({
        "x": width + 20,
        "gap_top": gap_top,
        "passed": False,
    })


def start_flight_mode():
    global flight_mode, flight_plane_x, flight_plane_y, flight_pipe_spawn_due_ms, flight_pipes
    global fly_left_pressed, fly_right_pressed, fly_up_pressed, fly_down_pressed
    global current_level, scroll_speed, next_level_score, level_blink_until_ms
    flight_mode = True
    flight_plane_x = 120.0
    flight_plane_y = float(GROUND_Y - 90)
    flight_pipe_spawn_due_ms = millis() + 400
    flight_pipes = []
    fly_left_pressed = False
    fly_right_pressed = False
    fly_up_pressed = False
    fly_down_pressed = False
    current_level += 1
    scroll_speed = BASE_SCROLL_SPEED * (LEVEL_SPEED_FACTOR ** (current_level - 1))
    next_level_score = current_level * LEVEL_SCORE_STEP
    level_blink_until_ms = millis() + LEVEL_BLINK_DURATION_MS


def is_snake_extended():
    if obstacle_type != "snake":
        return False
    return obstacle_x < DINO_X + 220


def get_obstacle_draw_rect():
    cfg = OBSTACLE_CONFIG[obstacle_type]
    draw_x = obstacle_x
    draw_y = cfg["y"]
    draw_w = cfg["w"]
    draw_h = cfg["h"]

    if obstacle_type == "snake" and is_snake_extended():
        draw_w = cfg["extended_w"]
        # Uitklappen rondom midden, zodat de slang zichtbaar langer wordt dichtbij de speler.
        draw_x = obstacle_x - (draw_w - cfg["w"]) // 2

    return draw_x, draw_y, draw_w, draw_h


def get_obstacle_hitbox():
    cfg = OBSTACLE_CONFIG[obstacle_type]
    draw_x, draw_y, draw_w, draw_h = get_obstacle_draw_rect()
    if obstacle_type == "snake" and is_snake_extended():
        inset_left, inset_right, inset_top, inset_bottom = cfg["extended_hitbox_insets"]
    else:
        inset_left, inset_right, inset_top, inset_bottom = cfg["hitbox_insets"]

    return (
        draw_x + inset_left,
        draw_y + inset_top,
        draw_w - inset_left - inset_right,
        draw_h - inset_top - inset_bottom,
    )


def rects_overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax + aw > bx and ax < bx + bw and ay + ah > by and ay < by + bh


def get_dino_draw_y():
    if is_ducking and on_ground and not game_over:
        return dino_y + (DINO_H - DUCK_H)
    return dino_y


def get_selected_character_key():
    return CHARACTER_ORDER[selected_character_idx]


def get_current_character_key():
    if game_started:
        return active_character_key
    return get_selected_character_key()


def get_theme():
    return CHARACTER_CONFIG[get_current_character_key()]["theme"]


def update_level_from_score():
    global current_level, scroll_speed, next_level_score, level_blink_until_ms, pending_airplane_spawn
    new_level = max(1, (score // LEVEL_SCORE_STEP) + 1)
    if new_level > current_level:
        current_level = new_level
        scroll_speed = BASE_SCROLL_SPEED * (LEVEL_SPEED_FACTOR ** (current_level - 1))
        next_level_score = current_level * LEVEL_SCORE_STEP
        level_blink_until_ms = millis() + LEVEL_BLINK_DURATION_MS
        if current_level >= 5 and not flight_mode:
            pending_airplane_spawn = True


def is_level_blink_active():
    return millis() < level_blink_until_ms


def should_show_blink_phase():
    return int(millis() / LEVEL_BLINK_INTERVAL_MS) % 2 == 0


def draw_hud(theme, force_visible=False):
    blink_active = is_level_blink_active() and not force_visible
    visible = True if force_visible else (not blink_active or should_show_blink_phase())

    if visible:
        fill(*theme["text"])
        text_size(24)
        text(f"Score: {score}", 20, 40)
        text(f"Level: {current_level}", width - 150, 40)

    # During blink, briefly show level-up cue in accent color.
    if is_level_blink_active() and should_show_blink_phase():
        fill(*theme["accent"])
        text_size(20)
        text(f"Level Up! x{LEVEL_SPEED_FACTOR}", width // 2 - 90, 40)


def draw_flight_pipes():
    for pipe in flight_pipes:
        x = int(pipe["x"])
        top_h = int(pipe["gap_top"])
        bottom_y = top_h + FLIGHT_PIPE_GAP_H
        bottom_h = GROUND_Y - bottom_y

        fill(74, 160, 90)
        rect(x, 0, FLIGHT_PIPE_WIDTH, top_h)
        rect(x, bottom_y, FLIGHT_PIPE_WIDTH, bottom_h)


def update_and_draw_flight_mode(theme, update_world=True):
    global flight_plane_x, flight_plane_y, flight_pipe_spawn_due_ms, score, game_over

    now = millis()
    if update_world:
        # Movement in left half of the screen.
        if fly_left_pressed:
            flight_plane_x -= FLIGHT_PLANE_SPEED
        if fly_right_pressed:
            flight_plane_x += FLIGHT_PLANE_SPEED
        if fly_up_pressed:
            flight_plane_y -= FLIGHT_PLANE_SPEED
        if fly_down_pressed:
            flight_plane_y += FLIGHT_PLANE_SPEED

        plane_w = 88
        plane_h = 36
        flight_plane_x = max(20.0, min((width // 2) - plane_w - 10, flight_plane_x))
        flight_plane_y = max(50.0, min(GROUND_Y - plane_h - 4, flight_plane_y))

        if now >= flight_pipe_spawn_due_ms:
            spawn_flight_pipe()
            spawn_delay = max(700, int(FLIGHT_PIPE_SPAWN_BASE_MS / max(0.8, scroll_speed / BASE_SCROLL_SPEED)))
            flight_pipe_spawn_due_ms = now + spawn_delay

        for pipe in flight_pipes:
            pipe["x"] -= scroll_speed
            if not pipe["passed"] and pipe["x"] + FLIGHT_PIPE_WIDTH < flight_plane_x:
                pipe["passed"] = True
                score += FLIGHT_PIPE_POINTS
                update_level_from_score()

        flight_pipes[:] = [p for p in flight_pipes if p["x"] + FLIGHT_PIPE_WIDTH > -20]

        # Plane hitbox vs pipes.
        plane_rect = get_flight_plane_rect()
        for pipe in flight_pipes:
            top_rect = (pipe["x"], 0, FLIGHT_PIPE_WIDTH, pipe["gap_top"])
            bottom_rect = (
                pipe["x"],
                pipe["gap_top"] + FLIGHT_PIPE_GAP_H,
                FLIGHT_PIPE_WIDTH,
                GROUND_Y - (pipe["gap_top"] + FLIGHT_PIPE_GAP_H),
            )
            if rects_overlap(plane_rect, top_rect) or rects_overlap(plane_rect, bottom_rect):
                game_over = True
                if CRASH_SOUND is not None:
                    CRASH_SOUND.play()
                break

    draw_flight_pipes()

    if isDebugMode:
        plane_rect = get_flight_plane_rect()
        no_fill()
        stroke(255, 0, 0)
        stroke_weight(2)
        rect(*plane_rect)
        for pipe in flight_pipes:
            rect(pipe["x"], 0, FLIGHT_PIPE_WIDTH, pipe["gap_top"])
            rect(
                pipe["x"],
                pipe["gap_top"] + FLIGHT_PIPE_GAP_H,
                FLIGHT_PIPE_WIDTH,
                GROUND_Y - (pipe["gap_top"] + FLIGHT_PIPE_GAP_H),
            )
        no_stroke()

    if millis() < airplane_warning_until_ms and not game_over:
        fill(*theme["accent"])
        text_size(20)
        text("Flight mode: stay left and dodge the pipes!", width // 2 - 170, 28)


def draw_rounded_rect_outline(x, y, w, h, radius, col, weight=2):
    # Rounded rectangle via lines + quarter arcs (API has no native rounded rect).
    stroke(*col)
    stroke_weight(weight)
    no_fill()
    line(x + radius, y, x + w - radius, y)
    line(x + radius, y + h, x + w - radius, y + h)
    line(x, y + radius, x, y + h - radius)
    line(x + w, y + radius, x + w, y + h - radius)
    arc(x + radius, y + radius, radius * 2, radius * 2, PI, PI + PI / 2)
    arc(x + w - radius, y + radius, radius * 2, radius * 2, PI + PI / 2, TWO_PI)
    arc(x + w - radius, y + h - radius, radius * 2, radius * 2, 0, PI / 2)
    arc(x + radius, y + h - radius, radius * 2, radius * 2, PI / 2, PI)
    no_stroke()


def draw_character_select(theme):
    text_size(22)
    fill(*theme["text"])
    text("Kies character: pijl links/rechts", width // 2 - 160, height // 2 + 72)

    card_w = 170
    card_h = 165
    gap = 26
    start_x = (width - (card_w * 3 + gap * 2)) // 2
    card_y = height // 2 + 92

    pulse = (math.sin(millis() / 180.0) + 1.0) * 0.5
    pulse_pad = int(5 + pulse * 6)
    pulse_weight = int(2 + pulse * 2)

    for idx, character_key in enumerate(CHARACTER_ORDER):
        character = CHARACTER_CONFIG[character_key]
        x = start_x + idx * (card_w + gap)

        fill(255, 255, 255)
        no_stroke()
        rect(x, card_y, card_w, card_h)
        draw_rounded_rect_outline(x, card_y, card_w, card_h, 14, theme["ground_line"], 2)

        preview = character["stand"]
        image(preview, x + 28, card_y + 16, 114, 96)

        fill(*theme["text"])
        text_size(20)
        text(character["label"], x + 46, card_y + 140)

        if idx == selected_character_idx:
            draw_rounded_rect_outline(
                x - pulse_pad,
                card_y - pulse_pad,
                card_w + pulse_pad * 2,
                card_h + pulse_pad * 2,
                18,
                theme["accent"],
                pulse_weight,
            )


def draw():
    global dino_y, velocity_y, on_ground, obstacle_x, score, game_over, game_started
    global is_ducking, bird_duck_scored, is_fast_falling, snake_hiss_played_for_current
    theme = get_theme()
    background(*theme["bg"])
    fill(*theme["ground_fill"])
    rect(0, GROUND_Y, width, 40)  # ground
    stroke(*theme["ground_line"])
    stroke_weight(2)
    line(0, GROUND_Y, width, GROUND_Y)
    no_stroke()

    if shared.show_info:
        shared.draw_info_screen(INFO_TEXT)
        return

    if not game_started:
        draw_dino()
        fill(*theme["text"])
        text_size(44)
        text("Dino Game", width // 2 - 105, height // 2 - 55)
        text_size(22)
        text("Start: SPACE of A", width // 2 - 95, height // 2 - 10)
        text("Spring: pijl omhoog", width // 2 - 110, height // 2 + 20)
        text("Duik: pijl omlaag (lucht = fast fall)", width // 2 - 188, height // 2 + 50)
        text("High jump: buk en spring binnen 0.5s", width // 2 - 190, height // 2 + 80)
        text("Info: I", width // 2 - 45, height // 2 + 110)
        draw_character_select(theme)
        return

    if flight_mode:
        update_and_draw_flight_mode(theme, update_world=(not game_paused and not game_over))
        draw_dino()
        if game_paused and not game_over:
            fill(40)
            text_size(34)
            text("Pauze", width // 2 - 55, height // 2 - 8)
            text_size(18)
            text("Druk op P om verder te gaan", width // 2 - 118, height // 2 + 22)
            draw_hud(theme)
            return
        if game_over:
            fill(255, 0, 0)
            text_size(40)
            text("Game Over!", width // 2 - 120, height // 2)
            draw_hud(theme, force_visible=True)
            fill(*theme["text"])
            text_size(22)
            text(f"Snelheid: x{round(scroll_speed / BASE_SCROLL_SPEED, 2)}", width - 230, 72)
            text("Druk op SPACE voor startscherm", width // 2 - 170, height // 2 + 40)
            return
        draw_hud(theme)
        return

    # Draw obstacle
    obstacle_cfg = OBSTACLE_CONFIG[obstacle_type]
    obstacle_draw_x, obstacle_draw_y, obstacle_draw_w, obstacle_draw_h = get_obstacle_draw_rect()
    image(obstacle_cfg["img"], obstacle_draw_x, obstacle_draw_y, obstacle_draw_w, obstacle_draw_h)
    draw_dino()

    if game_paused:
        fill(40)
        text_size(34)
        text("Pauze", width // 2 - 55, height // 2 - 8)
        text_size(18)
        text("Druk op P om verder te gaan", width // 2 - 118, height // 2 + 22)
        draw_hud(theme)
        return

    if millis() < high_jump_warning_until_ms and game_started and not game_over:
        fill(*theme["accent"])
        text_size(20)
        text("Prepare for high jump: duck first then quickly jump.", width // 2 - 235, 28)
    if millis() < airplane_warning_until_ms and game_started and not game_over:
        fill(*theme["accent"])
        text_size(20)
        text("Jump on the airplane to start flight mode!", width // 2 - 170, 56)

    if not game_over:
        # Dino jump physics
        if not on_ground:
            gravity_now = GRAVITY + (FAST_FALL_EXTRA_GRAVITY if is_fast_falling else 0)
            velocity_y += gravity_now
            dino_y += velocity_y
            if dino_y >= DINO_Y:
                dino_y = DINO_Y
                velocity_y = 0
                on_ground = True
                is_fast_falling = False

        obstacle_x -= scroll_speed

        if obstacle_type == "snake" and is_snake_extended() and not snake_hiss_played_for_current:
            snake_hiss_played_for_current = True
            if HISS_SOUND is not None:
                HISS_SOUND.play()

        if obstacle_type == "bird_low":
            dino_hitbox = get_dino_hitbox()
            obstacle_hitbox = get_obstacle_hitbox()
            if (
                is_ducking and on_ground and
                obstacle_hitbox[0] < dino_hitbox[0] + dino_hitbox[2] and
                obstacle_hitbox[0] + obstacle_hitbox[2] > dino_hitbox[0]
            ):
                bird_duck_scored = True

        obstacle_draw_x, _, obstacle_draw_w, _ = get_obstacle_draw_rect()
        if obstacle_draw_x < -obstacle_draw_w:
            gained_points = obstacle_cfg["points"]
            if obstacle_cfg.get("requires_duck_score", False) and not bird_duck_scored:
                gained_points = 0
            score += gained_points
            update_level_from_score()
            spawn_obstacle()

        if obstacle_type == "airplane_pickup":
            dino_hitbox = get_dino_hitbox()
            plane_hitbox = get_obstacle_hitbox()
            dino_bottom = dino_hitbox[1] + dino_hitbox[3]
            plane_top = plane_hitbox[1]
            overlap_x = (
                dino_hitbox[0] < plane_hitbox[0] + plane_hitbox[2] and
                dino_hitbox[0] + dino_hitbox[2] > plane_hitbox[0]
            )
            landing_on_top = overlap_x and velocity_y >= 0 and plane_top - 10 <= dino_bottom <= plane_top + 18
            if landing_on_top:
                is_ducking = False
                is_fast_falling = False
                velocity_y = 0
                on_ground = False
                start_flight_mode()
                draw_dino()
                draw_hud(theme)
                return

        # Collision detection
        dino_hitbox = get_dino_hitbox()
        obstacle_hitbox = get_obstacle_hitbox()
        if rects_overlap(dino_hitbox, obstacle_hitbox):
            game_over = True
            is_ducking = False
            if CRASH_SOUND is not None:
                CRASH_SOUND.play()

    if isDebugMode:
        no_fill()
        stroke(255, 0, 0)
        stroke_weight(2)
        rect(*get_obstacle_hitbox())
        no_stroke()

    if game_over:
        fill(255, 0, 0)
        text_size(40)
        text("Game Over!", width // 2 - 120, height // 2)
        draw_hud(theme, force_visible=True)
        fill(*theme["text"])
        text_size(22)
        text(f"Snelheid: x{round(scroll_speed / BASE_SCROLL_SPEED, 2)}", width - 230, 72)
        text("Druk op SPACE voor startscherm", width // 2 - 170, height // 2 + 40)
        return

    draw_hud(theme)

def key_pressed():
    global velocity_y, on_ground, game_started, isDebugMode, is_ducking
    global game_paused, selected_character_idx, active_character_key
    global duck_jump_expires_ms, is_fast_falling
    global fly_left_pressed, fly_right_pressed, fly_up_pressed, fly_down_pressed
    pressed_key = key.lower() if isinstance(key, str) else key
    shared.handle_common_keys(pressed_key, key_code, info_text=INFO_TEXT)
    if pressed_key in ("i", "q", "s"):
        return

    if shared.show_info:
        return

    if key in ("d", "D"):
        isDebugMode = not isDebugMode
        return

    if key in ("p", "P") and game_started and not game_over:
        game_paused = not game_paused
        return

    if game_over and key == " ":
        if active_character_key in CHARACTER_ORDER:
            selected_character_idx = CHARACTER_ORDER.index(active_character_key)
        reset_game(show_splash=True)
        return

    if not game_started and key_code == pygame.K_LEFT:
        selected_character_idx = (selected_character_idx - 1) % len(CHARACTER_ORDER)
        return

    if not game_started and key_code == pygame.K_RIGHT:
        selected_character_idx = (selected_character_idx + 1) % len(CHARACTER_ORDER)
        return

    if not game_started and key in (" ", "a", "A"):
        active_character_key = get_selected_character_key()
        reset_game(show_splash=False)
        return

    if game_paused:
        return

    if game_started and flight_mode and not game_over:
        if key_code == pygame.K_LEFT:
            fly_left_pressed = True
            return
        if key_code == pygame.K_RIGHT:
            fly_right_pressed = True
            return
        if key_code == pygame.K_UP:
            fly_up_pressed = True
            return
        if key_code == pygame.K_DOWN:
            fly_down_pressed = True
            return
        return

    if game_started and not game_over and key_code == pygame.K_DOWN:
        if on_ground:
            is_ducking = True
            duck_jump_expires_ms = millis() + HIGH_JUMP_WINDOW_MS
        else:
            is_fast_falling = True
        return

    if game_started and not game_over and key_code == pygame.K_UP and on_ground:
        # Buk-spring binnen half seconde geeft high jump.
        now = millis()
        jump_velocity = HIGH_JUMP_VELOCITY if now <= duck_jump_expires_ms else JUMP_VELOCITY
        is_ducking = False
        velocity_y = jump_velocity
        on_ground = False
        is_fast_falling = False
        duck_jump_expires_ms = 0
        if JUMP_SOUND is not None:
            JUMP_SOUND.play()


def key_released(released_key):
    global is_ducking, duck_jump_expires_ms, is_fast_falling
    global fly_left_pressed, fly_right_pressed, fly_up_pressed, fly_down_pressed
    if flight_mode:
        if released_key == pygame.K_LEFT:
            fly_left_pressed = False
        elif released_key == pygame.K_RIGHT:
            fly_right_pressed = False
        elif released_key == pygame.K_UP:
            fly_up_pressed = False
        elif released_key == pygame.K_DOWN:
            fly_down_pressed = False
        return

    if released_key == pygame.K_DOWN:
        if on_ground:
            duck_jump_expires_ms = millis() + HIGH_JUMP_WINDOW_MS
        is_ducking = False
        is_fast_falling = False


def draw_dino():
    if flight_mode:
        plane_x, plane_y, plane_w, plane_h = get_flight_plane_rect()
        image(AIRPLANE_IMG, plane_x, plane_y, plane_w, plane_h)
        if isDebugMode:
            no_fill()
            stroke(255, 0, 0)
            stroke_weight(2)
            rect(plane_x, plane_y, plane_w, plane_h)
            no_stroke()
        return

    dino_h = DUCK_H if (is_ducking and on_ground and not game_over) else DINO_H
    dino_y_draw = get_dino_draw_y()
    character = CHARACTER_CONFIG[get_current_character_key()]
    draw_x = DINO_X
    draw_w = DINO_W
    draw_h = dino_h
    if game_over:
        dino_sprite = character["oops"]
        if get_current_character_key() == "cowboy":
            # Cowboy falls backward and lies on the ground.
            draw_x = DINO_X - 10
            draw_w = 88
            draw_h = 40
            dino_y_draw = GROUND_Y - draw_h
    elif is_ducking and on_ground:
        dino_sprite = character["duck"]
    elif (
        get_current_character_key() == "cowboy" and
        game_started and
        not game_paused and
        on_ground
    ):
        # Simple walk cycle for cowboy: alternate stand/run frames.
        run_phase = int(millis() / 150) % 2
        dino_sprite = character["run"] if run_phase else character["stand"]
    else:
        dino_sprite = character["stand"]
    image(dino_sprite, draw_x, dino_y_draw, draw_w, draw_h)
    if isDebugMode:
        no_fill()
        stroke(255, 0, 0)
        stroke_weight(2)
        rect(*get_dino_hitbox())
        no_stroke()

run()
