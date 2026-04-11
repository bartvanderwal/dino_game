# Python Processing Starter

This project provides a small Processing-like API on top of Pygame, using Python-style naming.
It is designed for quick visual programming, classroom demos, and beginner-friendly sketch workflows.

## Project Goal

The goal is to let you write simple sketches with minimal setup:

- define `setup()` for one-time initialization
- define `draw()` for frame-by-frame rendering
- call `run()` to start the sketch loop

You can use functions like `size()`, `background()`, `circle()`, `text()`, `image()`, and input callbacks.

## Preparation

1. Have Python!
2. Install Pygame using pip: `pip install pygame`
3. Copy the folder processing to your program's folder or to `/Lib/site-packages`

## Create Your First Sketch

Create a file like `my_sketch.py`:

```python
from processing import *

x = 0


def setup():
    size(800, 500)
    frame_rate(60)
    title("My First Sketch")


def draw():
    global x
    background(245)
    fill(80, 170, 255)
    no_stroke()
    circle(x, 250, 40)
    x = (x + 2) % width


run()
```

Run it with:

```powershell
python my_sketch.py
```

## API Documentation

See `api.md` for the full English API reference, including:

- public constants
- public runtime variables
- public functions
- optional callback handlers

## Notes

- Function and variable names follow `snake_case`.
- ESC closes the sketch window.
- The runtime supports both static and interactive sketch modes.

## WebAssembly Build (pygbag)

You can package `dino_game.py` for the browser (WASM) and embed it in a blog post.

### 1) Setup once

```bash
scripts/web/setup_web.sh
```

### 2) Build web version

```bash
scripts/web/build_web.sh
```

Output is copied to:

```text
.web-build/output/
```

### 3) Run local preview

```bash
scripts/web/run_web.sh
```

Then open:

```text
http://localhost:8000
```

### Blog embed idea

Host the generated `.web-build/output/` files on your site and embed with an iframe:

```html
<iframe
  src="https://bartvanderwal.nl/path-to-game/index.html"
  width="960"
  height="600"
  style="border:0;"
  loading="lazy"
  allowfullscreen
></iframe>
```

![alt text](assets/macbook.png)
