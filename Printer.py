
import matplotlib.pyplot
from pyactor.context import interval

class Printer(object):
    _tell = ['actualizaGrafico', 'setValues', 'start']
    _ref= ['start', 'setValues']

    def __init__(self):

        self.lista = {}

    def start(self, proxy):
        self.interval= interval(self.host, 2, self.proxy, "actualizaGrafico")
        self.lista[proxy] = []

    def setValues(self, valor, proxy):

        print proxy.getid(),": Anadiendo valor --> ",valor
        self.lista[proxy].append(valor)

    def actualizaGrafico(self):

        for i in self.lista.keys():

            for x in self.lista[i]:
                if x==100.0:
                    print "..............................................GENERANDO GRAFICAS............................................................."
                    string = i.getid()
                    matplotlib.pyplot.plot(self.lista[i])
                    matplotlib.pyplot.title("Grafica Descarga de " + string)
                    matplotlib.pyplot.ylabel("Porcentaje (%)")
                    matplotlib.pyplot.xlabel("tiempo")
                    matplotlib.pyplot.savefig(string + '.png')
                    matplotlib.pyplot.close()

                    del self.lista[i]


