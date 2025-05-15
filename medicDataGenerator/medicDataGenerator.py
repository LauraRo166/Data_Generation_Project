import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import numpy as np

fake = Faker('es_ES')

# Proporciones reales de tipos de sangre en Colombia (en porcentaje)
tipos_sangre = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
probabilidades = [0.62, 0.27, 0.07, 0.02, 0.015, 0.007, 0.004, 0.002]

# Peso promedio (kg) por rango de edad y género para Colombia (aproximados)
peso_por_edad_genero = {
    "Masculino": [
        ((0, 1), 10, 2),
        ((2, 5), 16, 3),
        ((6, 12), 32, 6),
        ((13, 18), 58, 10),
        ((19, 40), 72, 12),
        ((41, 60), 76, 14),
        ((61, 100), 73, 15)
    ],
    "Femenino": [
        ((0, 1), 9, 1.8),
        ((2, 5), 15, 2.8),
        ((6, 12), 28, 5),
        ((13, 18), 55, 9),
        ((19, 40), 65, 10),
        ((41, 60), 70, 13),
        ((61, 100), 68, 14)
    ]
}

def peso_según_edad_genero(edad, genero):
    rangos = peso_por_edad_genero[genero]
    for (min_edad, max_edad), peso_prom, desv in rangos:
        if min_edad <= edad <= max_edad:
            peso = max(1, round(np.random.normal(peso_prom, desv), 1))
            return peso
    # Por defecto, peso adulto promedio
    return max(1, round(np.random.normal(70, 15), 1))

def generar_signos_vitales(edad, peso):
    # Temperatura normal (ligera variación)
    temp = round(random.uniform(36.1, 37.2), 1)

    # Frecuencia cardíaca (lpm) según edad
    if edad <= 1:
        fc = random.randint(100, 160)
    elif edad <= 5:
        fc = random.randint(90, 140)
    elif edad <= 12:
        fc = random.randint(70, 120)
    elif edad <= 18:
        fc = random.randint(60, 100)
    else:
        fc = random.randint(60, 100)

    # Frecuencia respiratoria (rpm) según edad
    if edad <= 1:
        fr = random.randint(30, 60)
    elif edad <= 5:
        fr = random.randint(20, 40)
    elif edad <= 12:
        fr = random.randint(18, 30)
    else:
        fr = random.randint(12, 20)

    # Presión arterial (mmHg) ajustada por edad
    if edad < 18:
        sistolica = random.randint(90, 110)
        diastolica = random.randint(60, 70)
    elif edad < 40:
        sistolica = random.randint(110, 130)
        diastolica = random.randint(70, 85)
    else:
        sistolica = random.randint(120, 150)
        diastolica = random.randint(75, 95)

    return temp, (sistolica, diastolica), fc, fr

def evaluar_frecuencia_cardiaca(fc):
    if fc < 60:
        return "Bradicardia"
    elif fc > 100:
        return "Taquicardia"
    else:
        return "Normal"

def evaluar_presion_arterial(sistolica, diastolica):
    if sistolica < 90 or diastolica < 60:
        return "Hipotensión"
    elif sistolica > 140 or diastolica > 90:
        return "Hipertensión"
    else:
        return "Normal"

def evaluar_temperatura(temp):
    if temp < 36.0:
        return "Hipotermia"
    elif temp > 37.5:
        return "Fiebre"
    else:
        return "Normal"

def generar_edad():
    return random.randint(0, 100)

def asignar_fumador(edad, genero):
    prob = 0

    if edad < 14:
        return "No"

    if genero == 'Masculino':
        if edad < 18:
            prob = 0.01
        elif edad <= 24:
            prob = 0.15
        elif edad <= 34:
            prob = 0.20
        elif edad <= 49:
            prob = 0.17
        else:
            prob = 0.10
    elif genero == 'Femenino':
        if edad < 18:
            prob = 0.01
        elif edad <= 24:
            prob = 0.08
        elif edad <= 34:
            prob = 0.10
        elif edad <= 49:
            prob = 0.07
        else:
            prob = 0.05
    return "Sí" if random.random() < prob else "No"

def generar_datos_pacientes(num=100):
    datos = []

    for i in range(1, num + 1):
        genero = random.choice(["Masculino", "Femenino"])
        edad = generar_edad()

        if genero == "Masculino":
            altura = round(np.random.normal(170, 7), 1)
            nombre = fake.first_name_male()
        else:
            altura = round(np.random.normal(158, 6), 1)
            nombre = fake.first_name_female()

        peso = peso_según_edad_genero(edad, genero)
        apellido = fake.last_name()
        fecha_consulta = fake.date_between(start_date='-6M', end_date='today')
        tipo_visita = random.choice(["Consulta general", "Control", "Urgencia", "Especialista"])
        proxima_cita = fecha_consulta + timedelta(days=random.randint(7, 60))

        temp, presion, fc, fr = generar_signos_vitales(edad, peso)

        tipo_sangre = random.choices(tipos_sangre, probabilidades)[0]

        fumador = asignar_fumador(edad, genero)

        datos.append({
            "ID Paciente": f"P{i:05d}",
            "Nombre": nombre,
            "Apellido": apellido,
            "Género": genero,
            "Edad": edad,
            "Altura (cm)": altura,
            "Peso (kg)": peso,
            "Temperatura (°C)": temp,
            "Evaluación Temperatura": evaluar_temperatura(temp),
            "Presión Sistólica": presion[0],
            "Presión Diastólica": presion[1],
            "Evaluación Presión": evaluar_presion_arterial(*presion),
            "Frecuencia Cardíaca (lpm)": fc,
            "Evaluación FC": evaluar_frecuencia_cardiaca(fc),
            "Frecuencia Respiratoria (rpm)": fr,
            "Tipo de Sangre": tipo_sangre,
            "Fumador": fumador,
            "ID Consulta": f"C{i:05d}",
            "Fecha de Consulta": fecha_consulta.strftime('%Y-%m-%d'),
            "Tipo de Visita": tipo_visita,
            "Próxima Cita": proxima_cita.strftime('%Y-%m-%d')
        })

    return datos

def guardar_en_csv(datos, nombre_archivo="consultas_pacientes.csv"):
    if not datos:
        return
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        campos = list(datos[0].keys())
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)

# Ejecutar
datos_pacientes = generar_datos_pacientes(100)
guardar_en_csv(datos_pacientes)
print("Archivo CSV generado exitosamente con edad, peso y altura relacionados.")
