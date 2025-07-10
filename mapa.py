#CLASE MAPA
class Mapa:
    def __init__(self, cantidad_filas, cantidad_columnas):
        self.cantidad_filas = cantidad_filas
        self.cantidad_columnas = cantidad_columnas


        #Encapsulo los caracteres para representar los diferente elementos
        self.caracteres = {
            'calle': '⬜',
            'edificio': '🏢', 
            'agua': '💧',
            'zona_bloqueada': '🚫',
            'camino': '🟢',
            'inicio': '🚶',
            'final': '🏁'
        }

        #Elementos adicionales
        self.inicio = None
        self.final = None
        self.obstaculos = []
        self.agua = []

        #Matriz visual
        self.matriz = self._crear_mapa_vacio()


    def _crear_mapa_vacio(self):

        #Esta es una matriz llena de edificios
        mapa = [[self.caracteres['edificio'] for _ in range(self.cantidad_columnas)] for _ in range(self.cantidad_filas)]

        #ahora se agregan las calles
        for fila in range(self. cantidad_filas):
            for columna in range(self. cantidad_columnas):
                if fila % 3 == 1 or columna % 3 == 1:
                    mapa[fila][columna] = self.caracteres['calle']
        return mapa 
    
    #Ahora el metodo para imprimir el mapa
    def imprimir_mapa(self):
        '''hace que se pueda imprimie el mapa en pantalla'''
        for fila in self.matriz:
            print(' '.join(fila))

    '''def obtener_dimensiones(self):

        return self.cantidad_filas, self.cantidad_columnas'''
    
    #Metodo para agregar agua
    def _agregar_agua_matriz (self):
        for agua_fila, agua_columna in self.agua:
            self.matriz[agua_fila][agua_columna] = self.caracteres['agua']
        

    #Metodo para agregar obstaculo
    def _agregar_obstaculo_matriz (self):
        for obstaculo_fila, obstaculo_columna in self.obstaculos:
            self.matriz[obstaculo_fila][obstaculo_columna] = self.caracteres['zona_bloqueada']

    #Metodo para agregar inicio
    def agregar_inicio_final (self, inicio, final):
        self.matriz[inicio[0]][inicio[1]] = self.caracteres['inicio']
        self.matriz[final[0]][final[1]] = self.caracteres['final']


    #Metodo para marcar el camino
    def marcar_camino (self, inicio, final, camino):
        # Verificar si el camino realmente conecta inicio con final
        if not camino or camino[0] != inicio or camino[-1] != final:
            print("no se pudo llegar al destino")
            return 
        
        if camino:
            for fila, columna in camino:
                self.matriz[fila][columna] = self.caracteres['camino']

    #Metodo para unificar cambios
    def aplicar_todos_elementos(self):
        self._agregar_agua_matriz()
        self._agregar_obstaculo_matriz()
        if self.inicio and self.final:
            self.agregar_inicio_final(self.inicio, self.final)
