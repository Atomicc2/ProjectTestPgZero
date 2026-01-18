# Platform Adventure Kodland

A simple platform game developed with **Pygame Zero**.

## Description

Control the hero to navigate through levels, collecting the objective while avoiding enemies! The game features:

- **Platform mechanics**: jumping and lateral movement
- **Enemies**: Bees and Barnacles that move and attack
- **Interactive menu**: with sound control
- **Animations**: animated character, enemies and objective

## How to Play

| Key | Action |
|-----|--------|
| **W** | Jump |
| **A** | Move left |
| **D** | Move right |
| **ESC** | Exit game |

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
pgzrun game.py
```

## Requirements

- Python 3.7+
- Pygame Zero (specified in `requirements.txt`)

## Project Structure

```
├── game.py                           # Main game code
├── mapa_plataformas.csv             # Level map
├── images/                          # Game images
├── music/                           # Music files
├── sounds/                          # Sound effects
└── kenney_new-platformer-pack-1.0/  # Kenney Assets
```

## Assets

The game uses sprites and sounds from **Kenney.nl** (see `kenney_new-platformer-pack-1.0/` folder).

---
