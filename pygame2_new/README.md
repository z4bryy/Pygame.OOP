# Super Mario - OOP Edition 🍄✨

Kompletní 2D Mario hra vytvořená v Pygame s použitím objektově orientovaného programování, pokročilými grafickými efekty a herními mechanikami.

## 🎮 Vlastnosti

### Základní herní mechaniky
- **3 unikátní levely** s postupně se zvyšující obtížností
- **3 životy** - hra končí po ztrátě všech životů
- **Nepřátelé** - Goomba houby, které můžete zničit skokem shora
- **Mince** - sbírejte pro zvýšení skóre
- **Platformy** - skákejte mezi detailními cihlovými platformami
- **Animovaná kamera** - sleduje hráče během hry

### 🎨 Pokročilé grafické efekty
- **Částicové efekty** - exploze při zabití nepřítele, skok, sebrání mince
- **Animace běhu** - Mario má animované nohy a ruce při běhu
- **Hvězdičkové efekty** - při speciálních událostech
- **Gradientní pozadí** - krásné nebe s přechody barev
- **Animované mraky** - pohybující se s kamerou
- **Stébla trávy** - detailní země
- **3D platformy** - cihlový vzor se stíny
- **Lesklé mince** - s rotací a odlesky
- **Power-up aury** - vizuální efekty při aktivaci

### ⚡ Power-upy
- **Extra život** 💚 - zelené srdce přidá život (max 3)
- **Speed Boost** 💙 - modrá šipka zrychlí Maria na 5 sekund

### 🎯 Combo systém
- Zabíjejte nepřátele v rychlém sledu pro combo multiplikátor!
- Každý další nepřítel v combu dává více bodů
- Combo se zobrazuje uprostřed obrazovky s pulzujícím efektem

### 🎨 Vylepšené GUI
- **Poloprůhledný panel** s informacemi
- **Srdíčka** pro životy (plné/prázdné)
- **Ikona mince** pro skóre
- **Progress bar** pro postup levely
- **Combo indikátor** s animací
- **Speed boost timer** s progress barem

## 🎯 Herní mechaniky

### Ovládání
- **←/→ nebo A/D** - pohyb doleva/doprava
- **MEZERNÍK** - skok
- **ENTER** - pokračování na další level
- **R** - restart hry (po game over nebo výhře)

### Jak hrát
1. Skákejte mezi platformami a vyhýbejte se nepřátelům
2. Sbírejte zlaté mince pro body (10 bodů za minci)
3. Skákejte na nepřátele shora pro jejich zničení (50+ bodů za combo)
4. Sbírejte power-upy pro extra životy a speed boost
5. Dorazte k zelené vlajce pro dokončení levelu
6. Dokončete všechny 3 levely a vyhrajte!

### Bodování
- **Mince**: 10 bodů
- **Zabitý nepřítel**: 50 bodů
- **Combo 2x**: 100 bodů
- **Combo 3x**: 150 bodů atd.
- **Extra život power-up**: 100 bodů
- **Speed boost power-up**: 50 bodů

## 🏗️ Struktura projektu (OOP)

```
pygame2_new/
├── main.py          # Hlavní vstupní bod hry
├── config.py        # Konfigurační konstanty
├── game.py          # Hlavní herní třída Game
├── player.py        # Třída Player (hráč) s animacemi
├── enemy.py         # Třída Enemy (nepřítel)
├── platform.py      # Třída Platform (platforma)
├── coin.py          # Třída Coin (mince)
├── flag.py          # Třída Flag (cílová vlajka)
├── level.py         # Třída Level (správa levelů)
├── particle.py      # Částicové efekty
├── powerup.py       # Power-up prvky
└── README.md        # Dokumentace
```

## 📦 Požadavky

- Python 3.x
- Pygame

## 🚀 Spuštění

```bash
# Instalace pygame (pokud ještě není nainstalován)
pip install pygame

# Spuštění hry
python main.py
```

## 🎨 Designové prvky

### Postavy a objekty
- **Mario**: Detailní postava s modrými kombinézami, červeným trikem, hnědými botami, bílými rukavicemi, čepicí s logem "M" a hnědým knírem
- **Goomba**: Hnědé houby s bílými tečkami, zlýma očima, zuby a mrzutým výrazem
- **Platformy**: Cihlový vzor s 3D efekty, maltou a stíny
- **Mince**: Zlaté 3D mince s symbolem "$", leskem a animací
- **Power-upy**: Zelená srdce (extra život) a modrá šipka (speed boost) s světélkováním

### Pozadí a prostředí
- **Obloha**: Gradientní přechod od světlejší k tmavší modré
- **Mraky**: Bílé animované mraky pohybující se s kamerou
- **Země**: Zelená tráva s animovanými stébly a hnědá zemina
- **Vlajka**: Zlatá koule na vrcholu, zelená vlajka se žlutou hvězdou

### Efekty
- **Částice**: Při skoku, zabití nepřítele, sebrání mince
- **Hvězdičky**: Při sebrání power-upu a dokončení levelu
- **Textové efekty**: "+10" při sebrání mince, "COMBO x2!" atd.
- **Aury**: Modrá aura při speed boostu

## 📝 Levely

### Level 1 - Úvodní 🟢
Jednoduchý level pro seznámení se s herními mechanikami.
- 6 platforem
- 8 mincí
- 3 nepřátelé
- 2 power-upy

### Level 2 - Střední obtížnost 🟡
Více vertikálních skoků a více nepřátel.
- 10 platforem
- 12 mincí
- 5 nepřátel
- 2 power-upy

### Level 3 - Těžký 🔴
Náročné skoky vyžadující přesnost, hodně nepřátel.
- 14 platforem
- 18 mincí
- 9 nepřátel
- 3 power-upy

## 🎓 OOP principy použité v projektu

- **Zapouzdření**: Každá herní entita má vlastní třídu s privátními atributy
- **Dědičnost**: Všechny entity sdílejí společnou logiku
- **Polymorfismus**: Každá entita má vlastní metodu draw() a update()
- **Abstrakce**: Herní logika oddělena od vykreslování
- **Kompozice**: Game třída obsahuje Level, který obsahuje Entity

## ✨ Nové featury v nejnovější verzi

### Částicové systémy
- ✅ `Particle` - základní částice pro exploze
- ✅ `StarParticle` - hvězdičky pro speciální události
- ✅ `CoinCollectEffect` - "+10" text při sebrání mince

### Power-up systém
- ✅ Extra život (zelené srdce)
- ✅ Speed boost (modrá šipka)
- ✅ Vizuální indikátory v GUI

### Animace
- ✅ Animace běhu Maria (nohy a ruce)
- ✅ Pulzující combo text
- ✅ Blikající text na obrazovkách
- ✅ Rotující mince
- ✅ Pohybující se mraky
- ✅ Konfety při výhře

### Combo systém
- ✅ Multiplikátor za zabití více nepřátel v řadě
- ✅ Vizuální zobrazení comba
- ✅ Timer pro udržení comba

Užijte si hru! 🎮✨🍄
