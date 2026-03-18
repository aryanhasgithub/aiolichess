"""Models for aiolichess."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class LichessPerf:
    """Represents a user's performance in a single game format."""

    rating: int
    games: int
    rd: int
    prog: int
    prov: bool = False


@dataclass
class LichessProfile:
    """Represents a user's public profile."""

    flag: str | None = None
    location: str | None = None
    bio: str | None = None
    fide_rating: int | None = None
    uscf_rating: int | None = None
    ecf_rating: int | None = None


@dataclass
class LichessCount:
    """Represents a user's game counts."""

    all: int = 0
    rated: int = 0
    win: int = 0
    loss: int = 0
    draw: int = 0


@dataclass
class LichessUser:
    """Represents a Lichess account."""

    id: str
    username: str
    url: str
    created_at: int
    seen_at: int
    play_time: int
    perfs: dict[str, LichessPerf] = field(default_factory=dict)
    profile: LichessProfile | None = None
    count: LichessCount | None = None

@dataclass
class LichessStatistics:
    """Represents a user's rating statistics across all formats."""

    bullet_rating: int | None = None
    blitz_rating: int | None = None
    rapid_rating: int | None = None
    classical_rating: int | None = None
    puzzle_rating: int | None = None
    correspondence_rating: int | None = None
    bullet_games: int | None = None
    blitz_games: int | None = None
    rapid_games: int | None = None
    classical_games: int | None = None
    puzzle_games: int | None = None