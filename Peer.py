'''
Remote example spawning on a remote server. CLIENT
@author: Daniel Barcelona Pons
'''
from pyactor.context import interval
import random



class Peer(object):
    _tell = ['push', 'announce', 'ann_start', 'start_peer', 'get_peers', 'push', 'pull_start', 'pull', 'load_file','guarda_peers','push_start', 'guarda_fichero','envia_progreso']
    _ask= ['getid']
    _ref = ['start_peer', 'announce', 'get_peers']

    def __init__(self):

        self.chunks = {}
        self.peers = []

    def getid(self):
        return self.id

    def start_peer(self, operacion, protocolo, longitud_archivo, fileX, tracker, printer):

        self.torrenthash = fileX

        self.long_archivo = longitud_archivo

        self.tracker = tracker


        self.interval1 = interval(self.host, 1, self.proxy, "announce")

        if operacion == "up":  # UPLOAD

            self.printer = printer

            self.chunks_restantes = None

            self.cargar_fichero(fileX)

            self.interval2 = interval(self.host, 2, self.proxy, "get_peers")




        else:  # DOWNLOAD

            self.printer = printer

            self.printer.start(self.proxy) #iniciamos el printer con nuestro proxy

            self.chunks_restantes = list(xrange(longitud_archivo))

            self.interval2 = interval(self.host, 2, self.proxy, "get_peers")

            # Inicia el proceso para la grafica
            self.progreso = interval(self.host, 1, self.proxy, "envia_progreso")



        if protocolo==1 or protocolo==3:
            # Inicia el processo pull para descargar
            self.proceso_pull = interval(self.host, 1, self.proxy, "pull_start")
        if protocolo==2 or protocolo==3:
            # Inicia el processo push para compartir
            self.proceso_push= interval(self.host, 1, self.proxy, "push_start")




    # Compartir fichero

    def announce(self):
        self.tracker.announce(self.torrenthash, self.proxy)

    # Descaragr fichero

    def get_peers(self):
        self.tracker.get_peers(self.torrenthash, self.proxy)

    def guarda_peers(self, peers):
        self.peers = peers


    # Metodo para enviar los chunks que tengo a mis vecinos
    def push_start(self):
        if self.chunks and self.peers:
            chunk = random.choice(self.chunks.keys())
            #print self.id,": Compartiendo el trozo numero: ", chunk
            for peer in self.peers:
                peer.push(chunk, self.chunks[chunk])


    def push(self, id_chunk, data):
        if id_chunk not in self.chunks:
            self.chunks[id_chunk] = data
            print self.id,": CHUNKS RECIVIDOS: ",self.chunks
            self.chunks_restantes.remove(id_chunk)

            if len(self.chunks) == self.long_archivo:  # Si tenemos todas las partes del fichero paramos el proceso de pedir chunks
                self.guarda_fichero()


    # Metodo para pedir los chunks que me faltan a mis vecinos
    def pull_start(self):
        if self.chunks_restantes and self.peers:
            chunk = random.choice(self.chunks_restantes)  # numero chunk aleatorio
            #print self.id,": Pidiendo trozo numero ", chunk
            for peer in self.peers:
                peer.pull(chunk, self.proxy)  # hacemos un pull a cada peer del enjambre


    def pull(self, id_chunk, sender):
        if id_chunk in self.chunks.keys():
            #print self.id,": Enviando el trozo ", id_chunk, " a ", sender
            sender.push(id_chunk, self.chunks[id_chunk])

    def cargar_fichero(self, file1):
        f = open(file1)
        l = list(f.read())
        self.chunks= {}

        for i in range(len(l)):
            self.chunks[i]=l[i]

        self.missing_chunks = []

    def guarda_fichero(self):

        filename= "out"+self.id+".txt"
        f = open(filename, 'w')
        for i in list(self.chunks.values()):
            f.write(""+i)

        f.close()

    def envia_progreso(self):

        self.porcentaje= float(len(self.chunks.values()))/float(self.long_archivo)
        self.printer.setValues(self.porcentaje * 100, self.proxy)

        if self.porcentaje==1.0:
            self.progreso.set()
        #print self.id,": Procentaje de descarga: ", self.porcentaje, self.printer






