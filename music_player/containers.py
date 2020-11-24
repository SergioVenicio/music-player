import hashlib

from dependency_injector import containers, providers

from shared.hash.services.MD5 import MD5
from shared.file.services.FileDecoder.FileDecoder import FileDecoder
from shared.cache.services.RedisService import RedisService
from shared.file.services.Storage.LocalStorage import LocalStorage


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    file_decoder_service = providers.Factory(
        FileDecoder
    )

    cache_service = providers.Factory(
        RedisService
    )

    hash_service = providers.Factory(
        MD5,
        hasher=hashlib.md5
    )
    file_service = providers.Factory(
        LocalStorage,
        hash_service=hash_service
    )
