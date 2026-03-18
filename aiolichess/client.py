"""Client for aiolichess."""
from __future__ import annotations
import aiohttp
from .exceptions import AuthError, RateLimitError, LichessServerError, AioLichessError
from .models import LichessUser, LichessPerf, LichessProfile, LichessCount, LichessStatistics

BASE_URL = "https://lichess.org"


class AioLichess:
    """Async client for the Lichess REST API."""

    def __init__(self, session: aiohttp.ClientSession | None = None) -> None:
        """Initialize the client."""
        self._session = session
        self._owns_session = session is None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Return existing session or create one."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _request(self, endpoint: str, token: str) -> dict:
        """Make an authenticated GET request to the Lichess API."""
        session = await self._get_session()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{BASE_URL}{endpoint}"

        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    raise AuthError("Invalid or missing API token.")
                elif response.status == 429:
                    raise RateLimitError("Rate limit hit. Wait 60 seconds before retrying.")
                elif response.status >= 500:
                    raise LichessServerError(f"Lichess server error: {response.status}")
                else:
                    raise AioLichessError(f"Unexpected status code: {response.status}")
        except aiohttp.ClientError as err:
            raise AioLichessError(f"Network error: {err}") from err

    async def _fetch_account(self, token: str) -> dict:
        """Fetch raw account data."""
        return await self._request("/api/account", token)

    async def get_all(self, token: str) -> LichessUser:
        """Get all account information for the authenticated user."""
        data = await self._fetch_account(token)

        perfs: dict[str, LichessPerf] = {}
        for format_name, perf_data in data.get("perfs", {}).items():
            if "rating" not in perf_data:
                continue
            perfs[format_name] = LichessPerf(
                rating=perf_data["rating"],
                games=perf_data["games"],
                rd=perf_data["rd"],
                prog=perf_data["prog"],
                prov=perf_data.get("prov", False),
            )

        profile = None
        if raw_profile := data.get("profile"):
            profile = LichessProfile(
                flag=raw_profile.get("flag"),
                location=raw_profile.get("location"),
                bio=raw_profile.get("bio"),
                fide_rating=raw_profile.get("fideRating"),
                uscf_rating=raw_profile.get("uscfRating"),
                ecf_rating=raw_profile.get("ecfRating"),
            )

        count = None
        if raw_count := data.get("count"):
            count = LichessCount(
                all=raw_count.get("all", 0),
                rated=raw_count.get("rated", 0),
                win=raw_count.get("win", 0),
                loss=raw_count.get("loss", 0),
                draw=raw_count.get("draw", 0),
            )

        return LichessUser(
            id=data["id"],
            username=data["username"],
            url=data["url"],
            created_at=data["createdAt"],
            seen_at=data["seenAt"],
            play_time=data["playTime"]["total"],
            perfs=perfs,
            profile=profile,
            count=count,
        )

    async def get_user_id(self, token: str) -> str:
        """Get the user ID of the authenticated user."""
        data = await self._fetch_account(token)
        return data["id"]

    async def get_username(self, token: str) -> str:
        """Get the username of the authenticated user."""
        data = await self._fetch_account(token)
        return data["username"]

    async def get_statistics(self, token: str) -> LichessStatistics:
        """Get rating statistics for all formats."""
        data = await self._fetch_account(token)

        perfs = data.get("perfs", {})

        def _rating(key: str) -> int | None:
            p = perfs.get(key)
            return p["rating"] if p and "rating" in p else None

        def _games(key: str) -> int | None:
            p = perfs.get(key)
            return p["games"] if p and "games" in p else None

        return LichessStatistics(
            bullet_rating=_rating("bullet"),
            blitz_rating=_rating("blitz"),
            rapid_rating=_rating("rapid"),
            classical_rating=_rating("classical"),
            puzzle_rating=_rating("puzzle"),
            correspondence_rating=_rating("correspondence"),
            bullet_games=_games("bullet"),
            blitz_games=_games("blitz"),
            rapid_games=_games("rapid"),
            classical_games=_games("classical"),
            puzzle_games=_games("puzzle"),
        )

    async def close(self) -> None:
        """Close the session only if we created it."""
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None