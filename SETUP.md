# Maze Game Setup

This guide sets up the Maze Game project from a fresh computer. It covers the
tutorial, the complete reference game, tests, and optional development tools.

The project has no required third-party Python packages for the tutorial or the
tests. Python's standard library is enough. A virtual environment is still
recommended so optional tools do not affect the rest of your computer.

## 1. Install The Required Software

### Python

Download Python 3 from the official website:

https://www.python.org/downloads/

Use Python 3.11 or newer if possible.

Windows users: during installation, enable **Add Python to PATH**.

Check the installation in a new terminal:

```text
python3 --version
```

If `python3` is not recognised on Windows, use:

```text
python --version
```

The commands below use `python3`. On Windows, replace `python3` with `python`
when necessary.

### Git

Git records changes to the project and lets you download the repository.

Download Git from:

https://git-scm.com/downloads

Check the installation:

```text
git --version
```

### Code editor

Visual Studio Code is recommended, but any plain-text editor will work.

Download VS Code from:

https://code.visualstudio.com/

Inside VS Code, install the official **Python** extension. Do not install a
random extension that claims to be Python; choose the one published by
Microsoft.

## 2. Create Or Choose A Projects Folder

Choose a folder where you keep programming projects. The commands below create
one in your home folder.

macOS or Linux:

```text
mkdir -p ~/Code
cd ~/Code
```

Windows PowerShell:

```text
New-Item -ItemType Directory -Force "$HOME\Code"
Set-Location "$HOME\Code"
```

If you already have a projects folder, use that instead. `cd` means **change
directory**. The terminal always runs commands in its current directory.

## 3. Clone The Repository

Run this command inside your projects folder:

```text
git clone https://github.com/SovietMeteor10/maze_game_tutorial.git
```

Move into the new repository:

```text
cd maze_game_tutorial
```

Check that Git knows which repository you are in:

```text
git status
```

You should see the `main` branch and the repository status. If Git asks you to
sign in while cloning a public repository, check that the URL was typed
correctly and that Git itself installed successfully.

## 4. Create A Virtual Environment

A virtual environment is a private Python installation for this project. It
prevents optional tools for this project from interfering with other Python
projects.

Create it from the repository root:

```text
python3 -m venv .venv
```

Activate it on macOS or Linux:

```text
source .venv/bin/activate
```

Activate it in Windows PowerShell:

```text
.venv\Scripts\Activate.ps1
```

Activate it in Windows Command Prompt:

```text
.venv\Scripts\activate.bat
```

When activation works, your terminal usually shows `(.venv)` at the beginning
of its prompt. Check which Python is active:

```text
python --version
```

The exact version is less important than seeing Python 3. You can use `python`
inside the activated environment on every platform.

To leave the virtual environment later:

```text
deactivate
```

You must activate `.venv` again whenever you open a new terminal and want to use
the optional tools installed inside it.

## 5. Update Pip

`pip` installs Python packages. The game itself does not require any packages,
but update pip before installing optional development tools:

```text
python -m pip install --upgrade pip
```

Using `python -m pip` is safer than typing `pip` by itself because it makes
sure pip belongs to the Python environment currently in use.

## 6. Install Optional Development Tools

The project uses Ruff for formatting and linting. It is optional for learning
the first lessons, but recommended when checking the whole project:

```text
python -m pip install ruff
```

There is no required `requirements.txt` file. Do not install packages such as
Pygame for this project. The tutorial and reference game use the Python
standard library and terminal output.

## 7. Open The Project In VS Code

From the repository root, try:

```text
code .
```

If the `code` command is not available, open VS Code normally and choose:

```text
File > Open Folder
```

Select the `maze_game_tutorial` folder.

In VS Code, select the Python interpreter from `.venv`:

1. Open the Command Palette.
2. Choose **Python: Select Interpreter**.
3. Select the interpreter whose path contains `.venv`.

This matters because VS Code must use the same environment where Ruff was
installed.

## 8. Run The First Tutorial Example

Make sure the terminal is at the repository root. The root is the folder that
contains `game`, `tutorial`, `TASK.md`, and `plan.md`.

Run the first checkpoint:

```text
python tutorial/checkpoints/01_static_room.py
```

You should see a small ASCII room.

Run the first learner exercise:

```text
python tutorial/lessons/01_printing_static_room.py
```

Run its model answer:

```text
python tutorial/solutions/01_printing_static_room.py
```

Read the written lesson before moving to the next one:

```text
tutorial/lessons/01-printing-static-room.md
```

## 9. Follow The Tutorial Workflow

For every lesson:

1. Read the matching Markdown lesson in `tutorial/lessons/`.
2. Run the learner exercise in `tutorial/lessons/`.
3. Complete its `TODO` sections.
4. Run the exercise again.
5. Try a side quest from the written lesson.
6. Compare your result with the file in `tutorial/solutions/`.
7. Run the matching checkpoint in `tutorial/checkpoints/`.

For example, Lesson 4 uses:

