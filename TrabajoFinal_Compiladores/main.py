import os  # Importa el módulo os para operaciones del sistema operativo
import re  # Se importa para trabajar con parentesis en la ultima gramatica


# Función para calcular el conjunto 'Primero' de cada no terminal en las producciones
def computar_pr(producciones):
    # Inicializa un diccionario 'primero' donde cada no terminal tiene un conjunto vacío
    primero = {no_terminal: set() for no_terminal in producciones}

    # Bucle infinito que se romperá cuando no haya más actualizaciones
    while True:
        actualizado = False  

        # Recorre cada no terminal en las producciones
        for no_terminal in producciones:
            # Recorre cada producción del no terminal actual
            for produccion in producciones[no_terminal]:
                # Si la producción es 'epsilon', lo añade al conjunto 'Primero' del no terminal
                if produccion == 'epsilon':
                    if 'epsilon' not in primero[no_terminal]:
                        primero[no_terminal].add('epsilon')
                        actualizado = True  # Marca que hubo una actualización
                else:
                    # Recorre cada símbolo en la producción
                    for simbolo in produccion:
                        if simbolo in producciones:
                            # Agrega los elementos del conjunto 'Primero' del símbolo actual al conjunto 'Primero' del no terminal actual, excepto 'epsilon'
                            # Guarda el tamaño actual del conjunto 'Primero' del no terminal
                            antes = len(primero[no_terminal])
                            primero[no_terminal].update(primero[simbolo] - {'epsilon'})
                            if len(primero[no_terminal]) > antes:
                                actualizado = True  # Marca que hubo una actualización
                            # Si el símbolo no contiene 'epsilon', termina el bucle
                            if 'epsilon' not in primero[simbolo]:
                                break
                        else:
                            # Si el símbolo es un terminal, lo añade directamente al conjunto 'Primero' del no terminal actual
                            if simbolo not in primero[no_terminal]:
                                primero[no_terminal].add(simbolo)
                                actualizado = True  # Marca que hubo una actualización
                            break
                    else:
                        # Si todos los símbolos pueden derivar 'epsilon', se añade 'epsilon' al conjunto 'Primero' del no terminal
                        if 'epsilon' not in primero[no_terminal]:
                            primero[no_terminal].add('epsilon')
                            actualizado = True  # Marca que hubo una actualización
        # Si no hubo actualizaciones en esta iteración, rompe el bucle
        if not actualizado:
            break

    return primero  # Devuelve el diccionario 'primero' con los conjuntos 'Primero' de cada no terminal


# Función para calcular el conjunto 'Siguiente' de cada no terminal en las producciones
def computar_sig(producciones, primero):
    # Inicializa un diccionario 'siguiente' donde cada no terminal tiene un conjunto vacío
    siguiente = {no_terminal: set() for no_terminal in producciones}
    # Obtiene el símbolo inicial (el primer no terminal en las producciones) y añade '$' a su conjunto 'Siguiente'
    simbolo_inicio = next(iter(producciones))
    siguiente[simbolo_inicio].add('$')

    # Bucle infinito que se romperá cuando no haya más actualizaciones
    while True:
        actualizado = False  

        # Recorre cada no terminal y sus reglas de producción
        for no_terminal, reglas in producciones.items():
            for regla in reglas:
                # Copia temporalmente el conjunto 'Siguiente' del no terminal actual
                siguiente_temporal = siguiente[no_terminal].copy()
                # Recorre la regla de producción de derecha a izquierda
                for i in range(len(regla) - 1, -1, -1):
                    simbolo = regla[i]
                    if simbolo in producciones:
                        # Actualiza el conjunto 'Siguiente' del símbolo actual con el conjunto temporal
                        anterior = siguiente[simbolo].copy()
                        siguiente[simbolo].update(siguiente_temporal)
                        if siguiente[simbolo] != anterior:
                            actualizado = True  # Marca que hubo una actualización
                        # Si el símbolo puede derivar 'epsilon', añade el conjunto 'Primero' del símbolo al conjunto temporal
                        if 'epsilon' in primero[simbolo]:
                            siguiente_temporal = siguiente_temporal.union(primero[simbolo] - {'epsilon'})
                        else:
                            siguiente_temporal = primero[simbolo]
                    else:
                        # Si el símbolo es un terminal, establece el conjunto temporal al símbolo
                        siguiente_temporal = {simbolo}
        # Si no hubo actualizaciones en esta iteración, rompe el bucle
        if not actualizado:
            break

    return siguiente  # Devuelve el diccionario 'siguiente' con los conjuntos 'Siguiente' de cada no terminal


