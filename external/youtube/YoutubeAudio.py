from external.youtube import AudioProvider

def get_youtube_link(song_name: str, song_artists: str, song_album: str, duration: str):
    youtube_link = AudioProvider.search_and_get_best_match(
        song_name, song_artists, song_album, duration
    )
    if youtube_link is None:
        return None
    else:
        return youtube_link