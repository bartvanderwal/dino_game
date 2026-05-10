# Changelog

Alle opmerkelijke wijzigingen in dit project staan in dit bestand geregistreerd.

## [0.6.0] — 2026-05-10

### Added
- DJ Jukebox menu met speelbare tracks en per-track visuele elementen.
- DJ level visuals voor tracks (assets/dj-level-visuals/) zodat plaatjes per liedje automatisch tonen.
- Water-atmosphere muziek voor level 3 conditioneel op natte grondtrigger.
- Level 3 water-jump-block mechanica met beschrijving in SGB.
- Skip-to-next functionaliteit in DJ mode (tracked in issue #6).

### Changed
- Migrated legacy audio format: `loading-atmosphere.*` → `water-atmosphere.*` voor semantische helderheid.
- SGB level 6 en 7 documenten verduidelijkt: noodlanding hoort bij level 6, level 7 is pure grondphase.
- SGB verwijderd verwarrende vliegtuig-references uit level 7.
- DJ menu UI verfijnd met betere track-selectie en play/stop feedback.

### Fixed
- Level 7 DALL·E-generation nu correct voorgesteld als ground boss stage (geen vliegtuig).
- SGB consistency tussen leve 6/7 documentatie en runtime behavior.

### Technical Notes
- Per-track DJ visuals gebruik caching (`DJ_TRACK_VISUAL_CACHE`) voor performance.
- Fallback naar standaard DJ poster bij ontbrekende level visuals.
- Audio asset naming houdt creator/bron zichtbaar (e.g., `pixabay-*`, `KoyRoilers-*`).

---

## [0.5.0] — 2026-04-XX

### Added
- AI-assisted agentic development setup met AGENTS.md guidelines.
- Mini-boss music tracks (Bird, Zeppelin, Cactus, Coyote).
- Zeppelin in-level 5 flight sequence.
- Car mode in level 9 (speed tiers, HUD, obstacle progression).
- Emergency landing sequence (level 6 → 7 transition).
- DJ menu stub with track browsing.

### Changed
- Audio production moved to mp3 for web parity (pygbag compatibility).
- Level structure clarified in SGB (flight sections, ground phases, boss arenas).
- Web build structure documented (bundle, staging, runtime mirror).

### Fixed
- Flight mode initialization at zeppelin boss transition.
- Boss music proxy compatibility across level transitions.
- Character crouch sprite consistency per character set.

---

*See [AGENTS.md](AGENTS.md) for AI agent development guidelines and [docs/sgb.md](docs/sgb.md) for architectural details.*
