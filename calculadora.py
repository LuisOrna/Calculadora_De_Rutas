#Importo primero la clase MAPA, porque tengo elementos de la clase Mapa aqui
from mapa import Mapa

#CLASE CALCULADORA DE RUTAS
class Calculadora_De_Rutas:
    def __init__(self, mapa):
        self.mapa = mapa
        
        self.peso_base = 1
        self.peso_agua = 20
        self.ultimo_camino = None
                
        #Datos para navegacion
        self.conexiones = {}
        self.lista_de_adyacencias = {}
        self._generar_conexiones() #Es un metodo privado, entonces ejecuto de una vez

    def _generar_conexiones(self):
        #Diccionario vacio
        self.conexiones = {}

        #Itero en el mapa
        for fila in range(self.mapa.cantidad_filas):
            for columna in range(self.mapa.cantidad_columnas):
                if fila % 3 == 1 or columna % 3 == 1:
                    self.conexiones[fila, columna] = self.peso_base
    
    #Metodo para agregar obstaculo
    def agregar_obstaculo (self, fila, columna):
        if (fila, columna) in self.conexiones and (fila, columna) != self.mapa.inicio and (fila, columna) != self.mapa.final:
            self.mapa.obstaculos.append((fila, columna))
            return True
        return False

    #Metodo para agregar agua
    def agregar_agua (self, fila, columna):
        if (fila, columna) in self.conexiones and (fila, columna) != self.mapa.inicio and (fila, columna) != self.mapa.final:
            self.mapa.agua.append((fila, columna))
            return True
        return False


    #Metodo para agregar obstaculos y agua
    def _actualizar_conexiones_con_modificadores (self):

        #Genero las conexiones
        self._generar_conexiones()

        #Eliminar Nodos (Obstaculos)
        for obstaculo in self.mapa.obstaculos:
            if obstaculo in self.conexiones:
                del self.conexiones[obstaculo]

        #Agrego el peso del agua
        for agua in self.mapa.agua:
            if agua in self.conexiones:
                self.conexiones[agua] = self.peso_agua

    
    #Metodo para generar lista de adyacencias
    def _generar_lista_adyacencias (self):
        self.lista_de_adyacencias = {}

        #Itero sobre la lista de conexiones
        for nodo in self.conexiones.keys():
            vecinos = []
            fila, columna = nodo #Desarmo la tupla

            #Busco las coordenadas en 4 direcciones
            for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                posible_vecino = (fila + x, columna + y)
                #Ahora verifico si eso existe en conexiones
                if posible_vecino in self.conexiones:
                    peso_vecino = self.conexiones[posible_vecino]
                    vecinos.append((posible_vecino[0], posible_vecino[1], peso_vecino)) #Creo la nueva tupla con peso y la sumo a la lista vecino
            #Agrego a la lista de adyacencia los hayasgos
            self.lista_de_adyacencias[nodo] = vecinos


    #Metodo para calcular la ruta
    def _calcular_ruta(self, inicio, final):
        '''Calculo de la ruta mas corta utilizando una implementacion del algoritmo DIJKSTRA'''
        
        #Se establecen puntos de inicio y final, traidos de la clase MAPA
        self.mapa.inicio = inicio
        self.mapa.final = final

        #Preparo las estructuras
        self._actualizar_conexiones_con_modificadores()
        self._generar_lista_adyacencias()

        #Algoritmo dijkstra
        import heapq #Para la cola de prioridad

        #Creo un diciccionario donde se guardan las distancias
        distancias_acumuladas = {nodo: float("inf") for nodo in self.lista_de_adyacencias.keys()}
        
        #Este puedo definir la primera distancia, siempre sera 0
        distancias_acumuladas[inicio] = 0

        #Creo un diccionario donde se va guardando lo visitado
        visitados = {nodo: False for nodo in self.lista_de_adyacencias.keys()}

        #Creo un diccionario donde estan los nodos Previos que nos llevaron a el
        previos = {nodo: None for nodo in self.lista_de_adyacencias.keys()}

        #Creo la lista de prioridad donde se van guardando los diferentes 
        priority_lista = [] #Aqui voy a guardar una tupla (distancia para llagar a, nodo)
        heapq.heapify(priority_lista) #hago que esta lista este hipifiada
        heapq.heappush(priority_lista, (0, inicio)) #Esta lista va a ordernar en base al primer numero de la tupla (distancia, nodo)

        iteraciones_maximas = 1000
        contador = 0

        #inicio un bucle de ejecucion
        while priority_lista and (contador < iteraciones_maximas): #Esto es True siempre que la lista tenga algun valor
            contador += 1

            #Saco de la lsita de prioridad los primero valores a evaluar
            distancia_actual, nodo_removido = heapq.heappop(priority_lista)
            
            #Creo una condicion de finalizacion en caso de llegar al final
            if nodo_removido == final:
                return previos
                
            #Creo una condicion para que no se repita un nodo ya visto
            if visitados[nodo_removido] == True:
                continue

            else: #Cambio el estado del nodo removido en la lista
                visitados[nodo_removido] = True

            #De esta manera puedo acceder a cada uno de los vecinos que tenga el nodo evaluado
            for fila, columna, peso in self.lista_de_adyacencias[nodo_removido]:
                nodo_observado = (fila, columna)
                distancia = peso  #obtengo la distancia

                #Pero necesito que esa distancia se sume con la distancia del nodo previo
                nueva_distancia = distancia_actual + distancia
                #Entra al diccionario donde estan las distancias infinitas a cada nodo y las modifica
                if nueva_distancia < distancias_acumuladas[nodo_observado]: #solo si la distancia es menor a la distancia actual
                    distancias_acumuladas[nodo_observado] = nueva_distancia #la actualizo

                    #Hago que se actualice el diccionario de Visitados
                    previos[nodo_observado] = nodo_removido # se guarda en el diccionario asi {1: 0 este es nodo de donde vino}
                
                #Lo hago entrar en la priority
                heapq.heappush(priority_lista, (nueva_distancia, nodo_observado))
                
        return previos

    

    #Metodo para reconstruir el camino
    def _reconstruir_camino (self, final, previos_diccionario):
        camino = []
        previo = final
        while previo is not None:
            camino.append(previo)
            previo = previos_diccionario[previo]

        return camino[::-1]
    
    #Metodo para establecer inicio
    def establecer_inicio (self, fila, columna):
        if (fila, columna) in self.conexiones:
            self.mapa.inicio = (fila, columna) #Es de la clase MAPA
            return True
        else:
            return False


    def establecer_final (self, fila, columna):
        if (fila, columna) in self.conexiones and (fila, columna) != self.mapa.inicio:
            self.mapa.final = (fila, columna) #Es de la clase Mapa
            return True
        
        else:
            return False
        
    
    def calcular_y_obtener_ruta(self, inicio, final):
        '''Calcula la ruta y devuelve el camino directamente'''
        previos = self._calcular_ruta(inicio, final)
        return self._reconstruir_camino(final, previos)