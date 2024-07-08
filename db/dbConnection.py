from flask import current_app, g
import pymongo

# return a client.
def connect_mongo():
    """
    Returns:
        MongoDB client
    """
    app = current_app._get_current_object()
    if 'db' not in g:
        g.db = pymongo.MongoClient("mongodb+srv://MusMixAdmin1:uGpw6A07tp2kbTP7@musmix.bb1xivw.mongodb.net/",
                                    username = "MusMixAdmin1", password = "uGpw6A07tp2kbTP7").get_database("musmixdata")
    return g.db

