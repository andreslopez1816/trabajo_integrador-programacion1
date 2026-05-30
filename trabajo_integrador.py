# =====================================================================
# Global
# =====================================================================

import csv
import time
lista_paises = []  # Lista global para almacenar los países en memoria durante la ejecución# Lista global para almacenar los países en memoria durante la ejecución

def volviendo_al_menu():
    print('\nPulse una tecla para continuar')
    input()
    print('Volviendo al menú principal...')
    time.sleep(1)

def cargar_datos_csv(ruta_archivo: str) -> list:

    try:
        # Abrimos el archivo en modo lectura ('r') con codificación utf-8 por los acentos
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            # csv.DictReader usa la primera línea (header) como las claves del diccionario
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    # Limpiamos los espacios en blanco de las claves y valores (.strip())
                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"].strip()),
                        "superficie": int(fila["superficie"].strip()),
                        "continente": fila["continente"].strip()
                    }
                    lista_paises.append(pais)

                except (ValueError, KeyError):
                    # Si falla el int() o falta una columna en esa fila, salta este error
                    print(f"[Aviso] Error de formato en la fila: {fila}. Se omitió este registro.")

    except FileNotFoundError:
        print(f"[Error] No se encontró el archivo en la ruta: '{ruta_archivo}'.")
    except Exception as e:
        print(f"[Error] Ocurrió un fallo inesperado al leer el archivo: {e}")

    return lista_paises
 
# =====================================================================
# 1. Cargar un país manualmente por Consola
# =====================================================================
  
def cargar_desde_consola(lista_paises: list) -> None:  
    
    print("\n--- Carga Pais Manual por Consola ---\n")

    nombre = input("Ingrese el nombre del país: ").strip().title()
    if not nombre:
        print("[Error] El nombre no puede estar vacío.") 
        return

    # 2. Validar Población (Debe ser un entero positivo) 
    try:
        poblacion = int(input("Ingrese la población (solo números enteros): "))
        if poblacion < 0:
            print("[Error] La población no puede ser negativa.") 
            return
    except ValueError:
        print("[Error] Formato inválido. Debe ingresar un número entero.") 
        return

    # 3. Validar Superficie (Debe ser un entero positivo) 
    try:
        superficie = int(input("Ingrese la superficie en km² (solo números enteros): "))
        if superficie < 0:
            print("[Error] La superficie no puede ser negativa.") 
            return
    except ValueError:
        print("[Error] Formato inválido. Debe ingresar un número entero.") 
        return

    # 4. Validar Continente (No vacío) 
    continente_menu =   {1: "África",
                         2: "América",
                         3: "Asia",
                         4: "Europa",
                         5: "Oceanía",
                         6: "Antártida"}

    print()

    for clave, (descripcion) in continente_menu.items():
        print(f'{clave} - {descripcion}')
    
    print()      
    
    try:
        continente_opcion = int(input("Ingrese el número del continente: ").strip())
    except ValueError:
        print("[Error] Debe ingresar un número entero.")
        return

    if continente_opcion not in continente_menu:
        print("[Error] No es una opción válida.")
        return

    continente = continente_menu[continente_opcion]

    # Si todo está OK, armamos el diccionario y lo añadimos a la lista 1
    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    lista_paises.append(nuevo_pais)
    print(  f"\n¡Éxito! Pais cargado correctamente.\n"
            f"'Nombre del pais: {nombre}'\n" 
            f"'La población es: {poblacion}'\n" 
            f"'La superficie es: {superficie} km²'\n" 
            f"'El continente es: {continente}'") 

    volviendo_al_menu()

# =====================================================================
# 2. Actualizar población / superficie
# =====================================================================

def actualizar_pais(lista_paises: list) -> None:

    print("\n--- Actualizar Datos de País ---\n")

    #Verificación rápida de datos cargados
    if not lista_paises:
        print("[Aviso] No hay países cargados. Use la opción 1 primero.")
        return
    
    print("Los paises disponibles son: ")
    for idx, pais2 in enumerate(lista_paises): 
        print(f"{idx + 1} - {pais2["nombre"]}")

    busqueda = input("Ingrese el nombre del país a modificar: ").strip()

    #Buscamos el país
    for pais in lista_paises:
        if pais["nombre"].lower() == busqueda.lower():
            print(f"\nPaís encontrado: {pais['nombre']}")
            print(f"Población actual: {pais['poblacion']} | Superficie actual: {pais['superficie']} km²")

    #Pregunta directa
            que_cambiar = input("¿Qué desea modificar? (poblacion / superficie / ambos): ").strip().lower()

            try:
                if que_cambiar == "poblacion" or que_cambiar == "ambos":
                    pais["poblacion"] = int(input("Ingrese nueva población: "))

                if que_cambiar == "superficie" or que_cambiar == "ambos":
                    pais["superficie"] = int(input("Ingrese nueva superficie en km²: "))

                if que_cambiar not in ["poblacion", "superficie", "ambos"]:
                    print("[Error] Opción no válida. No se hicieron cambios.")
                    return
                
                if pais["superficie"] < 0 or pais["poblacion"]< 0:
                    print("[Error] La superficie o la población no pueden ser negativas.") 
                    return
                               
                print(f"\n[Éxito] ¡Datos de {pais['nombre']} actualizados!")
                volviendo_al_menu() 
                return # Terminamos la función con éxito

            except ValueError:
                print("[Error] Debe ingresar solo números enteros. Cambios cancelados.")
                return

    # Si terminó el bucle y no entró al "if", es porque no lo encontró
    print(f"[Aviso] No se encontró el país '{busqueda}'.")

    volviendo_al_menu()

