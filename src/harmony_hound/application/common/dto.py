from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class SongRecognitionResponse:
    subtitle: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    genre: Optional[str] = None
    album: Optional[str] = None
    label: Optional[str] = None
    released: Optional[date] = None
    spotify_url: Optional[str] = None
    deezer_url: Optional[str] = None
    youtube_url: Optional[str] = None


