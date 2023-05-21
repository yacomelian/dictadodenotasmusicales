import argparse
import datetime
import os
import random
import subprocess
import signal
import sys
import time

from gtts import gTTS

# Lista de notas musicales
notas = ["do", "re", "mi", "fa", "sol", "la", "si"]

# Textos utilizados en el juego
textos = {
    'vacio': 'LA LA LA',
    'bienvenida': '¡Bienvenida al dictado de notas musicales!',
    'inicio': 'Empezamos',
    'fin': 'Gracias por jugar. ¡Hasta la próxima!',
    'ficheromalo': 'Uy, pero que fichero es este, así no podemos jugar.'
}

# Rutas
ruta_audios = "audios"
ruta_dictados = "dictados"

TIEMPO_ENTRE_NOTAS = 2.5  # Segundos, pueden ser decimales, por ejemplo 1.5
MAX_NOTAS = 100

# Obtener la fecha actual para utilizarla en los nombres de archivo
fecha_archivo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Nombres de los archivos de dictado
nombre_archivo_dictado = f"dictado_de_notas_{fecha_archivo}.txt"

# Números mágicos que identifican archivos MP3 válidos
magic_numbers_mp3 = [b'\x49\x44\x33', b'\xFF\xFB', b'\xFF\xF2', b'\xFF\xF3']

def generar_nota_aleatoria():
    """
    Genera una nota aleatoria seleccionada de la lista 'notas'.

    Returns:
        str: La nota seleccionada aleatoriamente.
    """
    return random.choice(notas)

def generar_audio(texto, nombre_archivo):
    """
    Genera un archivo de audio a partir del texto proporcionado utilizando la biblioteca gTTS.

    Args:
        texto (str): El texto a convertir en audio.
        nombre_archivo (str): El nombre del archivo de salida.

    Returns:
        None
    """
    ruta_archivo = os.path.join(ruta_audios, nombre_archivo)
    if not existe_mp3(ruta_archivo):
        tts = gTTS(text=texto, lang='es')
        tts.save(ruta_archivo)

def crear_voces_textos():
    """
    Crea archivos de audio para cada texto en el diccionario 'textos' utilizando la biblioteca gTTS.

    Cada archivo de audio se guarda con el nombre de la clave correspondiente en el diccionario,
    y se agrega la extensión '.mp3'.

    La función verifica la existencia del archivo antes de crearlo para evitar sobreescribir archivos existentes.
    
    Returns:
        None
    """
    for clave, texto in textos.items():
        nombre_archivo = f"{clave}.mp3"
        generar_audio(texto, nombre_archivo)

def crear_voces_notas():
    """
    Crea archivos de audio para cada nota en la lista 'notas' utilizando la biblioteca gTTS.

    Cada archivo de audio se guarda con el formato 'XX-nota.mp3', donde XX es un número de dos dígitos
    y 'nota' es el nombre de la nota correspondiente.

    La función verifica la existencia del archivo antes de crearlo para evitar sobreescribir archivos existentes.
    
    Returns:
        None
    """
    for i, nota in enumerate(notas):
        nombre_archivo = f"{i:02}-{nota}.mp3"
        generar_audio(nota, nombre_archivo)
        

def crear_carpetas():
    """
    Crea las carpetas 'audios' y 'dictados' si no existen.
    """
    if not os.path.exists(ruta_audios):
        os.makedirs(ruta_audios)
    
    if not os.path.exists(ruta_dictados):
        os.makedirs(ruta_dictados)

def existe_mp3(ruta):
    """
    Verifica si el archivo en la ruta especificada es un archivo MP3 válido.

    Args:
        ruta (str): La ruta del archivo a verificar.

    Returns:
        bool: True si el archivo existe y es un archivo MP3 válido, False en caso contrario.
    """
    if os.path.isfile(ruta):
        with open(ruta, 'rb') as archivo:
            primeros_bytes = archivo.read(max(len(m) for m in magic_numbers_mp3))
            for magic_number in magic_numbers_mp3:
                if primeros_bytes.startswith(magic_number):
                    return True
    return False

def reproducir_audio(texto, modo_depuracion=False):
    """
    Reproduce el archivo de audio correspondiente al texto proporcionado.

    Args:
        texto (str): El nombre del archivo de audio a reproducir.
        modo_depuracion (bool): Indica si se debe mostrar la salida en la consola (True) o redirigirla (False).

    Returns:
        None
    """
    nombre_archivo = f"{texto}.mp3"
    ruta_archivo = os.path.join(ruta_audios, nombre_archivo)
    if modo_depuracion:
        salida = None  # La salida se muestra en la consola
    else:
        salida = open(os.devnull, 'w')  # La salida se redirige a /dev/null o nul en Windows

    proceso = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", ruta_archivo], stdout=salida, stderr=salida)
    proceso.wait()

    if not modo_depuracion:
        salida.close()

