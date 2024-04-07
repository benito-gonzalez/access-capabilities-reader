import os
import json
import pandas as pd
import pdfplumber
from src import constants


def create_dict_struct(row):
    return {
        "Comunidad Autónoma": row[0],
        "Provincia": row[1],
        "Municipio": row[2],
        "Subestación": row[3],
        "Ubicación (Latitud)": row[4],
        "Ubicación (Longitud)": row[5],
        "Tensión (kV)": row[6],
        "CAPACIDAD DE ACCESO (MW)": {
            "DISPONIBLE": row[7],
            "OCUPADA": {
                "TOTAL": row[8],
                "Desglose por Posición de SSEE": {
                    "P1": row[9],
                    "P2": row[10],
                    "P3": row[11],
                    "P4": row[12],
                    "P5": row[13],
                    "P6": row[14],
                    "P7": row[15],
                    "P8": row[16],
                    "P9": row[17],
                    "Con Permiso de AyC": row[18],
                    "En trámite con Capacidad en RdD": row[19]
                }
            },
            "ADMITIDA Y NO RESUELTA": {
                "TOTAL": row[20],
                "Desglose por Tecnologia": {
                    "Eólica": row[21],
                    "Fotovolaica": row[22],
                    "Hidráulica": row[23],
                    "Solar Térmica": row[24],
                    "Resto de Tecnologías": row[25]
                }
            }
        },
        "Nudo de Afección Mayoritaria en la Red de Transporte": row[26],
        "Comentarios": row[27]
    }


def fix_column_names(column_names):
    fixed_column_names = []
    for name in column_names:
        if name.startswith('acilóE'):
            fixed_column_names.append('Eólica')
        elif name.startswith('aciatlovotoF'):
            fixed_column_names.append('Fotovoltaica')
        elif name.startswith('acilúardiH'):
            fixed_column_names.append('Hidráulica')
        elif name.startswith('acim'):
            fixed_column_names.append('Solar\nTérmica')
        elif name.startswith('otse'):
            fixed_column_names.append('Resto de\nTecnologías')
        else:
            fixed_column_names.append(name)
    return fixed_column_names


def append_to_json(json_file: str, plan_dict: dict):
    existing_data = []

    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            existing_data = json.load(file)

    existing_data.append(plan_dict)

    # Write the updated data back to the file
    with open(json_file, 'w') as file:
        json.dump(existing_data, file, indent=4, ensure_ascii=False)


def generate_json_from_file(pdf_file_name):
    path_file = os.path.join(constants.DATA_PATH, pdf_file_name)
    raw_file_name = pdf_file_name.split(".")[0]
    json_file = os.path.join(constants.DATA_PATH, f"{raw_file_name}.json")

    with pdfplumber.open(path_file) as pdf:
        for page_number in range(1, len(pdf.pages)):
            page = pdf.pages[page_number]
            table = page.extract_table()
            if table:
                for i in range(4, len(table)):
                    d = create_dict_struct(table[i])
                    append_to_json(json_file, d)


def generate_csv_from_file(pdf_file_name):
    path_file = os.path.join(constants.DATA_PATH, pdf_file_name)
    all_tables = []
    with pdfplumber.open(path_file) as pdf:
        for page_number in range(1, len(pdf.pages)):
            page = pdf.pages[page_number]
            table = page.extract_table()
            if table:
                # if it is the first page, we have to put the headers:
                if not all_tables:
                    table[3] = fix_column_names(table[3])
                    header_content = table[3:]
                    all_tables.extend(header_content)
                else:
                    content = table[4:]
                    all_tables.extend(content)

    df = pd.DataFrame(all_tables)
    raw_file_name = pdf_file_name.split(".")[0]
    csv_file = os.path.join(constants.DATA_PATH, f"{raw_file_name}.csv")
    df.to_csv(csv_file, index=False)
    return df


if __name__ == "__main__":
    generate_json_from_file("EDRD_Capacidad_de_Acceso_2024_03_01.pdf")
