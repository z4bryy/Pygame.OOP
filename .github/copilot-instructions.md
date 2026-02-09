Purpose
-------
Short, focused guidance to help an AI agent become immediately productive in this small Pygame project.

Quick start (how this repo runs)
- Entrypoint: `main.py` (run the project from the workspace root).
- Runtime: requires Python and the `pygame` package. Typical run command (Windows PowerShell):

```powershell
python ./main.py
```

Big picture
- Minimal Pygame-based game. Key files:
  - `main.py` — project entrypoint / runner.
  - `config.py` — configuration constants (currently empty, used via `from config import *`).
  - `game/game.py` — contains the `Game` class and the main game loop skeleton.
  - `game/__innit__.py` — present but empty; note the filename is misspelled (should be `__init__.py`).

What to know and watch for (concrete, discoverable patterns)
- Several modules import configuration using `from config import *` (see `game/game.py`). Prefer reading `config.py` to discover constants; don't assume a rich config exists — it's currently empty.
- The `Game` class in `game/game.py` is the central object. Expect game loop, initialization, and Pygame lifecycle code to live there.
- The package initializer is misspelled: `game/__innit__.py`. This means `import game` may not behave as a package on Python versions that require `__init__.py` files. When modifying imports or running tests, first check whether the author intended `game` to be a package and, if so, create or rename `__init__.py`.

Developer workflows and assumptions
- No build system, no tests detected. Agents should avoid adding heavy infra without confirmation.
- Dependency management: add a lightweight `requirements.txt` with `pygame` if creating CI or instructions. For local development, installing `pygame` via pip is expected.
- Debugging locally: run `python main.py` from the repo root in PowerShell. If running in headless CI, set `SDL_VIDEODRIVER=dummy` or equivalent before importing pygame.

Project-specific conventions
- Files are simple modules (no package metadata). Keep changes minimal and preserve the current import style unless refactoring.
- Naming: constants likely in `config.py` (suggest using UPPER_SNAKE case); project currently uses broad imports (`from config import *`) — if you introduce names, check for collisions.

Integration points and external deps
- Primary external dependency: `pygame` (not declared in repo). No other external services observed.

Examples from the codebase
- `game/game.py` begins with:

```py
import pygame
from config import *

class Game:
    # game loop and initialization expected here
```

Actionable rules for an AI agent
1. Read `config.py` and `game/game.py` before making changes. Many assumptions about globals and constants will live in `config.py`.
2. Do not assume `game` is an importable package — verify presence/intent of `__init__.py` (`__innit__.py` is currently present and likely a typo).
3. When adding dependencies, update a `requirements.txt` and mention the platform (Windows PowerShell).
4. Keep changes small and visible: add a focused unit (a single new file or a small, well-tested change) and run `python main.py` to smoke-test.

If anything is unclear
- Ask the repo owner whether `game` should be a package (rename `__innit__.py` to `__init__.py`), and whether they want `requirements.txt` added.

Changed files to consider (for humans reviewing agent edits)
- `main.py` — entry point edits and run logic.
- `config.py` — add or change constants; watch for global imports.
- `game/game.py` — primary behavior; small, incremental edits are preferred.

Feedback request
- If you want these instructions to be stricter (coding style, test framework, CI rules) provide a short checklist and I will update this file.
