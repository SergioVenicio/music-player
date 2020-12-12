import hashlib

from dependency_injector import containers, providers

from shared.hash.services import MD5Service
from shared.file.services.Storage import LocalStorage
from shared.cache.services.RedisService import RedisService
from shared.file.services.FileDecoder import (
    AudioDecoder,
    ImageDecoder
)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    audio_decoder_service = providers.Singleton(
        AudioDecoder
    )

    image_decoder_service = providers.Singleton(
        ImageDecoder
    )

    cache_service = providers.Singleton(
        RedisService
    )

    hash_service = providers.Singleton(
        MD5Service,
        hasher=hashlib.md5
    )

    file_service = providers.Singleton(
        LocalStorage,
        hash_service=hash_service
    )
