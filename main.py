from mapa import Mapa
from calculadora import Calculadora_De_Rutas

def main ():
    #MOSTRAR título del programa
    print("CALCULADORA DE RUTAS")
    print("=" * 30)

    print("Configuremos el Mapa")
    
    #PEDIR al usuario filas y columnas
    while True:
        try:
            numero_filas = int(input("Ingrese el numero de Filas: "))
            numero_columnas = int(input("Ingrese numero de columnas: "))
            if 0 < numero_filas < 100 and 0 < numero_columnas < 100:
                print(f"valores de filas {numero_filas} y columnas {numero_columnas} configurado")
                break
            else:
                print("Ingrese numeros entre 1 y 99")
        except ValueError:
            print("Por favor ingrese numeros")

    # CREAR objetos mapa y calculadora
    mapa = Mapa(numero_filas, numero_columnas)
    calculadora = Calculadora_De_Rutas(mapa)
    
    #Muestro el Mapa creado
    print(f'\n mapa de {numero_filas}x{numero_columnas} creado')
    mapa.imprimir_mapa()


    #Usuario agrega inicio y fin
    #Inicio
    print('Agreguemos ahora punto de inicio y punto final')
    while True:
        try:
            inicio = input("Ingrese las coordenadas de inicio (fila, columna): ")
            fila_inicio, columna_inicio = map(int, inicio.split(','))

            if calculadora.establecer_inicio(fila_inicio, columna_inicio):
                print("Inicio Establecido")
                break
            else:
                print('Coordenadas invalidas, debe ser una calle')
        except ValueError:
            print("Coordenadas invalidas, utilice el formato (filas, columnas)")
    #Final
    while True:
        try:
            final = input("Ingrese las coordenadas de final (fila, columna): ")
            fila_final, columna_final = map(int, final.split(','))

            if calculadora.establecer_final(fila_final, columna_final):
                print('Final Establecido')
                break
            else:
                print('Coordenadas invalidas, debe ser una calle y debe ser un punto diferente al inicio')
        except ValueError:
            print("Coordenadas invalidas, utilice el formato (filas, columnas)")

    
    # Se muestra mapa con ruta inicio fin
    inicio = (fila_inicio, columna_inicio)
    final = (fila_final, columna_final)
    camino = calculadora.calcular_y_obtener_ruta(inicio, final) #lo obtengo desde la calculadora

    if camino:
        mapa.matriz = mapa._crear_mapa_vacio()
        mapa.marcar_camino(inicio, final, camino)
        mapa.aplicar_todos_elementos()

        print('\nMapa con ruta')
        mapa.imprimir_mapa()
    else:
        print('No se pudo encontrar la ruta')

    

    # Usuario decide si agregar obstáculos, agua
    print("\n🚧 ¿Desea agregar modificadores al mapa?")

    # Obstáculos
    respuesta = input("¿Agregar obstáculos? (s/n): ").lower()
    if respuesta == 's':
        print("🚫 Ingrese obstáculos (escriba 'f' cuando termine)")
        while True:
            entrada = input("Coordenadas del obstáculo (fila,columna): ")
            if entrada.lower() == 'f':
                break
            
            try:
                fila, columna = map(int, entrada.split(','))
                if calculadora.agregar_obstaculo(fila, columna):
                    print(f"✅ Obstáculo agregado en ({fila},{columna})")
                else:
                    print("❌ Coordenadas inválidas")
            except ValueError:
                print("❌ Formato inválido. Use: fila,columna")

    # Agua  
    respuesta = input("¿Agregar agua? (s/n): ").lower()
    if respuesta == 's':
        print("💧 Ingrese agua (escriba 'f' cuando termine)")
        while True:
            entrada = input("Coordenadas del agua (fila,columna): ")
            if entrada.lower() == 'f':
                break
            
            try:
                fila, columna = map(int, entrada.split(','))
                if calculadora.agregar_agua(fila, columna):
                    print(f"✅ Agua agregada en ({fila},{columna})")
                else:
                    print("❌ Coordenadas inválidas")
            except ValueError:
                print("❌ Formato inválido. Use: fila,columna")

    
    # Se muestra mapa con ruta actualizada
    print("\n🧭 Recalculando ruta con modificadores...")

    camino_actualizado = calculadora.calcular_y_obtener_ruta(inicio, final)

    if camino_actualizado:
        print("✅ Nueva ruta encontrada!")
        
        # Limpiar mapa y aplicar todos los elementos
        mapa.matriz = mapa._crear_mapa_vacio()
        mapa.marcar_camino(inicio, final, camino_actualizado)
        mapa.aplicar_todos_elementos()
        print(f"\n🗺️ Mapa final con ruta actualizada:")
        mapa.imprimir_mapa()
            
    else:
        print("❌ ¡No se pudo encontrar una ruta! Los obstáculos bloquean el camino.")
        print("🗺️ Mapa final (sin ruta posible):")
        mapa.matriz = mapa._crear_mapa_vacio()
        mapa.aplicar_todos_elementos()
        mapa.imprimir_mapa()

main()
