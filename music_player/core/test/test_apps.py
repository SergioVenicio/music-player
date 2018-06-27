from music_player.api.apps import ApiConfig
from music_player.core.apps import CoreConfig


def test_api_apps():
    assert ApiConfig.name == 'api'


def test_core_apps():
    assert CoreConfig.name == 'core'
