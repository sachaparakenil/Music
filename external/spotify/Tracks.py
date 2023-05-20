from models.spotifyconn import sp

def spotifyTrack(id):
    result = sp.track(track_id=id)
    return result