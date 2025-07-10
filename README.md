# 🗺️ Calculadora de Rutas

Un sistema de pathfinding que encuentra la ruta más corta entre dos puntos en un mapa de ciudad con obstáculos y diferentes tipos de terreno.

## 📋 Descripción del Proyecto

Este proyecto implementa un algoritmo de búsqueda de rutas (Dijkstra) en un mapa de ciudad con calles, edificios, obstáculos y zonas de agua. El usuario puede configurar puntos de inicio y destino, añadir modificadores al terreno y visualizar la ruta óptima calculada.

## 🏗️ Arquitectura y Responsabilidades

### División de Responsabilidades

El proyecto se estructura en **dos clases principales** con responsabilidades claramente definidas:

#### 🎨 Clase Mapa (`mapa.py`)
**Responsabilidad: Visualización y Representación**
- **Creación del entorno visual**: Genera la matriz que representa la ciudad
- **Gestión de elementos gráficos**: Maneja los caracteres emoji para cada tipo de terreno
- **Renderizado**: Se encarga de mostrar el mapa en pantalla
- **Aplicación de modificadores visuales**: Coloca agua, obstáculos, inicio, final y camino en la matriz

#### 🧭 Clase Calculadora_De_Rutas (`calculadora.py`)
**Responsabilidad: Navegación y Lógica de Rutas**
- **Generación de conexiones**: Crea la red de nodos navegables (calles)
- **Implementación del algoritmo Dijkstra**: Calcula la ruta más corta
- **Gestión de modificadores**: Maneja obstáculos y diferentes pesos de terreno
- **Validación de movimientos**: Verifica que las posiciones sean válidas

Esta separación permite que cada clase se enfoque en una única responsabilidad, siguiendo el principio de **Single Responsibility** de la programación orientada a objetos.

## 🔄 Proceso de Refactorización

### Lo que Aprendí

**Ventajas de las Clases:**
- **Agrupación consistente**: Las clases permiten mantener datos y métodos relacionados juntos de forma lógica
- **Escalabilidad**: Facilita agregar nuevas funcionalidades sin afectar el código existente
- **Estructura más clara**: El proyecto con clases es más fácil de entender a nivel arquitectónico
- **Crecimiento sostenible**: Proporciona una base sólida para futuras expansiones del proyecto

**Mejoras en Organización:**
- El código está más organizado y es más fácil de mantener
- Cada clase tiene un propósito específico y bien definido
- La separación hace que los errores sean más fáciles de localizar y corregir

### Decisiones de Diseño

**Métodos Privados:**
Implementé múltiples métodos privados (con `_`) que simplifican la interfaz pública:
```python
# Ejemplos de métodos privados
_crear_mapa_vacio()
_generar_conexiones()
_actualizar_conexiones_con_modificadores()
_reconstruir_camino()
```

**Beneficios:**
- **Main simplificado**: Los métodos públicos en el main son más claros y concisos
- **Encapsulación**: La lógica compleja está oculta y protegida
- **Interfaz limpia**: Solo se exponen los métodos que realmente necesita el usuario

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.7 o superior

### Estructura de Archivos
```
📁 proyecto/
├── 📄 mapa.py           # Clase Mapa
├── 📄 calculadora.py    # Clase Calculadora_De_Rutas  
├── 📄 main.py           # Programa principal
└── 📄 README.md         # Este archivo
```

### Ejecución
```bash
python main.py
```

### Instrucciones de Uso
1. **Configurar dimensiones**: Ingresa el tamaño del mapa (1-99 filas y columnas)
2. **Establecer puntos**: Define coordenadas de inicio y destino en formato `fila,columna`
3. **Añadir modificadores** (opcional):
   - **Obstáculos**: Bloquean completamente el paso
   - **Agua**: Incrementa significativamente el costo de movimiento
4. **Visualizar resultado**: El programa muestra la ruta óptima calculada

## 🧠 Algoritmo Dijkstra

### Implementación

El proyecto utiliza una implementación personalizada del **algoritmo de Dijkstra** para encontrar la ruta más corta:

```python
def _calcular_ruta(self, inicio, final):
    # Inicialización de estructuras
    distancias_acumuladas = {nodo: float("inf") for nodo in self.lista_de_adyacencias.keys()}
    distancias_acumuladas[inicio] = 0
    
    # Cola de prioridad para nodos por explorar
    priority_lista = [(0, inicio)]
    
    # Algoritmo principal
    while priority_lista:
        distancia_actual, nodo_actual = heapq.heappop(priority_lista)
        # ... lógica de exploración de vecinos
```

### Funcionamiento

1. **Inicialización**: Todas las distancias se establecen como infinitas, excepto el nodo inicial (0)
2. **Cola de prioridad**: Se usa `heapq` para siempre procesar el nodo con menor distancia acumulada
3. **Exploración de vecinos**: Para cada nodo, se calculan las distancias a sus vecinos
4. **Actualización**: Si se encuentra un camino más corto, se actualiza la distancia y el nodo previo
5. **Reconstrucción**: Al llegar al destino, se reconstruye el camino siguiendo los nodos previos

### Complejidad
- **Temporal**: O((V + E) log V) donde V = vértices, E = aristas
- **Espacial**: O(V) para almacenar distancias y nodos previos

## 🏙️ Lógica del Mapa

### Creación de la Ciudad

El mapa se genera con un **patrón de cuadrícula urbana**:

```python
def _crear_mapa_vacio(self):
    # Matriz inicial llena de edificios
    mapa = [[self.caracteres['edificio'] for _ in range(self.cantidad_columnas)] 
            for _ in range(self.cantidad_filas)]
    
    # Creación de calles cada 3 posiciones
    for fila in range(self.cantidad_filas):
        for columna in range(self.cantidad_columnas):
            if fila % 3 == 1 or columna % 3 == 1:
                mapa[fila][columna] = self.caracteres['calle']
    return mapa
```

### Elementos del Terreno

| Elemento | Símbolo | Peso | Descripción |
|----------|---------|------|-------------|
| Calle | ⬜ | 1 | Terreno navegable estándar |
| Edificio | 🏢 | ∞ | No navegable |
| Agua | 💧 | 20 | Navegable con alto costo |
| Obstáculo | 🚫 | ∞ | Bloqueo temporal del usuario |
| Camino | 🟢 | - | Ruta calculada (visual) |
| Inicio | 🚶 | - | Punto de partida |
| Final | 🏁 | - | Punto de destino |

### Sistema de Pesos

- **Calles normales**: Peso 1 (movimiento estándar)
- **Agua**: Peso 20 (simula dificultad de movimiento)
- **Obstáculos**: Eliminados del grafo (imposibles de atravesar)

El algoritmo siempre buscará minimizar el costo total del recorrido, prefiriendo calles normales sobre agua cuando sea posible.

## 🔮 Posibles Mejoras Futuras

- Implementar diferentes algoritmos de pathfinding (A*, BFS)
- Añadir más tipos de terreno con diferentes costos
- Interfaz gráfica con pygame o tkinter
- Guardar/cargar mapas desde archivos
- Animación del proceso de búsqueda de rutas

---

*Proyecto desarrollado como parte del aprendizaje de programación orientada a objetos y algoritmos de grafos.*
