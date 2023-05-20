from models.spotifyconn import sp

def spotifySearch(query, type, market):
    result = sp.search(q=query)
    return result