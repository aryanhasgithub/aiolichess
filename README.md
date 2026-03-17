# aiolichess

Async Python client for the [Lichess REST API](https://lichess.org/api).

## Installation
```bash
pip install aiolichess
```

## Quick Start
```python
import asyncio
from aiolichess import AioLichess

async def main():
    client = AioLichess()
    user = await client.get_all(token="your_pat_here")

    print(user.username)
    print(user.perfs["blitz"].rating)
    print(user.count.win)

    await client.close()

asyncio.run(main())
```

### With an external session
```python
import aiohttp
from aiolichess import AioLichess

async with aiohttp.ClientSession() as session:
    client = AioLichess(session=session)
    user = await client.get_all(token="your_pat_here")
```

## API Reference

### `AioLichess(session=None)`

The main client class.

| Parameter | Type | Description |
|---|---|---|
| `session` | `aiohttp.ClientSession \| None` | Optional external session. If not provided, one is created internally. |

---

### `await client.get_all(token)`

Fetches all account information for the authenticated user via `/api/account`.

| Parameter | Type | Description |
|---|---|---|
| `token` | `str` | Lichess personal API token |

Returns a `LichessUser` object.

---

### `await client.close()`

Closes the session. Only closes if the session was created internally — never closes an externally provided session.

---

### Models

**`LichessUser`**

| Field | Type |
|---|---|
| `id` | `str` |
| `username` | `str` |
| `url` | `str` |
| `created_at` | `int` |
| `seen_at` | `int` |
| `play_time` | `int` |
| `perfs` | `dict[str, LichessPerf]` |
| `profile` | `LichessProfile \| None` |
| `count` | `LichessCount \| None` |

**`LichessPerf`**

| Field | Type |
|---|---|
| `rating` | `int` |
| `games` | `int` |
| `rd` | `int` |
| `prog` | `int` |
| `prov` | `bool` |

**`LichessProfile`**

| Field | Type |
|---|---|
| `flag` | `str \| None` |
| `location` | `str \| None` |
| `bio` | `str \| None` |
| `fide_rating` | `int \| None` |
| `uscf_rating` | `int \| None` |
| `ecf_rating` | `int \| None` |

**`LichessCount`**

| Field | Type |
|---|---|
| `all` | `int` |
| `rated` | `int` |
| `win` | `int` |
| `loss` | `int` |
| `draw` | `int` |

---

### Exceptions

| Exception | Raised on |
|---|---|
| `AioLichessError` | Base exception, catch-all |
| `AuthError` | `401` — invalid or missing token |
| `RateLimitError` | `429` — rate limit hit, wait 60s |
| `LichessServerError` | `5xx` — Lichess server error |

## License

GPL-3.0