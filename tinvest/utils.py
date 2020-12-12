import asyncio
import contextvars
import functools
import typing
from datetime import timezone

from .typedefs import AnyDict, datetime_or_str

__all__ = (
    'set_default_headers',
    'Func',
    'run_in_threadpool',
    'isoformat',
    'validate_token',
)


def set_default_headers(data: AnyDict, token: str) -> None:
    headers = data.get('headers', {})
    headers.setdefault('accept', 'application/json')
    headers.setdefault('Authorization', f'Bearer {token}')
    data['headers'] = headers


T = typing.TypeVar('T')  # pragma: no mutate


class Func:
    def __init__(
        self, func: typing.Callable, *args: typing.Any, **kwargs: typing.Any
    ) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_async = asyncio.iscoroutinefunction(func)

    async def __call__(self) -> None:
        if self.is_async:
            return await self.func(*self.args, **self.kwargs)
        return await run_in_threadpool(self.func, *self.args, **self.kwargs)


async def run_in_threadpool(
    func: typing.Callable[..., T], *args: typing.Any, **kwargs: typing.Any
) -> T:
    loop = asyncio.get_event_loop()
    child = functools.partial(func, *args, **kwargs)
    context = contextvars.copy_context()
    func = context.run
    args = (child,)
    return await loop.run_in_executor(None, func, *args)


def isoformat(dt: datetime_or_str) -> str:
    if isinstance(dt, str):
        return dt
    return dt.replace(tzinfo=timezone.utc).isoformat()


def validate_token(token: str) -> None:
    if not token:
        raise ValueError('Token can not be empty')
