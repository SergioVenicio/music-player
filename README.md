# Music Player
This project is a open source web music player with python / django.

[![Build Status](https://travis-ci.org/SergioVenicio21/music-player.svg?branch=master)](https://travis-ci.org/SergioVenicio21/music-player)
[![Updates](https://pyup.io/repos/github/SergioVenicio21/music-player/shield.svg)](https://pyup.io/repos/github/SergioVenicio21/music-player/)
[![Python 3](https://pyup.io/repos/github/SergioVenicio21/music-player/python-3-shield.svg)](https://pyup.io/repos/github/SergioVenicio21/music-player/)
[![codecov](https://codecov.io/gh/SergioVenicio21/music-player/branch/master/graph/badge.svg)](https://codecov.io/gh/SergioVenicio21/music-player)

# INSTALL UNIX
``` console
python3 -m venv .venv
source .venv/bin/activate
pip install -r requeriments-dev.txt
```
# INSTALL WINDOWS
``` console
PY -3 -m venv .venv
.venv\Scripts\activate
pip install -r requeriments-dev.txt
pip install python-magic
pip install python-magic-bin
```
If you are in Microsoft Windows is necessary to copy the following [DLL](https://github.com/pidydx/libmagicwin64) files to windows os folder C:\Windows\System32.
If you using 64bits version of OS. 
``` console
pip install python-magic-win64
```

# TESTS
``` console
flake8
pytest music_player --cov=music_player
```

# Usage Unix
``` console
./manager makemigrations
./manager migrate
./manager runserver
```

# Usage Windows
``` console
\manager makemigrations
\manager migrate
\manager runserver
```