```text
python tutorial/lessons/04_functions_collision_loop.py
python tutorial/lessons/04_functions_collision_loop.py --play
python tutorial/solutions/04_functions_collision_loop.py
python tutorial/checkpoints/04_functions_collision_loop.py
```

The default exercise and checkpoint runs do not wait for input. The `--play`
option is available on the movement exercises when you want to experiment.

## 10. Run All Tutorial Files

From macOS, Linux, or Windows PowerShell:

```text
for file in tutorial/checkpoints/*.py; do python "$file"; done
```

The shell loop above works in macOS and Linux. In Windows PowerShell, use:

```text
Get-ChildItem tutorial/checkpoints/*.py | ForEach-Object { python $_.FullName }
```

To run all learner exercises:

macOS or Linux:

```text
for file in tutorial/lessons/[0-9][0-9]_*.py; do python "$file"; done
```

Windows PowerShell:

```text
Get-ChildItem tutorial/lessons/[0-9][0-9]_*.py | ForEach-Object { python $_.FullName }
```

To run all model answers:

macOS or Linux:

```text
for file in tutorial/solutions/[0-9][0-9]_*.py; do python "$file"; done
```

Windows PowerShell:

```text
Get-ChildItem tutorial/solutions/[0-9][0-9]_*.py | ForEach-Object { python $_.FullName }
```

## 11. Run The Reference Game

The reference game is the complete product, not the first tutorial exercise.
Run it from the repository root:

```text
python -m game.main
```

Controls are shown in the game. The reference game uses the terminal's curses
interface and may need a reasonably large terminal window.

## 12. Windows Curses Setup

The tutorial works on Windows without extra packages. The complete reference
game imports Python's `curses` module, which is built into macOS and most Linux
installations but is not included with standard Windows Python.

Windows users have two options.

### Option A: Use Windows Subsystem For Linux

WSL gives you a Linux environment on Windows. Install it from Microsoft's
instructions, then clone and run the project inside the WSL terminal:

https://learn.microsoft.com/windows/wsl/install

The normal macOS/Linux commands in this document should then work.

### Option B: Install Windows curses support

Activate the virtual environment in PowerShell, then install the compatibility
package:

```text
python -m pip install windows-curses
```

Then try the game again:

```text
python -m game.main
```

If the terminal display behaves strangely, use WSL or run the tutorial
checkpoints instead. The tutorial does not require curses.

## 13. Run The Tests

The project uses Python's built-in `unittest` framework, so no test package is
required:

```text
python -m unittest discover -s game/tests -t .
```

You should see a summary ending in `OK`.

Run the test suite after making changes to the reference game. A failing test is
information about a behavior that changed; read the failure before changing
more code.

## 14. Run Formatting And Lint Checks

These commands require the optional Ruff installation:

```text
ruff check game tutorial
ruff format --check game tutorial
```

To automatically format Python files:

```text
ruff format game tutorial
```

Only format files after understanding that formatting changes whitespace and
line layout, not the intended behavior.

## 15. Check Python Syntax Without Running The Game

Compile all Python files:

```text
python -m compileall -q game tutorial
```

No output means compilation succeeded.

## 16. Useful Git Commands

Show the current branch and changed files:

```text
git status
```

Show the exact unstaged changes:

```text
git diff
```

Download updates from GitHub without changing your files immediately:

```text
git fetch origin
```

Update your local branch when you have no uncommitted work:

```text
git pull --ff-only origin main
```

Save your own changes locally:

```text
git add .
git commit -m "Describe what changed"
```

Upload your commit to GitHub:

```text
git push origin main
```

Do not use `git add .` or `git pull` blindly if you have work you do not
understand. Run `git status` first and ask for help if Git reports a conflict.

## 17. Troubleshooting

### `python3` or `python` is not recognised

Python is either not installed or is not on your PATH. Reinstall Python and
enable the PATH option on Windows. Open a new terminal after installation.

### `No module named game`

You are probably not in the repository root. Run `git status` and check that
the current folder contains the `game` directory. Then run:

```text
python -m game.main
```

### `No module named curses`

You are on Windows without curses support. Follow the Windows Curses Setup
section, or use the tutorial checkpoints instead.

### The terminal says the window is too small

Maximise the terminal window or reduce its font size. The reference game draws
a five-by-five tile viewport, so it needs more space than the small tutorial
checkpoints.

### A tutorial file waits for input

Most files run a scripted example. Check whether you added `--play` or whether
you are running one of the optional interactive movement modes. Press `q` to
leave an interactive exercise.

### Git says there are local changes before pulling

Do not delete files immediately. Run:

```text
git status
git diff
```

Save your work in a commit, or ask for help deciding whether the changes should
be kept before pulling.

## Quick Verification Checklist

After setup, these commands should all work from the repository root:

```text
python --version
git --version
python -m tutorial.checkpoints.01_static_room
python tutorial/checkpoints/01_static_room.py
python -m unittest discover -s game/tests -t .
python -m compileall -q game tutorial
```

The module form in the third command may not work on every checkpoint because
the checkpoint directory is intentionally a collection of standalone scripts.
The direct script form is the authoritative command.
