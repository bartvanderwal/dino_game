# Software Guidebook

Voor de hoofdstukindeling volgen we vooral de Software Guidebook-benadering van Simon Brown. Waar een lokale onderwijsvertaling helpt, sluiten we ook aan op de structuur van AIM/ENE.

- Context
- Functional Overview
- Quality Attributes
- Constraints
- Principles
- Software Architecture
- Code
- Data
- Infrastructure Architecture
- Deployment
- Operation and Support
- Development Environment
- Decision Log

Deze guidebook gebruikt ook een vaste schrijfstijl. De regels hieronder houden de tekst technisch, precies en consistent.

- Technische documentatie hoort helder en ondubbelzinnig te zijn.
- Vermijd onnodige bijvoeglijke naamwoorden en bijwoorden, omdat die technische tekst vaak subjectiever en minder precies maken.
- Bad practice quote: "adjectives and adverbs sometimes make technical readers bark loudly and ferociously." Source: [Google Technical Writing, Clear Sentences](https://developers.google.com/tech-writing/one/clear-sentences#minimize_certain_adjectives_and_adverbs_optional)

## 1. Context

Deze guidebook beschrijft hoe de Dino Game functioneel, technisch en operationeel in elkaar zit.

Gebruik dit bestand als referentie voor:

- levelprogressie;
- powerups en shopgedrag;
- boss-entrances en speciale arena's;
- UI-, audio- en feedbackprincipes;
- runtime-, build- en deploygedrag.

## 2. Functional Overview

De game is een level-based runner met characterkeuze, powerups, mini-bosses, flight-secties en een finale met credits.

- De speler doorloopt ontworpen levels met leerbare obstaclepatronen.
- De shop en powerups geven tijdelijke boosts of bescherming, maar veranderen de basisregels niet.
- Boss fights en flight mode zijn expliciete spelmodes met eigen presentatie, pacing en audio.
- Verdere functionele details staan later in dit document onder powerups, bosses en levels.

### 2.1 Shop En Powerups

De badger shop verschijnt in het menu en vlak voor boss fights.

### 2.1.1 Beschikbare powerups

- `Extra Life`:
  - icoon: hartje;
  - effect: absorbeert één fatale hit;
  - gebruik: blijft als voorraad bewaard tot een botsing het item verbruikt.
- `Shield`:
  - icoon: schild;
  - effect: tijdelijke bescherming;
  - duur: `SHOP_SHIELD_MS = 5000`.
- `Coin Boost`:
  - icoon: muntjes `x2`;
  - effect: verdubbelt verzamelde coins tijdelijk;
  - duur: `SHOP_COIN_BOOST_MS = 60000`.
- `Jump Shoes`:
  - icoon: schoenen;
  - effect: hogere sprongen tijdelijk;
  - duur: `SHOP_JUMP_SHOES_MS = 30000`.

### 2.1.2 Activatiegedrag

- Aankopen in het startmenu worden bij run-start geactiveerd.
- Aankopen in de pre-boss shop worden geactiveerd zodra de speler de shop-overlay afsluit.
- Het schild en extra leven zijn verdedigende lagen; coin boost en jump shoes zijn tijdelijke boosts.

### 2.1.3 UI-richting

- De vier shop-items horen icon-first te zijn.
- Dezelfde iconen mogen later ook in de HUD gebruikt worden zodra losse uitgesneden assets beschikbaar zijn.
- De huidige HUD mag daarom iconen naast tekst tonen in plaats van alleen tekstregels.

### 2.1.4 Startmenu playerstatistieken

- Na characterselectie toont het startmenu onder de geselecteerde speler altijd drie voortgangsregels.
  - De eerste regel toont het huidige checkpoint-level van die speler.
  - De tweede regel toont het totale aantal verbruikte levens van die speler.
  - De derde regel toont de totale speeltijd van die speler over alle levels samen.
- Deze drie regels zijn character-specifiek: wisselen van geselecteerde speler wisselt direct de getoonde waarden.

### 2.2 Boss Entrances

Voor elk boss level stopt de endless-runner-flow kort in een statische hubscene.

- De speler kan daar links/rechts bewegen zoals in een boss arena.
- Links staat de badger shop.
- Rechts staat de entrance naar het gevecht.
- `Pijl omlaag` is context-afhankelijk in deze hubscene.
- Als de speler voor de badger shop staat en `Pijl omlaag` indrukt, opent de shop-overlay; daar kan de speler items bekijken en kopen.
- De pipe-achtige entrances gebruiken niet langer Mario-groen, maar een steenrode gradient zodat ze visueel meer als deze eigen gamewereld lezen.
- Als de speler bij de arena-ingang staat en `Pijl omlaag` indrukt, start het gevecht alleen als de vereiste loadout aanwezig is.
- Voor gewone boss-hubs betekent dat: eerst een ranged wapen kopen in de shop; zonder wapen weigert de ingang de crouch-interactie en verschijnt de melding `Buy a gun first!`.
- Voor de coyote-route is de uitzondering character-afhankelijk: roadrunner gebruikt daar `TNT`, terwijl andere speelbare karakters hun gewone ranged weapon nodig hebben.

### 2.2.1 Mini bosses

- Voor level 4 en level 7 staat rechts een arena-ingang.
- De speler kan eerst shoppen en daarna bewust het gevecht starten.
- Tussen level 5 en level 6 zit een afwijkende minibossflow: aan het einde van de pipe/flappy flight-sectie verschijnt een Zeppelin in de lucht in plaats van een ground-hub.
- Die Zeppelin wordt verslagen vanuit het eigen gele vliegtuig met een schot-aanval; de boss is dus onderdeel van `flight_mode` en niet van de gewone boss hub.

### 2.2.2 Zeppelin miniboss gedrag

- De Zeppelin komt eerst de stad in tijdens een korte `approach`-fase; daarna start pas de echte fight-fase.
- Tijdens deze encounter blijft de speler in `flight_mode`; er is dus geen ground reset of gewone boss hub tussen intro en gevecht.
- De Zeppelin gebruikt een sprite-based render zodra `assets/zeppelin.png` beschikbaar is; alleen zonder asset blijft de oudere procedurale fallback actief.
- Tijdens het gevecht kan het vliegtuig `3` treffers van zeppelin-projectiles opvangen voordat het neerstort.
- Zodra de Zeppelin verslagen is, blijft `flight_mode` actief en loopt de speler direct door naar level 6 in plaats van eerst terug naar een ground-scene te vallen.
- Na de eerste treffer rookt het vliegtuig periodiek ongeveer elke `4` seconden.
- Na de tweede treffer rookt het vliegtuig periodiek ongeveer elke `2` seconden.
- De derde treffer door een zeppelin-projectile veroorzaakt een crash.
- Een botsing met een pipe blijft direct fataal; pipe-collisions gebruiken dus geen hitpoint-systeem.
- De post-boss overgang mag de luchtarena pas loslaten nadat de defeat/explosion sequence visueel klaar is.
- Pas daarna schakelt de game terug van city-bossarena naar de cave-flight presentatie van level 6.
- Vlak voor level 7 slaat de vlucht om naar een noodlanding: de brandstof is op, het vliegtuig zakt vanzelf langzaam, omhoog sturen werkt niet meer en de speler moet landen op een runway.

Waarom:

- De overgang van level 5 naar 6 bouwt al een luchtmechanic op; een luchtboss benut die bestaande skill direct.
- Een ground-hub zou de opgebouwde flight-spanning onnodig onderbreken.
- De speler moet dezelfde besturing en voertuigfantasie behouden tijdens het gevecht.
- Een 3-hit vliegtuigstate maakt de fight minder binair en leesbaarder zonder pipes of arena-positioning ongevaarlijk te maken.
- Rookfeedback maakt schade zichtbaar in de wereld zelf, in lijn met het principe dat gameplay-impact niet alleen in tekst mag zitten.

### 2.2.3 Eindbaas level 10

- Voor de coyote-boss staat rechts een pijp.
- Die pijp gebruikt dezelfde look als andere pipe-entrances.
- De speler kan op die pijp springen en daarna met crouch, dus `Pijl omlaag`, de pijp in duiken.
- Dat duiken via de pijp start de ondergrondse boss arena alleen met de juiste boss-weapon: voor roadrunner is dat `TNT`, voor andere karakters hun gewone ranged weapon.
- De arena gebruikt een donkerdere, grijze grot-achtige achtergrond.
- Grote vallende bommen tonen een gele landingsgloed zolang ze nog in de lucht zijn.
- Zodra een grote bom ontploft, licht de cave kort op.

### 2.2.4 Documentatiegraad bosses

- De globale boss-entrances en de specifieke level-5/6 en level-10 regels zijn nu beschreven in deze SGB.
- Het volledige encountergedrag van de bird boss, cactus boss en final boss is nog niet overal systematisch uitgeschreven.
- Verdere iteraties op boss-balans, arena-flow en visuele feedback horen die encounterregels later ook expliciet per boss aan te vullen.

### 2.3 Level Systeem

- De game heeft `10` levels.
- Hoofdstuk `1` duurt `6` obstacles.
- Elk volgend level vraagt `3` obstacles meer dan het vorige.
- Bij elk nieuw level stijgt de scrollsnelheid met factor `1.1`.
- Score en level-progressie zijn losgekoppeld:
  - score komt uit punten, coins en boss rewards;
  - level-progressie komt uit het aantal cleared obstacles.
- Boss rewards volgen de benodigde hits:
  - miniboss `1`: `15` punten;
  - miniboss `flight Zeppelin`: `18` punten;
  - miniboss `2`: `15` punten;
  - eindbaas: `35` punten.

### 2.3.1 Obstakelgeneratiebeleid

- Levels `1` t/m `7` zijn primair leerbaar en gebruiken vaste obstaclepatronen.
- Vanaf level `8` is beperkte variatie toegestaan, maar alleen met curated templates (geen vrije RNG-combinatie van losse obstakels).
- Elke template voor level `8+` moet handmatig speelbaar gevalideerd zijn.
- Validatieregel: ook als een high-jump powerup leeg is, moet de speler met normale sprong een uitwijkroute of haalbare timing houden.
- Templates die directe "soft-lock" situaties kunnen veroorzaken (zoals te krappe multi-cactusketens zonder herstelmoment) zijn niet toegestaan.

### 2.3.2 Aantal obstacles per level

- Level `1`: `6` obstacles.
- Level `2`: `9` obstacles (`15` totaal).
- Level `3`: `12` obstacles (`27` totaal).
- Level `4`: `15` obstacles (`42` totaal).
- Level `5`: `18` obstacles (`60` totaal).
- Level `6`: `21` obstacles (`81` totaal).
- Level `7`: `24` obstacles (`105` totaal).
- Level `8`: `27` obstacles (`132` totaal).
- Level `9`: `30` obstacles (`162` totaal).
- Level `10`: `33` obstacles (`195` totaal).

### 2.4 Levels

### 2.4.0 Vogelgedrag

- `bird_low` is de basisvogel op de grondchapters: een enkele lage passage die vooral leert wanneer de speler moet bukken of springen.
- `bird_swarm` is een samengestelde passage van meerdere vogels tegelijk en doorbreekt bewust de gewone enkel-obstakelcadans.
- In level 5 gebruiken flight-vogels vaste veilige lanes binnen het gat tussen de pijpen; ze kiezen dus geen vrije botsingsroute door de hele luchtlaag.
- In level 8 hoort de eerste uitbreiding van grondvogels te zitten: vogels die tijdens hun passage ook verticaal bewegen in een eenvoudig patroon omhoog of omlaag.
- In level 9 mag vogelgedrag sneller worden en mag een passage een volledige sinus volgen, zodat een vogel over zijn hele schermpassage precies één volledige golf maakt.
- Nieuwe vogelpatronen moeten leesbaar blijven: de speler moet uit silhouette, hoogte en bewegingsrichting vroeg genoeg kunnen aflezen of springen, bukken of lateraal corrigeren nodig is.
- Vogelgedrag mag moeilijker worden per level, maar niet willekeurig; patronen horen curated en testbaar te blijven.

### 2.4.1 Level 1: `Enter Cactus Land...`

- Gebruikte muziek: runner-thema.
- Introductie van de woestijn.
- Basisobstakels: lage cactus, hoge cactus en lage vogel.
- Nog geen slang.

### 2.4.2 Level 2: `Snake Sands`

- Gebruikte muziek: runner-thema.
- Meer druk in de woestijn.
- Slangen komen erbij.
- Timing tussen vogel, cactus en slang varieert meer.

### 2.4.3 Level 3: `High Jump Ridge`

- Gebruikte muziek: runner-thema; na een geraakt water blok tijdelijk water-atmosphere-thema.
- Verticale sprongen worden belangrijker.
- Torencactus en high-jumpflow krijgen nadruk.
- Jump blocks kunnen regen, natte grond en bloemen triggeren.
- Dit level krijgt een moeilijk platform-jump moment: de endless runner-flow vertraagt hier kort en de speler moet op waterplanten landen om de snake pit door te komen.

### 2.4.4 Level 4: `Bird Boss Canyon`

- Gebruikte muziek: runner-thema in de aanloop; bird-boss-thema in de arena.
- Eerste minibossfase.
- Reuzenvogel-boss.
- Shop-hub vóór de arena-ingang.
- De bird boss start pas nadat de speler de obstacle-doelstand van level 4 heeft gehaald.
- De speler start de bird boss via het nest in de tree-hub (interactie op de entrance-zone), niet automatisch midden in de runnerflow.
- Na het verslaan van de bird boss keert de speler terug naar de tree-hub.
- De overgang naar level 5 gebeurt pas nadat de speler opnieuw bij het nest staat en daar bewust `DOWN` gebruikt om door te gaan.

### 2.4.5 Level 5: `Fly away`

- Gebruikte muziek: plane-level-5-thema tijdens de vlucht; zeppelin-boss-thema aan het einde.
- Eerste vliegtuighoofdstuk.
- Pijpen verschijnen als obstakels.
- Vliegtuig kan als pickup flight mode starten.
- Tijdens de flight-sectie vliegen er ook vogels tussen de pijpen door.
- Die vogels kiezen bewust een route net boven de onderpijp of net onder de bovenpijp, zodat ze zelf niet tegen de pijpen botsen.
- Tegen het einde van level 5 verschijnt een dubbele vogelpassage met tegelijk een bovenste en onderste vogel, zodat alleen de middellijn veilig blijft.
- Aan het einde van dit level verschijnt de Zeppelin-tussenbaas als luchtgevecht boven de stad.
- De speler blijft in het gele vliegtuig en schiet de Zeppelin neer voordat level 6 begint.

### 2.4.6 Level 6: `Blue Caverns`

- Gebruikte muziek: plane-level-6-thema.
- Tweede vliegtuighoofdstuk.
- Flight mode loopt direct door vanuit de zeppelin-fight aan het einde van level 5.
- De groene pijpen maken plaats voor blauwe cave hazards die als stalactieten en stalagmieten uit plafond en vloer groeien.
- Deze hazards bewegen langzaam op en neer door het gat tussen boven- en onderzijde te verschuiven.
- Ongeveer de helft van deze cave hazards heeft geen extra projectile-actie; die hazards moet de speler alleen ontwijken door strak te sturen.
- Van de resterende cave hazards laat ongeveer de helft een steen uit de bovenste stalactiet vallen en laat ongeveer de helft een rode magma-bal uit de onderste stalagmiet omhoog springen.
- Zowel de vallende steen als de magma-bal kondigen zich ruim van tevoren aan met een zichtbare marker op de spire; pas bij de echte launch of val klinkt `hiss.wav`.
- De waarschuwing zelf is niet dodelijk. Voor de speler blijft vóór de launch of val alleen de vaste stalactiet of stalagmiet gevaarlijk. Zodra de steen valt of de magma-bal springt, wordt dat bewegende object wel dodelijk.
- Dit maakt level 6 nadrukkelijk meer een stuurlevel: de speler moet vaker heen en weer werken door nauwere doorgangen en actieve projectiles, minder als een rustige endless flyer en meer in de richting van Gradius/Galaga-achtig lane management.
- Dit level gebruikt geen aparte miniboss-intro meer; het is juist de doorlopende cave-flight nasleep van de zeppelin-boundary fight.
- Aan het einde van deze cave-flight verschijnt eerst een brandstofwaarschuwing; daarna start en eindigt de noodlanding nog binnen level 6.
- Tijdens die noodlanding mag het vliegtuig nog wel links/rechts en sneller omlaag sturen, maar niet meer omhoog.
- Te laag landen naast de baan of rechts voorbij de runway vliegen is fataal.
- Level 7 start pas na een succesvolle landing en is daarna weer een grondfase zonder vliegtuig.

### 2.4.7 Level 7: `Cactus Fortress`

- Gebruikte muziek: runner-thema in de aanloop; cactus-boss-thema in de arena.
- Tweede minibossfase.
- Level 7 is volledig een grondhoofdstuk; de noodlanding hoort bij het einde van level 6.
- Grondgevecht tegen de reuzencactus.
- Shop-hub vóór de arena-ingang.

### 2.4.8 Level 8: `Wild Flats`

- Gebruikte muziek: runner-thema.
- Meer tempo en krappe obstacle-combinaties.
- Multi-cactus packs vragen snelle landingen.
- Hier verschijnen voor het eerst vogels die tijdens hun passage ook verticaal bewegen.
- De eerste verticale patronen blijven eenvoudig en lineair: een vogel gaat of omhoog of omlaag terwijl hij van rechts naar links over het scherm beweegt.

### 2.4.9 Level 9: `Running up the hill, and driving down`

- Gebruikte muziek: runner-thema tijdens de run-up; car-level-9-thema zodra de auto actief is.
- Voorbereiding op de eindbaas.
- Hogere reactiedruk en minder hersteltijd.
- Vogelzwermen doorbreken hier de oude enkelvoudige obstakelcadans.
- Vogels bewegen hier sneller dan in level 8.
- Naast lineaire verticale passages mag level 9 ook sinus-passages gebruiken.
- Level 9 houdt vogels in een hoge luchtzone: vogelpassages spelen bovenin het scherm en niet op of vlak boven de grondlijn.
- De opening van level 9 is geen vlakke runnerstrook meer: voordat de speler de auto bereikt, hoort de grond tijdens ongeveer `10` tot `15` seconden scrollen geleidelijk omhoog te lopen.
- Die run-up hoort niet als een volledig zichtbare driehoek of complete heuvel in beeld te staan. De camera blijft een runner-camera; de speler ziet dus alleen het lokale stuk grond rondom het karakter langzaam stijgen terwijl de wereld naar links scrollt.
- Tijdens deze run-up blijft de speler exact op dezelfde getekende grondlijn staan; de collision- en renderhoogte van de speler mogen dus niet onder de zichtbare heuvel zakken.
- Tijdens deze run-up blijft de gewone runnerdruk actief: tussen startpunt en auto blijven er dus ook springobstakels op de helling langskomen in plaats van een lege aanloop.
- Tegen het einde van deze run-up staat de auto hoog op de helling, ongeveer rond de middenhoogte van het scherm, zodat de overgang naar car mode als een klim naar boven voelt.
- De auto zelf moet ook in deze minimalistische stijl direct leesbaar zijn als auto: zichtbare wielen, een cabine en een duidelijke voorkant zijn onderdeel van die pickup- en overlay-presentatie.
- Een sinus-passage hoort over de volledige schermpassage precies één hele golf te maken, zodat begin, midden en eind van de beweging voorspelbaar blijven.
- In dit level staat ook de auto-instap: als de speler op de auto landt, stopt de sidescroll heel kort voor een instapsequence.
- Tijdens die korte stilval speelt eerst `KoyRoilers-car-engine-fail-356001.mp3` als stotterende start/instapcue.
- Zodra de instappauze voorbij is en `car_mode` actief blijft, loopt de motor door met `pixabay-flutie8211-6-cylinder-car-starting-in-garage-399661.mp3`.
- Tijdens de run-up gebruikt de game contextuele guidance: eerst `CLIMB THE HILL`; pas dicht bij de heuveltop en auto verschijnt `GET INTO THE CAR!`.

#### Car mode: snelheidsbesturing en HUD

- De speler besturt de autosnelheid met de pijltjestoetsen: pijl-rechts (`→`) versnelt, pijl-links (`←`) vertraagt.
- Er zijn vier snelheidstiers: `low`, `medium`, `high`, `super high`. Elke tier bepaalt de jumpvelocity voor de volgende sprong (zie `CAR_SPEED_TIER_JUMP_VELOCITIES`).
- Hoe hoger de snelheid, hoe hoger de auto springt bij een ramp. De breedte van het volgende ravijn (`cliff_gap`) bepaalt welke snelheidstier de speler minimaal nodig heeft om het te halen.
- De HUD toont linksboven de huidige snelheidstier als balkengrafiek én als tekst.
- De HUD toont ook de benodigde snelheid voor de **volgende** ramp/ravijn-combinatie, zodat de speler tijdig kan remmen of accelereren.
- Pijltjes (`←` / `→`) verschijnen in de HUD als visuele hint: `←` knippert rood als te snel voor de bocht, `→` knippert groen als de speler moet versnellen vóór de ramp.
- Het ravijn begint nooit direct na de ramp. De volgorde is altijd: ravijn → ramp (de ramp staat aan de **overkant** van het ravijn, zodat de speler over het gat springt en landt op de ramp).
- De afstand tussen opeenvolgende cliff_gap-obstakels is minimaal `480px` zodat de speler voldoende reactietijd heeft.

### 2.4.10 Level 10: `Giant Town`

- Gebruikte muziek: runner-thema in de aanloop; coyote-boss-thema in de eindbaas-arena.
- Eindbaasfase.
- Reuzenvariant per karakter:
  - dino: `ReuzenDino`;
  - cowboy: `ReuzenCowboy`;
  - roadrunner: `ReuzenCoyote`.
- Voor de coyote-route loopt de speler eerst via de shop-hub naar een pijp.
- De coyote wordt verslagen door `5` grote bommen terug te gooien.

## 3. Quality Attributes

Elk principe en elke structurele beslissing in dit document bevat expliciet een `Waarom`.

- Zonder rationale zijn regels lastig te toetsen en verouderen ze sneller.
- Met rationale kunnen we wijzigingen evalueren op intentie, niet alleen op letterlijke tekst.

### 3.1 Exception Visibility

Exceptions worden niet stil ingeslikt.

Waarom:

- Een fout zonder logregel is in praktijk nauwelijks te debuggen, zeker in de web-runtime.
- Stil ingeslikte exceptions maken regressies onzichtbaar en laten kapot gedrag doorgaan alsof het "gewoon niet ondersteund" is.
- Browser-, audio- en assetproblemen moeten direct herleidbaar zijn naar de callsite en het bestand dat faalt.

- Geen `except Exception: pass` in projectcode.
- Als een exception bewust wordt opgevangen om runtime of tooling overeind te houden, log dan minimaal context, exceptiontype en melding naar console of stderr.
- Bij herhaalbare runtimefouten mag logging gededupliceerd worden om spam te beperken, maar de eerste fout moet zichtbaar blijven.

### 3.2 Platform Parity (DEV/PROD)

Lokaal draaien en web-deploy moeten dezelfde game opleveren qua gedrag.

Waarom:

- We willen lokaal snel itereren in Python-modus, zonder dat gedrag later op web functioneel afwijkt.
- Dat voorkomt verrassingen bij release: wat lokaal speelbaar en correct is, moet online dezelfde mechanics tonen.
- Performance kan tussen runtime-omgevingen verschillen; daarom testen we naast lokaal ook regelmatig de web-build zelf.

- Geen platform-specifieke gameplayregels: obstaclelogica, powerups, hitboxes, timing en scoreprogressie zijn identiek op desktop en web.
- Geen content-splitsing per platform: levels, patterns en balanswaarden worden centraal beheerd en niet gedupliceerd in `if IS_WEB` versus lokaal.
- Platform-afhankelijke code mag alleen voor technische runtime-zaken (bijv. input/audio unlock, packaging, pad-resolutie), nooit voor gamebalans of mechanics.
- Performanceproblemen worden opgelost met generieke optimalisaties die overal gelden (assets, renderpad, objectbeheer), niet met afwijkende spelregels op web.

## 4. Constraints

### 4.1 Framework Boundary

De map `processing/` is frameworkcode en heeft een andere wijzigingsdrempel dan gamecode zoals `dino_game.py`.

Waarom:

- Een wijziging in `processing/` heeft een veel grotere blast radius dan een wijziging in één sketch.
- Frameworkwijzigingen veranderen impliciet het contract voor alle sketches en moeten daarom als library-werk behandeld worden, niet als lokale bugfix.
- Als een bug alleen in één game of sketch zichtbaar is, lossen we die standaard eerst in de appcode op. Alleen bij bewezen frameworkschuld en expliciete afstemming passen we `processing/` aan.

- Geen ad-hoc wijzigingen in `processing/` om een bug in één sketch te fixen.
- Eerst het owning codepad in de app zelf onderzoeken.
- Als een frameworkaanpassing toch nodig lijkt, eerst expliciet afstemmen en idealiter apart behandelen als library-bug of library-change.

## 5. Principles

In dit hoofdstuk staan de ontwerpprincipes die richting geven aan gameplay, visuele consistentie, foutgedrag en audiofeedback.

### 5.1 Creative Integrity

De game gebruikt dezelfde visuele taal op meerdere plekken.

- Sprite-based visualisation (`.png`) heeft de voorkeur boven ad-hoc getekende placeholders zodra een asset beschikbaar is.
- Interactieve keuzes gebruiken kleine, duidelijke kaders met een subtiele pulse of glow.
- Shop-items mogen dus niet ineens als totaal andere UI-componenten verschijnen als ze al als iconen in HUD of shop bestaan.
- Informatie met gameplay-impact moet leesbaar zijn in de wereld zelf, niet alleen als tekst erboven.
- Gevaar krijgt altijd een visuele cue: bijvoorbeeld een landingsgloed onder een vallende bom, of een arena die oplicht bij explosies.
- Level-flow is leerbaar: obstaclevolgordes zijn in basis scripted/hardcoded per level, zodat spelers patronen kunnen herkennen en verbeteren.
- Variatie mag alleen gecontroleerd: vanaf hogere levels uitsluitend via een kleine, vooraf ontworpen set veilige patroonblokken.
- Onmogelijke combinaties zijn verboden: runtime mag geen obstacleketens genereren die niet haalbaar zijn met normale timing/spronghoogte wanneer een powerup net is afgelopen.
- Luchtlevels gebruiken decoratieve parallax-wolken als sfeerlaag en leesbare snelheidsreferentie, nooit als obstacle of misleidende hitbox.
- Menu-tekst boven de luchtlaag gebruikt karakter-afhankelijke contrastkleuren en mag nooit visueel over elkaar heen vallen; titel, startprompt en character-select copy blijven gescheiden blokken.
- Een echte sprite-asset vervangt procedurale placeholder-tekeningen zodra zo'n asset beschikbaar en geschikt is.

### 5.2 Semi-Realistische Continuiteit

Interacties mogen gestileerd zijn, maar de wereld mag niet abrupt vergeten wat er net nog zichtbaar of fysiek aanwezig was.

Waarom:

- De game is arcadeachtig, maar voelt sterker als objecten en gevolgen logisch doorlopen in beeld.
- Een vliegtuigcrash die direct omslaat naar een grond-lijk zonder wrak of luchtobstakels breekt de ruimtelijke continuiteit.
- Semi-realistische consequentie maakt verlies, impact en level-geometrie leesbaarder zonder dat de game een simulator hoeft te worden.

- Bestaande wereldobjecten verdwijnen niet zomaar op het moment van impact als daar geen zichtbare reden voor is.
- Een crash in `flight_mode` hoort visueel eerst als vliegtuigcrash leesbaar te blijven voordat de game reset of naar een andere state springt.
- Obstakels en arena-elementen blijven in principe zichtbaar tijdens een defeat-state als zij direct onderdeel waren van de aanleiding van die defeat.
- Stylization is toegestaan, maar alleen zolang oorzaak en gevolg voor de speler visueel navolgbaar blijven.

### 5.2.1 Character Asset Contract

Voor character poses is een runtime sprite sheet niet verplicht, maar de assetset moet zich wel gedragen alsof de frames uit één sprite sheet komen.

Begrippen:

- `canvas`: de volledige rechthoek van een spritebestand, inclusief transparante marge.
- `crop`: hoe strak het zichtbare figuur uit een groter beeld is uitgesneden.
- `grondlijn`: de denkbeeldige horizontale lijn waarop voeten, poten of wielen de grond raken.
- `anchor`: het vaste referentiepunt waarmee een pose op dezelfde plek wordt getekend als de vorige pose.

Waarom:

- Het grootste risico bij losse PNG's is niet het ontbreken van een sheet, maar inconsistente canvasmaat, baseline en anchor tussen poses.
- Een crouch-pose die strakker of anders gecropt is dan de normale pose veroorzaakt zichtbaar verspringen tijdens posewissels, ook als de hitbox zelf correct blijft.
- Een sprite sheet maakt zulke afwijkingen snel zichtbaar, maar dezelfde discipline is ook mogelijk met losse bestanden.

- Losse PNG's per state zijn toegestaan; een sprite sheet is dus geen vereiste.
- Binnen één character-set moeten alle poses exact dezelfde canvasbreedte en canvashoogte hebben: dus echt dezelfde pixelmaat per bestand binnen die set.
- Binnen één character-set delen alle poses dezelfde grondlijn: voeten of laagste contactpunt landen op dezelfde horizontale lijn.
- Binnen één character-set delen alle poses dezelfde horizontale anchor, zodat een posewissel niet naar links of rechts "springt".
- Strakke crops zijn ondergeschikt aan consistentie: voeg liever transparante marge toe dan dat één pose kleiner of verschoven binnenkomt.
- De concrete pixelmaat hoeft niet vooraf globaal voor alle characters gelijk te zijn, maar wordt per character-set expliciet gekozen zodra de eerste definitieve asset van die set wordt ingevoerd.
- Zodra zo'n maat voor een character-set is gekozen, worden nieuwe poses in die set daarop gepad of uitgelijnd in plaats van opnieuw vrij gecropt.

Foutvoorbeelden:

- `normaal` is 220 x 160 pixels, maar `duck` is 184 x 109 pixels. Resultaat: de sprite lijkt kleiner te worden en verschuift bij het bukken.
- `normaal` heeft 18 pixels transparante ruimte onder de voeten, maar `duck` maar 2 pixels. Resultaat: de crouch-variant zakt visueel door de grond of schiet omhoog.
- `normaal` is gecentreerd op het midden van het canvas, maar `duck` is verder naar links gecropt. Resultaat: de pose "teleporteert" horizontaal tijdens het wisselen.
- `oops` is veel strakker uitgesneden dan `normaal`. Resultaat: dezelfde character voelt ineens alsof die van schaal verandert.

Goed voorbeeld:

- Als de dino-set eenmaal op een vaste pixelmaat is gezet, moeten `normaal`, `duck`, `oops` en eventuele extra poses allemaal precies diezelfde canvasmaat, grondlijn en anchor gebruiken, ook als de zichtbare dino in de crouch-versie lager of compacter is.

Repo-voorbeelden:

- Losse sprite: `assets/dino-transparant.png`
- Sprite sheet: `assets/plane-sprite.png`

![Voorbeeld losse sprite](../assets/dino-transparant.png)

![Voorbeeld sprite sheet](../assets/plane-sprite.png)

Waarom:

- De Chrome Dino-vluchtstukken voelen sterker als luchtspace wanneer de achtergrond subtiel meebeweegt.
- Parallax helpt snelheid en diepte lezen zonder extra gameplay-ruis toe te voegen.
- Wolken mogen de obstacleleesbaarheid niet aantasten; daarom blijven ze puur decoratief.
- Ook in het menu moet tekst boven de lucht onmiddellijk leesbaar blijven; gekozen karakter en luchtkleur bepalen dus mee welke donkere contrastkleur daar werkt.

![Cowboy dead](cowboy-dead.png)

### 5.3 Geen Defensieve Gameplay-Fallbacks

Gameplaycode mag niet stilletjes ander gedrag kiezen als een asset, API, state of aanname ontbreekt.

Waarom:

- Fallbacks maken fouten onzichtbaar en daardoor lastig te reproduceren.
- Testen wordt onbetrouwbaar als code onder onbekende omstandigheden "iets anders" doet dan het ontworpen gedrag.
- Bij AI-assisted development moeten ontbrekende assets, ontbrekende API's en kapotte aannames expliciet zichtbaar worden, anders bouwt de agent verder op een verborgen fout.
- Een hard failure met een duidelijke oorzaak is beter dan een speelbare maar verkeerde toestand.

- Geen stille fallback van ontbrekende gameplay-assets naar oude sprites.
- Geen alternatieve mechanics bij ontbrekende functies of ongeldige state.
- Geen brede `try/except` rond gameplaylogica om fouten te maskeren.
- Wel toegestaan: expliciete platform-adapters voor technische runtimeverschillen, mits gameplaygedrag gelijk blijft en fouten zichtbaar blijven.

### 5.4 Audio Feedback

Sprong-audio moet het type sprong duidelijk maken.

Waarom:

- Een high jump moet niet alleen visueel waarneembaar zijn, maar zowel visueel als auditief.
- Het `weeh`-geluid past bij dat high-jump moment en maakt het effect direct herkenbaar.
- Dit ondersteunt timingleren, vooral bij snelle obstacle-combinaties.
- Waar een file-backed SFX webproblemen geeft, mag een runtime-generated sound als technische fallback bestaan, zolang de functionele betekenis van de sprong helder blijft.

- Normale sprong: gebruik `jump.wav` voor alle karakters.
- Versterkte/high jump (duck-jump, high-jump powerup of actieve jump shoes): gebruik `weeh.wav` voor alle karakters.
- De noodlanding richting level 7 gebruikt `pixabay-arunangshubanerjee-cockpit-sound-of-landing-gear-deployment-aviation-audio-328162.mp3` als lange landing-alert; de donkere motorwolken tijdens die sequence gebruiken daarna bewust de kortere `hiss.wav`.
- De auto-instap in level 9 gebruikt twee aparte autosignalen: `KoyRoilers-car-engine-fail-356001.mp3` voor de korte instappauze en `pixabay-flutie8211-6-cylinder-car-starting-in-garage-399661.mp3` als doorlopende motorklank zolang de speler rijdt.
- Menu- en levelmuziek hebben nu een duidelijker rolverdeling: `big-coyote-in-the-tree-2.mp3` is de menu-track; `pixel-leap.mp3` is de standaard runner-track voor gewone grondlevels; flight-, car- en boss-secties gebruiken hun eigen expliciete tracks.

## 6. Software Architecture

### 6.1 Web Runtime en Packaging

De webbuild bestaat niet uit "los wat Python-bestanden in de browser draaien", maar uit een kleine bootstraplaag plus een gecomprimeerde app-bundle.

Waarom:

- Zonder dit mentale model is het lastig te begrijpen waarom lokaal en productie kunnen verschillen terwijl de broncode zelf gelijk lijkt.
- De browser voert de app niet rechtstreeks uit de repository uit, maar uit een opgebouwde en verpakte webbundle.
- Voor debugging van webdeploys moet duidelijk zijn welk deel runtime is, welk deel appcode is, en welk deel uit lokale mirror of externe CDN komt.

#### 6.1.1 Wat is de webbundle precies?

- Tijdens de build wordt eerst een tijdelijke stage-map opgebouwd in `.web-build/stage/`.
- Daarin worden de app-entrypoint (`main.py`), `processing/`, `assets/` en enkele begeleidende bestanden gekopieerd.
- Pygbag produceert vervolgens weboutput met `index.html` plus een gecomprimeerde app-bundle.
- In dit project wordt die gedeployde bundle na de build hernoemd naar een buildspecifieke bestandsnaam zoals `dino_game-v0.2.0-<build_id>.tar.gz`.
- De bootstrapcode in `index.html` haalt precies die buildspecifieke bundle op en pakt die uit in de virtuele filesystem van de wasm-runtime.
- De Python-code van de game zit dus inderdaad in die gedeployde bundle, samen met assets en frameworkbestanden.
- De CPython WebAssembly-runtime zelf zit daar niet in; die komt uit de pygbag-runtimebestanden zoals `pythons.js`, `main.js` en `main.wasm`.

#### 6.1.2 Wat betekent `bundle = "stage"` dan?

- In `scripts/web/default.tmpl` staat een Python-variabele `bundle = "stage"`.
- Dat is geen environmentvariabele en ook geen verwijzing naar productie.
- Die naam wordt alleen intern gebruikt als runtime-mountnaam voor het virtuele pad `/data/data/stage`.
- De mountnaam `stage` en de bestandsnaam van de gedeployde bundle zijn dus twee verschillende dingen.
- De live gedeployde productiebundle kan bijvoorbeeld `dino_game-v0.2.0-<build_id>.tar.gz` heten, terwijl die na uitpakken nog steeds onder `/data/data/stage` beschikbaar komt.

#### 6.1.3 Waarom bestaat die tarball überhaupt?

- De browser kan niet direct een hele Python-projectmap als lokale directory mounten.
- Een gecomprimeerde bundle maakt het mogelijk om de volledige app als één payload te downloaden en daarna in de virtuele wasm-filesystem uit te pakken.
- Daardoor kan `assets/main.py` in de browser draaien alsof het een gewone projectmap is.
- Het verschil tussen lokale preview en productie zit daardoor vaak niet in "de repo", maar in welke gegenereerde webbundle daadwerkelijk wordt geserveerd.

#### 6.1.4 Lokaal previewen versus productie

- `http://127.0.0.1:9000/` serveert de lokale gegenereerde webbundle uit `.web-build/output/`.
- `https://bartvanderwal.github.io/dino_game/` serveert de live gedeployde productiebundle vanaf GitHub Pages.
- De lokale preview gebruikt dus niet de live gedeployde productiebundle van GitHub Pages.
- Gelijke URL-structuur en gelijke template betekenen dus nog niet dat lokaal en productie dezelfde gegenereerde webbundle laden.

#### 6.1.5 Rol van CDN versus lokale mirror

- De appcode en game-assets horen uit de eigen build-output te komen, dus uit de buildspecifieke bundle en lokale bestanden onder `.web-build/output/`.
- De pygbag-runtimebestanden kunnen uit een externe CDN of uit een lokale mirror `cdn/0.9.3/` komen.
- In dit project staat `LOCAL_CDN` standaard op `1` in de buildscriptconfiguratie en de GitHub Pages workflow zet `LOCAL_CDN=1` ook expliciet aan.
- "CDN" is hier dus niet bedoeld als uitzondering, maar als lokaal meegesynchroniseerde runtime-map binnen de eigen deploy-output.
- Een verschil tussen lokaal en productie wijst in dit model meestal op een verschil in de daadwerkelijk geserveerde bundle of runtimebestanden, niet per se op een verschil in repository-broncode.

#### 6.1.6 C4 Context

```mermaid
C4Context
title Dino Game - System Context
UpdateLayoutConfig($c4ShapeInRow="1", $c4BoundaryInRow="1")

Person(player, "Speler", "Speelt de game in een desktop- of mobiele browser.")
System(webapp, "Dino Game Web App", "Canvas-game die lokaal of via GitHub Pages draait.")
System_Ext(hosting, "GitHub Pages / lokale webserver", "Serveert index.html, een buildspecifieke bundle en de lokale runtime-mirror.")
System_Ext(cdn, "Optionele externe pygbag CDN", "Alternatieve bron voor runtimebestanden als de lokale mirror niet wordt gebruikt.")

Rel_D(player, webapp, "Speelt", "Browser + invoer")
Rel_D(webapp, hosting, "Laadt webbuild vanaf", "HTTPS")
Rel_D(webapp, cdn, "Gebruikt runtimebestanden van indien lokale mirror uit staat", "HTTPS, optioneel")
```

#### 6.1.7 C4 Container

```mermaid
C4Container
title Dino Game - Container Diagram

Person(player, "Speler", "Gebruikt de game in een browser.")
System_Ext(hosting, "GitHub Pages / lokale webserver", "Publiceert de webbuild en lokale runtime-mirror.")
System_Ext(cdn, "Optionele externe pygbag CDN", "Fallback voor runtimebestanden.")

System_Boundary(webapp, "Dino Game Web App") {
  Container(shell, "HTML shell", "index.html", "Laadt de runtime, toont titel/versie en bevat het canvas.")
  Container(runtime, "Pygbag runtime", "pythons.js, main.js, main.wasm", "Initialiseert CPython in WebAssembly en start de app.")
  Container(vfs, "Virtuele filesystem", "/data/data/stage", "Bevat de uitgepakte app-bundle tijdens runtime.")
  Container(pyapp, "Python game app", "assets/main.py + processing/ + assets/", "Voert game-logica, rendering en audio aansturing uit.")
  Container(canvas, "Canvas renderer", "HTML5 canvas", "Toont de gameframes en touch-controls.")
}

Container_Ext(bundle, "App-bundle", "dino_game-v<version>-<build_id>.tar.gz", "Gecomprimeerde payload met Python-code, framework en assets.")
Container_Ext(localcdn, "Lokale runtime-mirror", "cdn/0.9.3/", "Meegeleverde runtimebestanden binnen de eigen deploy-output.")

Rel(player, shell, "Opent en gebruikt", "Browser")
Rel(shell, runtime, "Laadt", "Script tags")
Rel(runtime, bundle, "Downloadt en pakt uit", "HTTP + tar.gz")
Rel(runtime, localcdn, "Laadt runtimebestanden vanaf", "HTTP")
Rel(runtime, cdn, "Gebruikt als fallback", "HTTP, optioneel")
Rel(bundle, vfs, "Wordt uitgepakt naar", "Virtuele filesystem")
Rel(vfs, pyapp, "Levert projectbestanden aan", "Bestandstoegang")
Rel(pyapp, canvas, "Tekent spelwereld en UI op", "pygame-ce / SDL")
```

#### 6.1.8 C4 Component

```mermaid
C4Component
title Dino Game - Component Diagram of the Web Runtime

Person(player, "Speler", "Start de game en gebruikt keyboard, touch of muis.")
Container_Ext(hosting, "Hosting-output", "index.html, buildspecifieke bundle, cdn/0.9.3/, version.json", "De gebouwde webartifacten.")

Container_Boundary(webapp, "Dino Game Web App") {
  Component(shell, "HTML shell", "index.html", "Start de webapp en toont paginatitel, versie en canvas-host.")
  Component(bootstrap, "Bootstrap script", "pygbag template script", "Initialiseert de runtime en opent de buildspecifieke bundle.")
  Component(runtime, "Runtime loader", "pythons.js + main.js", "Laadt CPython wasm en browser-API-koppelingen.")
  Component(vfs, "Virtuele filesystem", "BrowserFS / in-memory FS", "Exposeert de uitgepakte bundle als projectmap.")
  Component(mainpy, "Game entrypoint", "assets/main.py", "Start setup, game loop, audio en scene-overgangen.")
  Component(framework, "Processing framework", "processing/", "Levert teken-, input- en runtime-abstrahering.")
  Component(assets, "Game assets", "assets/", "Bevat sprites, audio en overige contentbestanden.")
  Component(canvas, "Canvas host", "HTML5 canvas", "Ontvangt de uiteindelijke rendering van de game.")
}

Rel(player, shell, "Opent en bedient", "Browser")
Rel(shell, bootstrap, "Voert uit", "Inline script")
Rel(bootstrap, hosting, "Leest bundle en runtimebestanden vanaf", "HTTP")
Rel(bootstrap, runtime, "Start", "JavaScript")
Rel(runtime, vfs, "Mount en gebruikt", "BrowserFS API")
Rel(vfs, mainpy, "Maakt entrypoint beschikbaar", "Bestandstoegang")
Rel(mainpy, framework, "Gebruikt Processing-API voor runtime en drawing", "Python import")
Rel(mainpy, assets, "Laadt sprites, audio en data", "Bestandstoegang")
Rel(mainpy, canvas, "Rendert frames en UI", "pygame-ce / SDL")
```

#### 6.1.9 Debug-implicaties

- Een verschil tussen lokaal en productie kan ontstaan als `index.html` of de buildspecifieke bundle op productie nog van een oudere build komt.
- Runtime-fouten over missende assets of onverwachte paden betekenen in dat geval meestal dat de geladen webbundle niet overeenkomt met de verwachte build-inhoud.
- Het is daarom niet genoeg om alleen de repo-bron te inspecteren; voor webbugs moet ook de daadwerkelijk geserveerde live gedeployde productiebundle gecontroleerd kunnen worden.

## 7. Code

- Applicatiecode blijft bewust in de single-file modular monolith `dino_game.py`.
- `processing/` is frameworkcode en wordt niet licht aangepast voor sketchspecifiek gedrag.
- Tests mogen buiten de monolith staan, maar nieuwe gamefeatures horen standaard in de appcode.

### 7.1 Schermcoordinaten

- Deze game gebruikt schermcoordinaten, geen cartesisch assenstelsel zoals in een wiskundegrafiek.
- Het nulpunt `(0, 0)` zit linksboven in het venster.
- `x` groeit naar rechts.
- `y` groeit naar beneden.
- Een grotere `y` betekent dus visueel lager op het scherm, niet hoger.
- `GROUND_Y` is in deze code de grondlijn; vliegende obstacles zoals vogels mogen daar niet onder renderen.

Waarom:

- De game draait op onze Processing-achtige wrapper bovenop Pygame en volgt daarom het gewone schermmodel van beide omgevingen.
- De Pygame-documentatie zegt bij `pygame.mouse.get_pos()` dat de positie relatief is aan de `top-left corner of the display`.
- De Processing-documentatie beschrijft `mouseY` als de `current vertical coordinate of the mouse`, wat hier ook een scherm-`y` is en geen wiskundige `y`-as die omhoog groeit.
- Zonder deze afspraak ontstaan bugs waarbij objecten wel mathematisch lijken te stijgen of dalen, maar in de game uit de grond of buiten het speelvlak renderen.

## 8. Data

- De game gebruikt vooral in-memory state voor spelerstatus, levelprogressie, boss state en tijdelijke powerups.
- Asset manifests en runtime padresolutie zijn codegedreven in plaats van databasegedreven.
- Audio, sprites en creditsdata worden geladen uit de gebundelde assets.

## 9. Infrastructure Architecture

- GitHub Pages of een lokale webserver serveert `index.html`, runtimebestanden en de app-bundle.
- De pygbag runtime draait als CPython WebAssembly in de browser.
- Een lokale runtime-mirror onder `cdn/0.9.3/` kan onderdeel zijn van de deploy-output.

## 10. Deployment

- De build gebruikt `.web-build/stage/` als staginggebied en `.web-build/output/` als publiceerbare output.
- `scripts/web/build_web.sh` genereert de app-bundle, `index.html` en runtimebestanden.
- Buildspecifieke bundlenamen en `version.json` maken zichtbaar welke build draait.
- Zie ook het how-to-run deel in [README.md](../README.md): `Snelle Start Met Virtual Environment` voor native runnen en `WebAssembly Build (pygbag)` plus `Run local preview` voor web-build en preview.

## 11. Operation and Support

- Webproblemen worden onderzocht over drie lagen: broncode, gegenereerde webbundle en live gedeployde productiebundle.
- Browserconsole, stderr-logging en soft-exception logging zijn primaire supportinstrumenten.
- Audio heeft eigen webcompatibiliteitsregels en vraagt expliciete validatie van echte assetpaden.

### 11.1 Audioformaat en webcompatibiliteit

Wij houden audio-attributie in de lopende tekst traceerbaar. De korte `tata-taa`-stinger voor level-ups en mini-boss-overwinningen staat daarom in de broncode en assets als `pixabay-mini-boss-tadaa.mp3`, omdat deze guidebook expliciet vastlegt dat wij assetbestanden met copyright of attributie een duidelijke naam geven waarin de rechthebbende organisatie terugkomt. Bijvoorbeeld via de `pixabay-...` prefix.

Voor audio-assets in web builds (pygbag) geldt:

> ".wav and .mp3 are safe, .ogg is not always supported on all browsers"
> (pygbag README, 2024, [pygbag assets docs](https://github.com/pygame-web/pygbag#assets))

- .wav en .mp3 werken in alle moderne browsers, inclusief Safari/iOS.
- .ogg werkt niet in Safari/iOS en is dus niet universeel web-compatibel.
- Zie ook: [MDN Web Docs: Audio codecs](https://developer.mozilla.org/en-US/docs/Web/HTML/Supported_media_formats#browser_compatibility)

### 11.1.2 Bestandsnamen en brontraceerbaarheid

- Audiofilenames met attributie houden de bron zichtbaar in de bestandsnaam zelf.
- Pixabay-audio gebruikt daarom een `pixabay-...` prefix wanneer die bron expliciet traceerbaar moet blijven, zoals bij `pixabay-mini-boss-tadaa.mp3` en `pixabay-arunangshubanerjee-cockpit-sound-of-landing-gear-deployment-aviation-audio-328162.mp3`.
- Hetzelfde geldt voor `pixabay-flutie8211-6-cylinder-car-starting-in-garage-399661.mp3`; de bestandsnaam houdt daarmee expliciet de Pixabay-bron en de maker `flutie8211` zichtbaar.
- Creator-specifieke audio buiten Pixabay houdt de maker ook in de bestandsnaam, zoals `KoyRoilers-car-engine-fail-356001.mp3`.
- Deze traceerbaarheid hoeft niet opnieuw in de credits-roll te staan zolang de guidebook en assetnaam de bron ondubbelzinnig maken.

### 11.1.1 Waarom

- Fallbacks op .ogg/.mp3/.wav maken foutmeldingen onduidelijk en maskeren assetproblemen.
- Alleen het juiste, verwachte bestand wordt geladen; ontbreekt dat, dan volgt een duidelijke foutmelding.
- Dit voorkomt verwarring over ontbrekende of niet-universeel ondersteunde audioformaten en zorgt voor dev/prod parity.

## 12. Development Environment

- Deze game is ontwikkeld in Python 3 met als editor VS Code met gebruikmaking van CoPilot extensie voor agentic development. Zie verder de AGENTS.md voor hints voor AI/LLM agents en meer details.
- De game kan lokaal native of als webpreview worden gedraaid.
- **Native desktop venstergrootte:** `800 × 500` pixels (BASE_GAME_WIDTH / BASE_GAME_HEIGHT). Voor betere zichtbaarheid van detailrijke assets (bijv. DJ level visuals) zie issue #7 voor upscaling.
- Web-build gebruikt dezelfde logical resolution maar renderopschaling in browser; visuals zijn daar groter en scherper.
- Relevante scripts zijn onder meer `scripts/web/build_web.sh`, `scripts/web/run_web.sh` en `python3 -m py_compile dino_game.py`.
- Smalle regressietests horen dicht op de gewijzigde slice te zitten.

## 13. Decision Log

Wij leggen architectuurkeuzes vast in `docs/adr/`. Die map is de repo-interne decision log.

De volgende ADR's zijn op dit moment direct relevant voor deze guidebook:

- [docs/adr/000-adr-format-and-conventions.md](../docs/adr/000-adr-format-and-conventions.md)
- [docs/adr/001-switch-to-pygame-ce.md](../docs/adr/001-switch-to-pygame-ce.md)
- [docs/adr/002-secure-python-dependency-sourcing.md](../docs/adr/002-secure-python-dependency-sourcing.md)
- [docs/adr/003-single-file-modular-monolith.md](../docs/adr/003-single-file-modular-monolith.md)
- [docs/adr/004-dev-prod-runtime-parity-for-loading.md](../docs/adr/004-dev-prod-runtime-parity-for-loading.md)
- [docs/adr/005-semver-application-versioning.md](../docs/adr/005-semver-application-versioning.md)

ADR003 borgt de keuze voor een single-file modular monolith voor applicatiecode. ADR004 en ADR005 onderbouwen runtime-parity en application versioning; beide keuzes komen ook terug in dit guidebook. Voor de structuur van dit document volgen we Simon Brown (Software Architecture for developers, 2012) en stemmen we de uitwerking praktisch af op deze repo en de genoemde ADR's.

## Bronnen

In de lopende tekst verwijzen we naar Brown en AIM/ENE wanneer die bronnen de structuur of uitleg van deze guidebook sturen. Hieronder staat alleen de bronnenlijst zelf.

- Simon Brown. Software Architecture for Developers.
- AIM/ENE Software Guidebook. [https://aim-ene.github.io/pexe/docs/Projectresultaat/SoftwareGuidebook](https://aim-ene.github.io/pexe/docs/Projectresultaat/SoftwareGuidebook)
- Speluitleg en projectnotities: [dino.md](dino.md)
- Contributierichtlijnen: [CONTRIBUTING.md](CONTRIBUTING.md)
- Agent/projectrichtlijnen: [AGENTS.md](AGENTS.md)
