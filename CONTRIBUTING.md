# Contributing

Bedankt voor je bijdrage aan dit project.

## Werken met GitHub in deze repo

Werk in deze codebase vanuit de daadwerkelijke git-configuratie van de repo, niet op basis van aannames of oude projectnamen.

### Huidige remotes

- `origin`: `https://github.com/bartvanderwal/dino_game.git`
- `upstream`: `git@github.com:AIM-HBO-ICT-Voorlichting/python-processing.git`

### Praktische werkwijze

**Let op:** Alle commit messages en issues (inclusief titels, beschrijvingen en comments) zijn altijd in het Nederlands, niet in het Engels.

- In deze workspace lijken projectnaam, upstream-herkomst en actieve GitHub-repo op elkaar, maar ze zijn niet hetzelfde.
- Door altijd vanuit de echte remotes te werken voorkom je zoekwerk, verkeerde issue-links en acties in de verkeerde repository.

## Python syntax-check met `py_compile`

Python is geen klassieke compile-taal zoals C/Java, maar je kunt wel een snelle syntax-check doen met de standaard Python-module `py_compile`.

Belangrijk:

- `py_compile` is een ingebouwde Python-module (stdlib), geen projectmodule.
- Daarom werkt `py_compile` niet als los shell-commando.
- Je roept het aan via `python3 -m ...`.

Voor 1 bestand:

```bash
python3 -m py_compile dino_game.py
```

Als dit zonder output terugkomt, is de syntax in orde.

## Verschil tussen checken en runnen

- Syntax-check (geen gameplay, alleen parse/bytecode check):

```bash
python3 -m py_compile dino_game.py
```

- Echt uitvoeren en gedrag testen:

```bash
python3 dino_game.py
```

## Tip: geen `__pycache__` in projectmap

Wil je geen lokale cache-mappen in je repo, gebruik dan:

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile dino_game.py
```

## Projectspecifiek

Deze codebase gebruikt een eigen Python Processing-implementatie. Controleer altijd de lokale API in:

- `api.md`
- `processing/`
- `sgb.md` voor gameplaysystems, levels, powerups en ontwerpprincipes

## Audio conversie met ffmpeg

### Installatie

#### macOS

```bash
brew install ffmpeg
```

Dit installeert zowel `ffmpeg` als `ffprobe` (analyse-tool).

#### Linux (Debian/Ubuntu)

```bash
sudo apt-get install ffmpeg
```

#### Windows

Download van [ffmpeg.org](https://ffmpeg.org/download.html) of via Chocolatey:

```powershell
choco install ffmpeg
```

### Basisgebruik: Converteren m4a → mp3

```bash
ffmpeg -i input.m4a output.mp3
```

Dit converteert met standaard encoding (VBR, ~128 kbps).

### Geavanceerd: Stilte-trimming

#### Stap 1: Detect leading/trailing silence

```bash
ffmpeg -i input.m4a -af "silencedetect=n=-50dB:d=0.1" -f null - 2>&1 | grep silence
```

Output bevat: `silence_start=0.123456 silence_end=3.456789` (voorbeeldwaardes).

#### Stap 2: Berekenen trim-point

- `silence_end` minus 0.1 seconde = `trim_start` (retain ~100ms intro)
- Als `trim_start` < 0, dan `trim_start = 0`

#### Stap 3: Trim + convert naar mp3

```bash
ffmpeg -ss {trim_start} -i input.m4a -c:a libmp3lame -b:a 128k output.mp3
```

**Concreet voorbeeld:**

```bash
ffmpeg -ss 3.35 -i "input-file.m4a" -c:a libmp3lame -b:a 128k "output-file.mp3"
```

### Audio-formaten in dit project

Zie [ADR 006: Audio-format strategie](docs/adr/006-audio-format-strategy.md).

- **Runtime:** `.mp3` (enige format dat door de game geladen wordt)
- **Source:** `.m4a` (origineel formaat, behouden voor remixing; NIET geladen door game)
- **Fallback:** `.wav` alleen voor bestanden die niet kunnen worden geconverteerd

### Verificatie na conversie

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output.mp3
```

Toont de duur van het bestand (nuttig om te controleren of trimming correct werkte).

Zie de [officiële ffmpeg website](https://ffmpeg.org/) voor uitgebreidere documentatie.
