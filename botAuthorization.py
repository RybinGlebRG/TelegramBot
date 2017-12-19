import dbInteraction
import os


def getToken():
    conn=dbInteraction.DBInteraction()
    res=conn.query('select token from tokens')
    return  os.environ['TOKEN']
    return res[0][0]