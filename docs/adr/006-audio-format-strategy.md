# ADR 006: Audio-format strategie

**Status:** Geaccepteerd (2026-05-10)  
**Context:** Dino Game ondersteunt meerdere audioformaten (.wav, .m4a, .mp3). Voor webdeployments en onderhoudsbaarheid moeten we keuzes maken over welke formaten we runtime gebruiken versus brondocumentatie.  
**Beslissing:** We gebruiken **MP3 als primaryformaat** voor alle game-runtime audio. Originele bron-m4a's en -wav's worden behouden in source voor onderhoudbaarheid.

## Motivatie

### 1. Bestandsgrootte en webdeployment

- MP3 biedt goede compressie (128–192 kbps standaard) zonder kwaliteitsverlies voor SFX en loopable tracks
- WAV is ongecomprimeerd (~1 MB/sec stereo 44.1kHz) → problematisch voor web
- M4A (AAC) is even compact als MP3, maar MP3 is universeler

### 2. Compatibiliteit

- MP3 wordt door alle pygame-versies ondersteund
- pygame.mixer.music ondersteunt MP3out-of-the-box
- Geen extra codec-installaties nodig

### 3. Onderhoudsbaarheid

- Originele m4a's behouden voor regeneratie/remixing
- Converts zijn niet-destructief (src = bron, dist = derived)
- Silence-trimming wordt gedocumenteerd, niet opgeslagen in origineel

### 4. Trim-strategie
- **Leading silence:** Detecteer met ffmpeg `silencedetect`, trim 0.1s *before* silence-end (retain ~100ms intro)
- **Trailing silence:** Trim automatisch
- **Floating loops:** Geen padding nodig; pygame.mixer loopt naadloos

## Implementatie

### Audiobestanden in runtime
- **Game-runtime:** Uitsluitend `.mp3` bestanden laden
- **Source-bestanden:** `.m4a` (origineel formaat, NIET geladen door game)
- **Fallback:** `.wav` alleen voor bestanden die niet kunnen worden geconverteerd

### Conversie-proces
```bash
# Voorbeeld: stilte-trim + m4a → mp3
ffmpeg -i input.m4a -af "silencedetect=n=-50dB:d=0.1" -f null - 2>&1 | grep silence_start
# ... bereken trim_start = silence_end - 0.1 ...
ffmpeg -ss {trim_start} -i input.m4a -c:a libmp3lame -b:a 128k -q:a 5 output.mp3
```

### Originele bronnen
- Behouden voor documentatie ("wie heeft dit gemaakt", "waar vandaan")
- Mogen NIET in dino_game.py worden geladen
- Nuttig voor remixing/regeneratie

## Gevolgen

### Positief
- Smaller web deployments
- Consistente compressie kwaliteit
- Betere laadperformance
- Duidelijk onderscheid src ↔ dist

### Negative
- Extra conversie-stap in prep-fase
- Moet vooraf gediaan worden (niet runtime)

## Verwante besluiten
- ADR 004: Dev-prod runtime parity → originele m4a's niet ingeladen
- CONTRIBUTING.md: ffmpeg-instructies voor locale conversie