# =====================================================================
# 3. Buscar país por nombre
# =====================================================================

def buscar_pais_nombre(lista_paises: list) -> None:

    if not lista_paises:
        print("[Aviso] No hay países cargados. Use la opción 1 primero.")
        return

    print("\n--- Buscar países ---\n")

    busqueda = input("Ingrese el nombre del país que quiere buscar: ").strip().lower()

    encontrado = False

    for pais in lista_paises:
        if busqueda in pais["nombre"].lower():
            print(
                f"\nPais encontrado!\n"
                f"Nombre del pais: {pais['nombre']}\n"
                f"La población es: {pais['poblacion']}\n"
                f"La superficie es: {pais['superficie']} km²\n"
                f"El continente es: {pais['continente']}"
            )
            encontrado = True

    if not encontrado:
        print(f"[Aviso] No se encontró el país '{busqueda}'.")

    volviendo_al_menu()
         
# =====================================================================
# 4. Filtrar paises
# =====================================================================

def filtrar_paises(lista_paises: list) -> None:
    
    print("\n--- Filtrar países ---\n")

    #Validamos primero si hay datos en el sistema
    if not lista_paises:
        print("[Aviso] No hay países cargados. Use la opción 1 primero.")
        return

    print(  "Criterios de filtrado disponibles:\n"
            "1. Por Continente\n"
            "2. Por Rango de Población\n"
            "3. Por Rango de Superficie\n")

    opcion = input("Seleccione una opción (1-3): ").strip()

    #Esta lista va a guardar los países que cumplan con el filtro
    resultados = []

    # OPCIÓN 1: FILTRAR POR CONTINENTE

    if opcion == "1":
        continente_buscado = input("Ingrese el continente a filtrar: ").strip().lower()

        for pais in lista_paises:
            if pais["continente"].lower() == continente_buscado:
                resultados.append(pais)
    
    #OPCIÓN 2: FILTRAR POR RANGO DE POBLACIÓN
    elif opcion == "2":
        try:
            min_pob = int(input("Ingrese el mínimo de población: "))
            max_pob = int(input("Ingrese el máximo de población: "))

            for pais in lista_paises:
                # Verificamos si la población está dentro del rango inclusivo
                if min_pob <= pais["poblacion"] <= max_pob:
                    resultados.append(pais)
        except ValueError:
            print("[Error] Debe ingresar números enteros para los rangos.")
            return

    # OPCIÓN 3: FILTRAR POR RANGO DE SUPERFICIE
    elif opcion == "3":
        try:
            min_sup = int(input("Ingrese la superficie mínima (km²): "))
            max_sup = int(input("Ingrese la superficie máxima (km²): "))

            for pais in lista_paises:
                # Verificamos si la superficie está dentro del rango inclusivo
                if min_sup <= pais["superficie"] <= max_sup:
                    resultados.append(pais)
        except ValueError:
            print("[Error] Debe ingresar números enteros para los rangos.")
            return
    else:
        print("[Error] Opción inválida. Volviendo al menú principal.")
        return

    # MOSTRAR RESULTADOS
    if resultados:
        print(f"\n--- Se encontraron {len(resultados)} países ---")
        for pais in resultados:
            print(f"País: {pais['nombre']} | Continente: {pais['continente']} | Población: {pais['poblacion']} | Superficie: {pais['superficie']} km²")
    else:
        print("\n[Aviso] No se encontraron países que cumplan con el criterio ingresado.")

    volviendo_al_menu()

# =====================================================================
# 5. Ordenar paises
# =====================================================================

