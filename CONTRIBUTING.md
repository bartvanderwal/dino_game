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

## Tip: geen `__pycache__` in je projectmap

Wil je geen lokale cache-mappen in je repo, gebruik dan:

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile dino_game.py
```

## Projectspecifiek

Deze codebase gebruikt een eigen Python Processing-implementatie. Controleer altijd de lokale API in:

- `api.md`
- `processing/`
- `sgb.md` voor gameplaysystems, levels, powerups en ontwerpprincipes

Ga niet uit van Java Processing-functies die niet in deze repo bestaan.

## Audio conversie met ffmpeg

Voor het converteren van audio (zoals m4a naar mp3) kun je [ffmpeg](https://ffmpeg.org/) gebruiken. Installeer ffmpeg via Homebrew:

```bash
brew install ffmpeg
```

Voorbeeld: converteer een m4a-bestand naar mp3:

```bash
ffmpeg -i input.m4a output.mp3
```

Zie de [officiële ffmpeg website](https://ffmpeg.org/) voor meer informatie en documentatie.
