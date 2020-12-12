from typing import Final

PRODUCTION: Final = 'https://api-invest.tinkoff.ru/openapi'
SANDBOX: Final = 'https://api-invest.tinkoff.ru/openapi/sandbox'
STREAMING: Final = 'wss://api-invest.tinkoff.ru/openapi/md/v1/md-openapi/ws'


def get_base_url(use_sandbox: bool) -> str:
    if use_sandbox:
        return SANDBOX

    return PRODUCTION