def guarda_para_comprobar_o_repetir(partida):
    """
    Guarda el resultado de la partida en un archivo para comprobar o volver a reproducir.

    El resultado de la partida se guarda en un archivo de texto llamado 'partida.txt'.
    Cada nota generada se guarda en una línea separada dentro del archivo.

    Args:
        partida (list): Lista de notas generadas en la partida.

    Returns:
        None
    """
    ruta_archivo = os.path.join(ruta_dictados, nombre_archivo_dictado)
    with open(ruta_archivo, 'w') as archivo:
        for nota in partida:
            archivo.write(nota + '\n')
    
    print(f"El resultado de la partida se ha guardado en el archivo '{ruta_archivo}'.")


def reproducir_notas(partida, tiempo_entre_notas):
    """
    Reproduce las notas generadas en la partida utilizando los archivos de audio correspondientes.

    Args:
        partida (list): Lista de notas generadas en la partida.
        tiempo_entre_notas (float): Tiempo en segundos entre la reproducción de cada nota.

    Returns:
        None
    """
    for nota in partida:
        try:
            nombre_archivo = f"{notas.index(nota):02}-{nota}"
            reproducir_audio(nombre_archivo)
            time.sleep(tiempo_entre_notas)
        except ValueError:
            print(f"Error: Este fichero no parece que contenga notas musicales.")
            reproducir_audio('ficheromalo')
            break

def juega(numero_de_notas):
    """
    Juego para generar y mostrar notas aleatorias.

    El juego genera 'numero_de_notas' notas aleatorias utilizando la función 'generar_nota_aleatoria'.
    Las notas generadas se almacenan en una lista 'dictado_notas' y luego se muestra por pantalla.

    Args:
        numero_de_notas (int): El número de notas aleatorias a generar y mostrar.

    Returns:
        list: La lista de notas generadas.
    """
    dictado_notas = []
    for _ in range(numero_de_notas):
        nota = generar_nota_aleatoria()
        dictado_notas.append(nota)

    print(dictado_notas)
    return dictado_notas

def reproducir_juego(partida, tiempo_entre_notas):
    """
    Reproduce el juego de notas aleatorias.

    El juego comienza reproduciendo los audios de bienvenida y luego reproduce las notas de la partida.

    Args:
        partida (list): Lista de notas generadas en la partida.
        tiempo_entre_notas (float): Tiempo en segundos entre la reproducción de cada nota.

    Returns:
        None
    """
    reproducir_audio('vacio')
    reproducir_audio('bienvenida')
    reproducir_audio('inicio')
    reproducir_notas(partida, tiempo_entre_notas)
    despedida()

def despedida():
    reproducir_audio('fin')

def salir_elegantemente(signal, frame):
    print("\nJuego interrumpido por el usuario.")
    despedida()
    sys.exit(0)

def main(args):
    """
    Función principal del programa.

    Args:
        args (Namespace): Los argumentos de línea de comandos.

    Returns:
        None
    """


    # Manejo de la señal de interrupción del usuario
    signal.signal(signal.SIGINT, salir_elegantemente)

    # Creo componentes necesarios
    crear_carpetas()
    crear_voces_textos()
    crear_voces_notas()

    # Gestiono los valores de entrada
    tiempo_entre_notas = args.tiempo
    if args.fichero:
        # Se pasa un archivo de partida como argumento
        archivo_partida = args.fichero
        if not os.path.exists(archivo_partida):
            print("Error: El archivo de partida especificado no existe.")
            return
        with open(archivo_partida, 'r') as archivo:
            partida = [line.strip() for line in archivo]
    else:
        # No se pasa un archivo de partida, se inicia el juego
        if args.notas:
            numero_de_notas = args.notas
            if not isinstance(numero_de_notas, int) or numero_de_notas >= 100:
                print("Error: El número debe ser un entero menor a 100.")
                return
        else:
            while True:
                try:
                    numero_de_notas = int(input("Ingrese el número de notas aleatorias a reproducir (menor a 100): "))
                    if numero_de_notas < 100:
                        break
                    else:
                        print("Error: El número debe ser menor a 100.")
                except ValueError:
                    print("Error: Por favor, introduzca un número válido.")

        partida = juega(numero_de_notas)
        guarda_para_comprobar_o_repetir(partida)

    # Ya tenemos la partida, ahora vamos con el audio
    reproducir_juego(partida, tiempo_entre_notas)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dictado de notas musicales.')
    parser.add_argument('-n', '--notas', type=int, help='Número de notas aleatorias a reproducir.')
    parser.add_argument('-t', '--tiempo', type=float, default=TIEMPO_ENTRE_NOTAS,
                        help='Tiempo en segundos entre notas aleatorias.')
    parser.add_argument('-f', '--fichero', type=str, help='Ruta del archivo de partida.')

    args = parser.parse_args()
    main(args)
