from ftptool import FTPHost
import re

def connect(server, username, password):
    host = FTPHost.connect(server, user = username, password = password)

    return host


def FtpSearch( server, username, password, st_id):
    host = connect(server, username, password)
    id = str(st_id)

    choices_tuple = []

    for (dirname, subdirs, files) in host.walk("pub/CDC/observations_germany/climate/"):
        for file in files:
            m = re.finditer(r'.*' + id + '.*', file, re.S)

            if m:
                f = dirname
                choices_tuple.append(f)

    return choices_tuple

def main(stationId):
    server = "ftp-cdc.dwd.de"
    username = 'anonymous'
    password = 'example@example.de'
    st_id= int(stationId)
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    t5 = []
    s = FtpSearch(server, username, password,st_id )


    for c in s:
        r = re.split('climate/',c)[-1]


        if  r.startswith('10_minutes'):
             d = r.split('/')
             t1.append(d[1])

        elif r.startswith('1_minute'):
            d = r.split('/')
            t2.append(d[1])

        elif r.startswith('daily'):
            d = r.split('/')
            t3.append(d[1])

        elif r.startswith('hourly'):
            d = r.split('/')
            t4.append(d[1])

        elif r.startswith('monthly'):
            d = r.split('/')
            t5.append(d[1])



    f1 = list(dict.fromkeys(t1))
    f2 = list(dict.fromkeys(t2))
    f3 = list(dict.fromkeys(t3))
    f4 = list(dict.fromkeys(t4))
    f5 = list(dict.fromkeys(t5))

    dic = {
        "stationId": st_id,
        "capabilities": [
            {
                "resolution": "10_minutes",
                "observationTypes": f1
            },
            {
                "resolution": "1_minute",
                "observationTypes": f2

            },
            {
                "resolution": "daily",
                "observationTypes": f3
            },
            {
                "resolution": "hourly",
                "observationTypes": f4
            },
            {
                "resolution": "monthly",
                "observationTypes": f5
            }
        ]
    }

    return(dic)