def ordenar_paises(lista_paises: list) -> None:

    if not lista_paises:
        print("[Aviso] No hay países cargados. Use la opción 1 primero.")
        return

    print("\n--- Ordenar Países ---\n")

    print(
        "1. Nombre\n"
        "2. Población\n"
        "3. Superficie\n"
    )

    opcion = input("Seleccione criterio: ").strip()

    orden = input("Ascendente (A) o Descendente (D): ").strip().lower()

    if orden not in ["a", "d"]:
        print("[Error] Debe ingresar A o D.")
        return

    descendente = (orden == "d")

    if opcion == "1":
        lista_paises.sort(
            key=lambda pais: pais["nombre"],
            reverse=descendente
        )

    elif opcion == "2":
        lista_paises.sort(
            key=lambda pais: pais["poblacion"],
            reverse=descendente
        )

    elif opcion == "3":
        lista_paises.sort(
            key=lambda pais: pais["superficie"],
            reverse=descendente
        )

    else:
        print("[Error] Opción inválida.")
        return

    print("\n--- Países ordenados ---\n")

    for pais in lista_paises:
        print(
            f"{pais['nombre']} | "
            f"Población: {pais['poblacion']} | "
            f"Superficie: {pais['superficie']} km² | "
            f"Continente: {pais['continente']}"
        )

    volviendo_al_menu()

# =====================================================================
# 6. Mostrar estadísticas generales
# =====================================================================

def mostrar_estadisticas(lista_paises: list) -> None:

    """Calcula y muestra:

    País con mayor y menor población.
    
    Promedio de población y superficie.
    
    Cantidad de países por continente."""
       
    if not lista_paises:
        print("[Aviso] No hay países cargados. Use la opción 1 primero.")
        return

    print("\n--- Estadísticas Generales ---\n")

    # País con mayor y menor población
    mayor_pob = lista_paises[0]
    menor_pob = lista_paises[0]

    total_poblacion = 0
    total_superficie = 0

    for pais in lista_paises:
        # Acumulamos para el promedio
        total_poblacion += pais["poblacion"]
        total_superficie += pais["superficie"]

        # Comparamos para encontrar mayor y menor
        if pais["poblacion"] > mayor_pob["poblacion"]:
            mayor_pob = pais
        if pais["poblacion"] < menor_pob["poblacion"]:
            menor_pob = pais

    print(f"Población más alta: {mayor_pob['nombre']} ({mayor_pob['poblacion']})")
    print(f"Población más baja: {menor_pob['nombre']} ({menor_pob['poblacion']})")

    # Promedios
    cantidad = len(lista_paises)
    promedio_pob = total_poblacion / cantidad
    promedio_sup = total_superficie / cantidad

    print(f"\nPromedio de población : {promedio_pob:.0f}")
    print(f"Promedio de superficie: {promedio_sup:.0f} km²")

    # Cantidad por continente
    print("\nPaíses por continente:")
    continentes = {}
    for pais in lista_paises:
        continente = pais["continente"]
        if continente in continentes:
            continentes[continente] += 1
        else:
            continentes[continente] = 1

    for continente in continentes:
        print(f"  {continente}: {continentes[continente]}")

    volviendo_al_menu()

# =====================================================================
# 7. Guardar cambios y Salir
# =====================================================================
def guardar_datos_csv(ruta_archivo: str, lista_paises: list) -> None:

    if not lista_paises:
        print("[Aviso] No hay países para guardar. Use la opción 1 primero.")
        return

    try:
        with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
            
            escritor.writeheader()  # Escribe la primera fila con los nombres de columnas
            
            for pais in lista_paises:
                escritor.writerow(pais)

        print(f"[Éxito] Datos guardados correctamente en '{ruta_archivo}'.")
        

    except Exception as e:
        print(f"[Error] No se pudo guardar el archivo: {e}")

# =====================================================================
# Menú Principal
# =====================================================================

def mostrar_menu() -> None:
    """Imprime las opciones disponibles en la consola."""

    print(  "\n========================================"
            "      SISTEMA DE GESTIÓN DE PAÍSES      "
            "========================================\n"
            "1. Agregar país\n"
            "2. Actualizar población / superficie\n"
            "3. Buscar país por nombre\n"
            "4. Filtrar países\n"
            "5. Ordenar países\n"
            "6. Mostrar estadísticas generales\n"
            "7. Guardar cambios y Salir\n"
            "========================================\n")

# =====================================================================
# Función Main
# =====================================================================

def ejecutar_sistema():
    """Función principal que controla el flujo de la aplicación."""
    RUTA_CSV = "paises.csv" # Asegurense de tener este archivo en la raíz del proyecto
    
    # Carga inicial de datos
    datos_paises = cargar_datos_csv(RUTA_CSV)
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            cargar_desde_consola(datos_paises) #OK
        elif opcion == "2":
            actualizar_pais(datos_paises)
        elif opcion == "3":
            buscar_pais_nombre(datos_paises)
        elif opcion == "4":
            filtrar_paises(datos_paises)
        elif opcion == "5":
             ordenar_paises(datos_paises)
        elif opcion == "6":
            mostrar_estadisticas(datos_paises)
        elif opcion == "7":
            print("\nGuardando cambios en el archivo...")
            guardar_datos_csv(RUTA_CSV, datos_paises)
            print("\nSaliendo del sistema...")
            print("\nAdios!...")
            break
        else:
            print("\n[Error] Opción inválida. Por favor, intente de nuevo.")

# Punto de entrada al programa
if __name__ == "__main__":
    ejecutar_sistema()

