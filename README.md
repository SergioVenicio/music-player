# Music Player
This project is a open source web music player with python / django.

[![Build Status](https://travis-ci.org/SergioVenicio21/music-player.svg?branch=master)](https://travis-ci.org/SergioVenicio21/music-player)
[![Updates](https://pyup.io/repos/github/SergioVenicio21/music-player/shield.svg)](https://pyup.io/repos/github/SergioVenicio21/music-player/)
[![Python 3](https://pyup.io/repos/github/SergioVenicio21/music-player/python-3-shield.svg)](https://pyup.io/repos/github/SergioVenicio21/music-player/)
[![codecov](https://codecov.io/gh/SergioVenicio21/music-player/branch/master/graph/badge.svg)](https://codecov.io/gh/SergioVenicio21/music-player)

# INSTALL
``` console
python3 -m venv .venv
source .venv/bin/activate
pip install -r requeriments-dev.txt
```

# TESTS
``` console
flake8
pytest music_player --cov=music_player
```

# Usage
``` console
./manager makemigrations
./manager migrate
./manager runserver
```
