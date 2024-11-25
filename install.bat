@echo off
if not exist ".venv" (
    python -m venv .venv
    call .venv\Scripts\activate
    echo Virtual environment created in %CD%\.venv
    :: pip install -r requirements.txt :: Installs the requirements.
    :: pip freeze > requirements.txt :: Creates the requirements.txt. DONT NEED THIS?
) else (
    call .venv\Scripts\activate
    echo Virtual environment already exists
)
pause