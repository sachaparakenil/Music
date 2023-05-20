# from models.dbconn import Session
from service.JsonResponse import JsonResponse
from external.spotify.Tracks import spotifyTrack
from external.youtube.YoutubeAudio import get_youtube_link

def GetTrack(id):
    response = JsonResponse()
    try:
        result = spotifyTrack(id)
        spotify_id = result["id"]
        spotify_name = result["name"]
        spotify_artists = []
        for artist in result["artists"]:
            spotify_artists.append(artist["name"])
        spotify_album = result["album"]["name"]
        spotify_img = result["album"]["images"][0]["url"]
        duration = round(result["duration_ms"] / 1000, ndigits=3)
        displayName = spotify_name + " - " + ", ".join(spotify_artists)
        
        youtube_link = get_youtube_link(spotify_name, spotify_artists, spotify_album, duration)
        if youtube_link != None:
            data = youtube_link
            response.set_data(data)
            response.set_status(200)
        else:
            response.set_status(400)
            response.set_message("Bad Request")
            response.set_error("Bad Request")
            return response.returnResponse()

    except Exception as e:
        response.set_status(500)  # Internal error
        response.set_message("Internal Server Error")
        response.set_error("Error in  fetching a content => " + str(e))
        # logConfig.logError("Error in  fetching a content  => " + str(e))
    finally:
        # session.close()
        return response.returnResponse()