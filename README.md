# Farming-simulator

A simple farming simulator game built with Python and Pygame where you can plant crops, harvest them, sell to merchants, and even buy an AI helper to automate your farm!

## Requirements

To run this game, you'll need:
- **Python 3.6 through 3.13** (Python 3.14 is not yet supported by pygame)
  - **Recommended:** Python 3.12 or 3.13 for best compatibility
  - **Note:** If you have Python 3.14, you'll need to install Python 3.12 or 3.13 alongside it
- **Pygame library**

## Installation Instructions

### Step 1: Check if Python is Installed

Open your terminal/command prompt and run:

```bash
python --version
```

Or on some systems:

```bash
python3 --version
```

**What to look for:**
- ✅ **Good:** `Python 3.6.x` through `Python 3.13.x` - You're ready to go!
- ⚠️ **Not supported:** `Python 3.14.x` or higher - You'll need to install Python 3.12 or 3.13
- ❌ **Too old:** `Python 2.x.x` or `Python 3.5.x` or lower - Install a newer version

If you don't have a compatible Python version, proceed to install Python.

### Step 2: Install Python (if needed)

**If you have Python 3.14:**
You can keep Python 3.14 and install Python 3.12 or 3.13 alongside it. Both versions can coexist on your system. Just make sure to use the correct version when running the game (e.g., `py -3.12 Farmsim.py` on Windows).

**Windows:**
1. Download Python 3.12 or 3.13 from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important:** Check the box "Add Python to PATH" during installation
4. Click "Install Now"

**macOS:**
1. Download Python 3.12 or 3.13 from [python.org](https://www.python.org/downloads/)
2. Run the installer package
3. Follow the installation prompts

**Linux:**
Most Linux distributions come with Python pre-installed. If not, or if you need a specific version:
```bash
sudo apt update
sudo apt install python3.12 python3.12-pip
```

Or for Python 3.13:
```bash
sudo apt install python3.13 python3.13-pip
```

### Step 3: Check if Pygame is Installed

Run this command:

```bash
python -m pygame --version
```

Or:

```bash
python3 -m pygame --version
```

If you see a version number, Pygame is installed. If not, proceed to the next step.

### Step 4: Install Pygame

Using pip (Python's package manager):

```bash
pip install pygame
```

Or on some systems:

```bash
pip3 install pygame
```

Or if that doesn't work:

```bash
python -m pip install pygame
```

Or:

```bash
python3 -m pip install pygame
```

### Step 5: Verify Installation

To make sure everything is working, you can check both requirements:

```bash
python --version
python -m pip show pygame
```

## How to Run the Game

1. Navigate to the game directory:
```bash
cd path/to/Farming-simulator
```

2. Run the game:
```bash
python Farmsim.py
```

Or:
```bash
python3 Farmsim.py
```

**If you have multiple Python versions installed:**

Windows:
```bash
py -3.12 Farmsim.py
```
or
```bash
py -3.13 Farmsim.py
```

macOS/Linux:
```bash
python3.12 Farmsim.py
```
or
```bash
python3.13 Farmsim.py
```

## Game Controls

- **WASD** - Move your character (hold to keep moving)
- **Left Click** - Harvest mature crops or plant new ones
- **Walk to M** - Open the Merchant shop
- **Walk to S** - Access your Shed storage
- **ESC** - Quit the game or close menus

## Gameplay Features

- Plant and harvest corn and turnips
- Crops grow automatically over time
- Sell crops to the merchant for gold
- Buy an AI Helper that automatically harvests crops
- Store crops in your shed
- Watch your farm grow and prosper!

## Troubleshooting

**"Python is not recognized as an internal or external command"**
- On Windows, you need to add Python to your PATH. Reinstall Python and make sure to check "Add Python to PATH"

**"No module named pygame"**
- Make sure you've installed pygame using pip as shown in Step 4

**"No module named 'setuptools._distutils.msvccompiler'" or pygame won't install**
- This typically means you have **Python 3.14** which pygame doesn't support yet
- Solution: Install **Python 3.12 or 3.13** from [python.org](https://www.python.org/downloads/)
- You can have multiple Python versions installed - just use the correct version to run the game

**"Permission denied" error when installing**
- Try adding `--user` flag: `pip install --user pygame`
- Or use `sudo` on Linux/Mac: `sudo pip install pygame`

**Game window doesn't open**
- Make sure your graphics drivers are up to date
- Try updating pygame: `pip install --upgrade pygame`

## Support

If you encounter any issues, make sure:
1. Python version is 3.6 or higher
2. Pygame is properly installed
3. You're running the command from the correct directory

Enjoy farming!