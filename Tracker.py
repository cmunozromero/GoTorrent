'''
Proxy references by parameter sample.
'''
from pyactor.context import interval
import random


class Tracker(object):
    _tell = ['announce', 'tracker_start', 'actualizar_peers', 'get_peers']
    _ask = ['get_peers']
    _ref = ['announce']

    def __init__(self):
        self.swarms = {}  # enjambres segun nombre torrent

    def tracker_start(self):
        self.interval = interval(self.host, 1, self.proxy, "actualizar_peers")

    def announce(self, torrent_hash, peer_ref):

        if self.swarms.has_key(torrent_hash):
            self.swarms[torrent_hash][peer_ref] = 10  # Ponemos el contador a 10 cuando lo creamos

        else:
            self.swarms[torrent_hash] = {}
            self.swarms[torrent_hash][peer_ref] = 10  # Ponemos el contador a 10 cuando lo creamos

    def get_peers(self, torrent_hash, proxy):

        aux = self.swarms[torrent_hash].keys()

        if proxy in self.swarms[torrent_hash].keys():
            aux.remove(proxy)

        if len(aux) < 3:  # Si hay menos de 3 peers enviamos todos los que hayan
            #print "TRAKER: Proxys que tienen ese fichero menos el que lo pide: ", aux
            proxy.guarda_peers(aux)
        else:  # Sino enviamos 3 peers aleatorios de todos los que hay
            proxy.guarda_peers (random.sample(aux, 3))

    def actualizar_peers(self):
        print "Traker: ",self.swarms
        for torrent_swarm in self.swarms:
            for peers in self.swarms[torrent_swarm].keys():  # Decrementamos los contadores de los peers.
                self.swarms[torrent_swarm][peers] -= 1

                if self.swarms[torrent_swarm][peers] == 0:  # Si el contador llega a cero eliminamos el peer de la lista
                    del self.swarms[torrent_swarm][peers]

            if len(self.swarms[torrent_swarm].keys()) == 0:
                del self.swarms[torrent_swarm]



