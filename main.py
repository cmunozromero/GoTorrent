'''
Proxy references by parameter sample.
'''
from pyactor.context import set_context, create_host, sleep, shutdown, serve_forever, interval
from Tracker import *
from Peer import *
from Printer import *


class main(object):
    _tell = ['init_time', 'show_time']

    def init_time(self):
        self.start_time = -1

        self.interval2 = interval(self.host, 1, self.proxy, "show_time")


    def show_time(self):
        self.start_time += 1

        print "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tTIEMPO TRANSCURRIDO: ",self.start_time



if __name__ == "__main__":
    protocolo=0
    while protocolo!=1 and protocolo!=2 and protocolo!=3:
        protocolo=int(input("Que protocolo quieres usar: \n 1.pull \n 2.push \n 3.pull&push "))

    set_context()
    h = create_host()
    tracker = h.spawn('Tracker', Tracker)
    main = h.spawn('main', main)
    main.init_time()

    tracker.tracker_start()

    peers=[]


    # Creamos los peers
    for i in range(1,6,1):
        string = "Peer"+`i`
        peers.append(h.spawn(string, Peer))
        print "Peer",i," iniciado"


    Printer= h.spawn("Printer", Printer)

    for i in range(len(peers)):
        peers[i].start_peer("down", protocolo, 10, "file.txt", tracker, Printer)


    seed= h.spawn("Seed", Peer)
    seed.start_peer("up", protocolo, 10, "file.txt", tracker, None)
    print "Seed iniciado"


    serve_forever()