# Función alternativa para calcular el conjunto 'Primero' de cada no terminal en producciones con alternas
def computar_primero_alternas(producciones):
    # Inicializa un diccionario 'primero' donde cada no terminal tiene un conjunto vacío
    primero = {no_terminal: set() for no_terminal in producciones}

    # Bucle infinito que se romperá cuando no haya más actualizaciones
    while True:
        actualizado = False  

        # Recorre cada no terminal en las producciones
        for no_terminal in producciones:
            # Recorre cada producción del no terminal actual
            for produccion in producciones[no_terminal]:
                # Si la producción es 'epsilon', lo añade al conjunto 'Primero' del no terminal
                if produccion == 'epsilon':
                    if 'epsilon' not in primero[no_terminal]:
                        primero[no_terminal].add('epsilon')
                        actualizado = True  # Marca que hubo una actualización
                else:
                    # Utiliza expresiones regulares para separar los símbolos, incluyendo paréntesis
                    # La expresión re.findall(r'\w+|[()]', produccion) se utiliza para dividir una cadena produccion en partes utilizando una expresión regular
                    # El propósito de esta expresión regular es dividir la producción en una lista de símbolos, donde cada símbolo es una palabra (formada por caracteres alfanuméricos) o un paréntesis. 
                    # Esto es útil para analizar y procesar las producciones que contienen paréntesis o palabras como símbolos.
                    simbolos = re.findall(r'\w+|[()]', produccion) 
                    for simbolo in simbolos:
                        if simbolo in producciones:
                            # Agrega los elementos del conjunto 'Primero' del símbolo actual al conjunto 'Primero' del no terminal actual, excepto 'epsilon'
                            antes = len(primero[no_terminal])
                            primero[no_terminal].update(primero[simbolo] - {'epsilon'})
                            if len(primero[no_terminal]) > antes:
                                actualizado = True  # Marca que hubo una actualización
                            # Si el símbolo no contiene 'epsilon', termina el bucle
                            if 'epsilon' not in primero[simbolo]:
                                break
                        else:
                            # Si el símbolo es un terminal, lo añade directamente al conjunto 'Primero' del no terminal actual
                            if simbolo not in primero[no_terminal]:
                                primero[no_terminal].add(simbolo)
                                actualizado = True  # Marca que hubo una actualización
                            break
                    else:
                        # Si todos los símbolos pueden derivar 'epsilon', se añade 'epsilon' al conjunto 'Primero' del no terminal
                        if 'epsilon' not in primero[no_terminal]:
                            primero[no_terminal].add('epsilon')
                            actualizado = True  # Marca que hubo una actualización
        # Si no hubo actualizaciones en esta iteración, rompe el bucle
        if not actualizado:
            break

    return primero  # Devuelve el diccionario 'primero' con los conjuntos 'Primero' de cada no terminal


