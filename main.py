import pandas as pd
import json
import os



# Función recursiva para construir el DataFrame
def build_dataframe(data, prefix='', level=0):
    if isinstance(data, dict):
        rows = []
        for key, value in data.items():
            new_prefix = f'{prefix}.{key}' if prefix else key
            rows.extend(build_dataframe(value, new_prefix, level+1))
            if level == 2:
                rows.append(('', ''))
        if level <= 1:
            rows.insert(0, (prefix, ''))
        return rows
    elif isinstance(data, list):
        if isinstance(data[0], str):
            data_str = json.dumps(data)
            return [(prefix, data_str)]
        else:
            rows = []
            for index, item in enumerate(data):
                new_prefix = f'{prefix}[{index}]' if prefix else f'[{index}]'
                rows.extend(build_dataframe(item, new_prefix, level+1))
            if level <= 1:
                rows.insert(0, (prefix, ''))
            return rows
    else:
        return [(prefix, data)]



# Función para convertir el json a excel
def convert_json_to_excel(filename_json, filename_excel):
    # Cargar el JSON desde un archivo
    with open(filename_json) as archivo:
        json_data = json.load(archivo)

    # Construir el DataFrame a partir del JSON
    df = pd.DataFrame(build_dataframe(json_data), columns=['Campo', 'Valor'])

    # Dividir la columna 'Campo' en múltiples columnas
    df[['Nivel {}'.format(i+1) for i in range(df['Campo'].str.count('\.').max() + 1)]] = df['Campo'].str.split('.', expand=True)

    # Eliminar la columna 'Campo'
    df = df.drop('Campo', axis=1)

    # Reemplazar los valores duplicados en los niveles anteriores con una cadena vacía
    for i in range(1, df.columns.str.startswith('Nivel').sum()):
        col_name = 'Nivel {}'.format(i)
        mask = df[col_name].duplicated()
        df.loc[mask, col_name] = ''

    # Obtener el índice de la columna 'Valor'
    valor_index = df.columns.get_loc('Valor')

    # Mover la columna 'Valor' al final
    df = df[[col for col in df.columns if col != 'Valor'] + ['Valor']]

    # Guardar el DataFrame como archivo de Excel

    df.to_excel(filename_excel, index=False)


# Función que retorna un batch de json de la carpeta .
def retrieve_json_from_filesystem():
    carpeta = '.'
    archivos = os.listdir(carpeta)
    arch = []
    for archivo in archivos:
        # Ruta completa del archivo
        ruta_archivo = os.path.join(carpeta, archivo)

        # Verificar si es un archivo regular (no directorio) y tiene la extensión .json
        if os.path.isfile(ruta_archivo) and archivo.endswith('.json'):
            # Realizar las operaciones necesarias con el archivo JSON
            arch.append(archivo)
    return arch




print("Tipo de extracción:")
print("1. Individual")
print("2. BATCH")
option = int(input("ingrese la opción:"))

if option == 1:
    filename = input("Nombre del archivo: ")
    filename_json = filename + ".json"
    filename_excel = filename + ".xlsx"
    convert_json_to_excel(filename_json, filename_excel)
else:
    json_files = retrieve_json_from_filesystem()
    for item in range(0, len(json_files)):
        excel = json_files[item].replace('.json', '.xlsx')
        convert_json_to_excel(json_files[item], excel)
