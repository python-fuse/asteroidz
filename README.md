# Asteroids Game 🚀

A classic Asteroids-style arcade game built with Python and Pygame. Navigate your spaceship through space, destroy asteroids, and survive as long as possible!

## Features

- **Classic Asteroids Gameplay**: Control a rotating spaceship in space
- **Smooth Movement**: Physics-based momentum system with realistic inertia
- **Shooting System**: Fire bullets with cooldown mechanics
- **Asteroid Spawning**: Procedurally spawned asteroids with random trajectories
- **Collision Detection**: Precise collision system between bullets, player, and asteroids
- **Lives System**: Multiple lives with invincibility frames after taking damage
- **Visual Feedback**: Player blinking during invincibility period
- **Sound Effects**: Shooting and explosion audio
- **Score System**: Track your performance as you destroy asteroids
- **Debug Mode**: Visual collision rectangles for development

## Controls

- **Arrow Keys**:
  - `Left/Right`: Rotate spaceship
  - `Up`: Thrust/Accelerate forward
- **Spacebar**: Shoot bullets
- **ESC**: Quit game

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the game files**
2. **Navigate to the game directory**:

   ```bash
   cd asteroids
   ```

3. **Create and activate virtual environment** (recommended):

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install pygame
   ```

### Quick Start (Using the provided script)

Make the startup script executable and run:

```bash
chmod +x asteroidz.sh
./asteroidz.sh
```

### Manual Start

```bash
python main.py
```

## Game Mechanics

### Player Ship

- **Lives**: Start with 3 lives
- **Movement**: Momentum-based physics with gradual acceleration/deceleration
- **Rotation**: Smooth 360-degree rotation
- **Invincibility**: Temporary invincibility after taking damage (3 seconds)
- **Shooting**: Limited rate of fire with cooldown system

### Asteroids

- **Spawning**: Automatic spawning at regular intervals
- **Movement**: Constant velocity in random directions
- **Collision**: Destroyed when hit by bullets
- **Scoring**: Points awarded for each asteroid destroyed

### Bullets

- **Lifetime**: Bullets automatically despawn after a set time
- **Direction**: Fire in the direction the ship is facing
- **Speed**: Fast-moving projectiles
- **Collision**: Destroy asteroids on impact

## Project Structure

```
asteroids/
├── main.py              # Game entry point
├── game.py              # Main game loop and logic
├── entities.py          # Game entities (Player, Bullet, Asteroid)
├── utils/
│   ├── constants.py     # Game constants and settings
│   └── ui.py           # UI components
├── assets/             # Game assets
│   ├── player.png      # Player sprite
│   ├── bullet_player.png # Bullet sprite
│   ├── asteroid1.png   # Asteroid sprites
│   ├── asteroid2.png
│   ├── explosion.png   # Explosion sprite
│   ├── shoot.mp3       # Shooting sound
│   ├── enemy_explode.wav # Explosion sound
│   └── squeak.mp3      # Additional sound
├── env/                # Virtual environment
└── README.md          # This file
```

## Code Architecture

### Entity System

- **Base Entity Class**: Common properties for all game objects
- **Player Class**: Handles input, movement, shooting, and damage
- **Bullet Class**: Projectile physics and collision
- **Asteroid Class**: Enemy movement and destruction
- **BulletsManager**: Manages bullet lifecycle and updates

### Key Classes

- `Entity`: Base class with position, collision, and rendering
- `Player`: Player-controlled spaceship with physics and input handling
- `Bullet`: Projectile with directional movement and lifetime
- `Asteroid`: Enemy objects with random movement patterns
- `BulletsManager`: Centralized bullet management system
- `Game`: Main game loop, event handling, and state management

## Customization

### Tweaking Game Settings

Edit `utils/constants.py` to modify:

- Window dimensions
- Sound file paths
- Game events

### Adjusting Player Properties

In `entities.py`, modify the `Player` class:

- `self.acceleration`: How fast the ship speeds up
- `self.rotation_speed`: How fast the ship rotates
- `self.shoot_delay`: Time between shots
- `self.lives`: Starting number of lives

### Bullet Properties

Modify the `Bullet` class:

- `self.speed`: Bullet velocity
- `self.lifetime`: How long bullets exist

## Development

### Debug Mode

Enable debug mode to see collision rectangles:

```python
player = Player(..., debug_mode=True)
```

### Adding New Features

- **Power-ups**: Extend the `Entity` class
- **Different Asteroid Types**: Modify the `Asteroid` class
- **Particle Effects**: Add to the rendering system
- **High Scores**: Implement score persistence

## Troubleshooting

### Common Issues

1. **"pygame not found"**:

   ```bash
   pip install pygame
   ```

2. **Audio not working**: Check that audio files exist in `assets/` directory

3. **Images not loading**: Verify all sprite files are in the `assets/` folder

4. **Game running too fast/slow**: Adjust the FPS setting in `game.py`

### Performance Tips

- The game runs at 60 FPS by default
- Collision detection is optimized for small numbers of entities
- Asset loading happens during gameplay (could be optimized)

## Contributing

Feel free to fork this project and submit pull requests for:

- Bug fixes
- New features
- Performance improvements
- Code cleanup

## License

This project is open source. Feel free to use and modify as needed.

## Credits

Built with Python and Pygame. Inspired by the classic Atari Asteroids game.

---

**Have fun playing!** 🎮✨