# Función alternativa para calcular el conjunto 'Siguiente' de cada no terminal en producciones con paréntesis
def computar_siguiente_alternas(producciones, primero):
    # Inicializa un diccionario 'siguiente' donde cada no terminal tiene un conjunto vacío
    siguiente = {no_terminal: set() for no_terminal in producciones}
    # Obtiene el símbolo inicial (el primer no terminal en las producciones) y añade '$' a su conjunto 'Siguiente'
    simbolo_inicio = next(iter(producciones))
    siguiente[simbolo_inicio].add('$')

    # Bucle infinito que se romperá cuando no haya más actualizaciones
    while True:
        actualizado = False  

        # Recorre cada no terminal y sus reglas de producción
        for no_terminal, reglas in producciones.items():
            for regla in reglas:
                # Copia temporalmente el conjunto 'Siguiente' del no terminal actual
                siguiente_temporal = siguiente[no_terminal].copy()
                # Utiliza expresiones regulares para separar los símbolos, incluyendo paréntesis
                simbolos = re.findall(r'\w+|[()]', regla)
                # Recorre la regla de producción de derecha a izquierda
                for i in range(len(simbolos) - 1, -1, -1):
                    simbolo = simbolos[i]
                    if simbolo in producciones:
                        # Actualiza el conjunto 'Siguiente' del símbolo actual con el conjunto temporal
                        anterior = siguiente[simbolo].copy()
                        siguiente[simbolo].update(siguiente_temporal)
                        if siguiente[simbolo] != anterior:
                            actualizado = True  # Marca que hubo una actualización
                        # Si el símbolo puede derivar 'epsilon', añade el conjunto 'Primero' del símbolo al conjunto temporal
                        if 'epsilon' in primero[simbolo]:
                            siguiente_temporal = siguiente_temporal.union(primero[simbolo] - {'epsilon'})
                        else:
                            siguiente_temporal = primero[simbolo]
                    else:
                        # Si el símbolo es un terminal, establece el conjunto temporal al símbolo
                        siguiente_temporal = {simbolo}
        # Si no hubo actualizaciones en esta iteración, rompe el bucle
        if not actualizado:
            break

    return siguiente  # Devuelve el diccionario 'siguiente' con los conjuntos 'Siguiente' de cada no terminal


# Función principal del programa
def main():
    try:
        entrada = 'C:/Users/Miguel/PycharmProjects/TrabajoFinal_Compiladores/glcs.in'  # Nombre del archivo de entrada
        salida = 'C:/Users/Miguel/PycharmProjects/TrabajoFinal_Compiladores/pr_sig.out'  # Nombre del archivo de salida

        # Verifica si el archivo de entrada existe
        if not os.path.exists(entrada):
            print(
                f"\nEl archivo de entrada '{entrada}' no existe. Asegúrate de haberlo creado y colocado en el directorio correcto.")
            return  # Termina la ejecución del programa

        with open(entrada, 'r') as infile:
            # Lee el número de casos del archivo de entrada
            casos = int(infile.readline().strip())
            resultados = []  # Lista para almacenar los resultados de cada caso

            # Procesa cada caso
            for caso_numero in range(casos):
                k = int(infile.readline().strip())  # Lee el número de producciones para este caso
                producciones = {}  # Diccionario para almacenar las producciones

                # Lee cada producción y las añade al diccionario
                for _ in range(k):
                    linea = infile.readline().strip()
                    no_terminal, prod = linea.split('->')
                    no_terminal = no_terminal.strip()
                    alternativas = [alt.strip() for alt in prod.split('|')]
                    producciones[no_terminal] = alternativas

                # Determina el tipo de producciones y calcula 'Primero' y 'Siguiente' en consecuencia
                if all(no_terminal.isupper() for no_terminal in producciones):
                    primero = computar_pr(producciones)
                    siguiente = computar_sig(producciones, primero)
                elif all((len(no_terminal) > 1) for no_terminal in producciones):
                    primero = computar_primero_alternas(producciones)
                    siguiente = computar_siguiente_alternas(producciones, primero)

                resultado = []  # Lista para almacenar los resultados de este caso
                resultado.append(f"{k}")  # Añade el número de producciones al resultado

                # Añade el conjunto 'Primero' de cada no terminal al resultado
                for no_terminal in producciones:
                    conjunto_primero = ', '.join(sorted(primero[no_terminal]))
                    resultado.append(f"Pr({no_terminal}) = {{{conjunto_primero}}}")

                # Añade el conjunto 'Siguiente' de cada no terminal al resultado
                for no_terminal in producciones:
                    follow_set = ', '.join(sorted(siguiente[no_terminal]))
                    resultado.append(f"Sig({no_terminal}) = {{{follow_set}}}")

                resultados.append(resultado)  # Añade el resultado de este caso a la lista de resultados

        with open(salida, 'w') as outfile:
            # Escribe el número de casos en el archivo de salida
            outfile.write(f"{casos}\n")
            # Escribe los resultados de cada caso en el archivo de salida
            for resultado in resultados:
                outfile.write('\n'.join(resultado) + '\n')

        print(f"\nEl archivo de salida se ha generado correctamente en {salida}")  # Imprime mensaje de éxito

    except Exception as e:
        print(f"Error: {e}")  # Imprime mensaje de error en caso de excepción


if __name__ == "__main__":
    main()  # Llama a la función principal si el script se ejecuta directamente
