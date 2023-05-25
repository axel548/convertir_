import os

# Ruta de la carpeta que contiene los archivos
carpeta = '.'

# Obtener la lista de archivos en la carpeta
archivos = os.listdir(carpeta)

arch = []

# Recorrer la lista de archivos
for archivo in archivos:
    # Ruta completa del archivo
    ruta_archivo = os.path.join(carpeta, archivo)

    # Verificar si es un archivo regular (no directorio) y tiene la extensión .json
    if os.path.isfile(ruta_archivo) and archivo.endswith('.json'):
        # Realizar las operaciones necesarias con el archivo JSON
        arch.append(archivo)


# print(arch)

for item in range(0, len(arch)):
    print(arch[item])