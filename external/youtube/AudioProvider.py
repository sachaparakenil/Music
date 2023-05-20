import typing
from typing import List
from rapidfuzz.fuzz import partial_ratio
from ytmusicapi import YTMusic
from bs4 import BeautifulSoup
from requests import get
from unidecode import unidecode


def match_percentage(str1: str, str2: str, score_cutoff: float = 0) -> float:
    try:
        return partial_ratio(str1, str2, score_cutoff=score_cutoff)
    except:
        newStr1 = ""
        for eachLetter in str1:
            if eachLetter.isalnum() or eachLetter.isspace():
                newStr1 += eachLetter

        newStr2 = ""
        for eachLetter in str2:
            if eachLetter.isalnum() or eachLetter.isspace():
                newStr2 += eachLetter

        return partial_ratio(newStr1, newStr2, score_cutoff=score_cutoff)

ytmApiClient = YTMusic()

def _parse_duration(duration: str) -> float:
    try:
        mappedIncrements = zip([1, 60, 3600], reversed(duration.split(":")))
        seconds = 0
        for multiplier, time in mappedIncrements:
            seconds += multiplier * int(time)
        return float(seconds)
    except (ValueError, TypeError, AttributeError):
        return 0.0


def _map_result_to_song_data(result: dict) -> dict:
    song_data = {}
    artists = ", ".join(map(lambda a: a["name"], result["artists"]))
    video_id = result["videoId"]
    if video_id is None:
        return {}
    song_data = {
        "name": result["title"],
        "type": result["resultType"],
        "artist": artists,
        "length": _parse_duration(result.get("duration", None)),
        "link": f"https://www.youtube.com/watch?v={video_id}",
        "position": 0,
    }

    album = result.get("album")
    if album:
        song_data["album"] = album["name"]

    return song_data


def _query_and_simplify(searchTerm: str, filter: str) -> List[dict]:
    searchResult = ytmApiClient.search(searchTerm, filter=filter)
    return list(map(_map_result_to_song_data, searchResult))


def search_and_get_best_match(songName: str, songArtists: List[str], songAlbumName: str, songDuration: int) -> typing.Optional[str]:
    songTitle = create_song_title(songName, songArtists)
    song_results = _query_and_simplify(songTitle, filter="songs")
    songs = order_ytm_results(
        song_results, songName, songArtists, songAlbumName, songDuration
    )
    if len(songs) != 0:
        best_result = max(songs, key=lambda k: songs[k])
        if songs[best_result] >= 80:
            return best_result
    video_results = _query_and_simplify(
        create_song_title(songName, songArtists), filter="videos"
    )
    videos = order_ytm_results(
        video_results, songName, songArtists, songAlbumName, songDuration
    )
    results = {**songs, **videos}
    if len(results) == 0:
        return None
    resultItems = list(results.items())
    sortedResults = sorted(resultItems, key=lambda x: x[1], reverse=True)
    return sortedResults[0][0]


def order_ytm_results(results: List[dict], songName: str, songArtists: List[str], songAlbumName: str, songDuration: int) -> dict:
    linksWithMatchValue = {}
    for result in results:
        if result == {}:
            continue
        lowerSongName = songName.lower()
        lowerResultName = result["name"].lower()
        sentenceAWords = lowerSongName.replace("-", " ").split(" ")
        commonWord = False
        for word in sentenceAWords:
            if word != "" and word in lowerResultName:
                commonWord = True
        if not commonWord:
            continue
        artistMatchNumber = 0

        if result["type"] == "song":
            for artist in songArtists:
                if match_percentage(
                    unidecode(artist.lower()), unidecode(result["artist"]).lower(), 85
                ):
                    artistMatchNumber += 1
        else:
            for artist in songArtists:
                if match_percentage(unidecode(artist.lower()), unidecode(result["name"]).lower(), 85):
                    artistMatchNumber += 1
            if artistMatchNumber == 0:
                for artist in songArtists:
                    if match_percentage(unidecode(artist.lower()), unidecode(result["artist"].lower()),85):
                        artistMatchNumber += 1

        if artistMatchNumber == 0:
            continue
        artistMatch = (artistMatchNumber / len(songArtists)) * 100
        song_title = create_song_title(songName, songArtists)

        if result["type"] == "song":
            nameMatch = round(
                match_percentage(unidecode(result["name"]), unidecode(songName), 60),
                ndigits=3,
            )
        else:
            nameMatch = round(
                match_percentage(unidecode(result["name"]), unidecode(song_title), 60),
                ndigits=3,
            )
        if nameMatch == 0:
            continue
        albumMatch = 0.0

        if result["type"] == "song":
            album = result.get("album")
            if album:
                albumMatch = match_percentage(album, songAlbumName)

        delta = result["length"] - songDuration
        nonMatchValue = (delta ** 2) / songDuration * 100

        timeMatch = 100 - nonMatchValue

        if result["type"] == "song":
            if album is not None:
                if (match_percentage(album.lower(), result["name"].lower()) > 95 and album.lower() != songAlbumName.lower()):
                    avgMatch = (artistMatch + nameMatch + timeMatch) / 3
                else:
                    avgMatch = (artistMatch + albumMatch + nameMatch + timeMatch) / 4
            else:
                avgMatch = (artistMatch + nameMatch + timeMatch) / 3
        else:
            avgMatch = (artistMatch + nameMatch + timeMatch) / 3
        linksWithMatchValue[result["link"]] = avgMatch

    return linksWithMatchValue


def create_song_title(songName: str, songArtists: List[str]) -> str:
    joined_artists = ", ".join(songArtists)
    return f"{joined_artists} - {songName}"
