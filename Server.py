import json
import os
from datetime import datetime, time
import cherrypy
from Dane import update
import socket

jsono = None


def getFile():
    update()
    with open(os.path.realpath(os.path.dirname(__file__))+"\data.json", "r") as f:
        jsonstr = f.read()
        f.close()
    global jsono
    jsono = json.loads(jsonstr)
    print("Updated file")


def whichLesson():
    check_time = datetime.now().time()
    times = [(time(8, 0), time(8, 45)), (time(8, 55), time(9, 40)), (time(9, 50), time(10, 35)), (time(10, 45), time(11, 30)), (time(11, 40), time(12, 25)), (time(12, 30), time(13, 15)), (time(13, 45), time(14, 30)), (time(14, 35), time(15, 20)), (time(15, 30), time(16, 15)), (time(16, 25), time(17, 10)), (time(17, 20), time(18, 5))]

    for i, (begin_time, end_time) in enumerate(times):
        if begin_time <= end_time:
            if begin_time <= check_time <= end_time:
                return i
        else:
            if check_time >= begin_time or check_time <= end_time:
                return i
    return -1


def getSala(klasa, nauczyciel, sala, czas, day2):
    send = []
    les = whichLesson()+1
    if czas != "-1":
        les = int(czas)
    if 0 < les:
        now = datetime.now()
        day = now.weekday()
        if day2 != "-1":
            day = int(day2)-1
        if day < 5:
            for i in jsono:
                try:
                    ob = {}
                    if klasa in jsono[i][day][str(les)][1] and klasa != "None":
                        ob["nauczyciel"] = jsono[i][day][str(les)][0][0]
                        ob["klasa"] = jsono[i][day][str(les)][1]
                        ob["sala"] = i
                        send.append(ob)
                        continue
                    if nauczyciel in jsono[i][day][str(les)][0][0] or nauczyciel in jsono[i][day][str(les)][0][1] and nauczyciel != "None":
                        ob["nauczyciel"] = jsono[i][day][str(les)][0][0]
                        ob["klasa"] = jsono[i][day][str(les)][1]
                        ob["sala"] = i
                        send.append(ob)
                        continue
                    if sala in i and sala != "None":
                        ob["nauczyciel"] = jsono[i][day][str(les)][0][0]
                        ob["klasa"] = jsono[i][day][str(les)][1]
                        ob["sala"] = i
                        send.append(ob)
                        break
                except:
                    pass
        return send
    else:
        return "Break"


def getWolne(czas, day2):
    send = []
    les = whichLesson()+1
    if czas != "-1":
        les = int(czas)
    if 0 < les:
        now = datetime.now()
        day = now.weekday()
        if day2 != "-1":
            day = int(day2)-1
        if day < 5:
            for i in jsono:
                try:
                    if jsono[i][day][str(les)] is None:
                        send.append(i)
                except:
                    send.append(i)
        return send
    else:
        return "Break"

def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        ip_address = sock.getsockname()[0]
        return ip_address
    except socket.error:
        return None
    finally:
        sock.close()


class Returner(object):
    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def index(self, klasa="None", nauczyciel="None", sala="None", czas="-1", day="-1"):
        try:
            return getSala(klasa, nauczyciel, sala, czas, day)
        except:
            raise cherrypy.HTTPError(400, "One of the variables is wrong. Check again documentation for more information.")

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def wolne(self, czas="-1", day="-1"):
        try:
            return getWolne(czas, day)
        except:
            raise cherrypy.HTTPError(400, "One of the variables is wrong. Check again documentation for more information.")

    @cherrypy.expose
    def update(self):
        getFile()
    

if __name__ == '__main__':
    getFile()
    cherrypy.config.update({'server.socket_host': get_ip_address()})
    cherrypy.quickstart(Returner())
