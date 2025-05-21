import csv
import random
from faker import Faker
from datetime import datetime, timedelta
import numpy as np
import uuid

fake = Faker('es_ES')

# Proporciones reales de tipos de sangre en Colombia (en porcentaje)
tipos_sangre = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
probabilidades = [0.56, 0.26, 0.07, 0.02, 0.05, 0.03, 0.007, 0.003]

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
    temp = round(random.uniform(35.1, 39.2), 1)

    # Factores de ajuste por temperatura
    aumento_temp = temp > 37.5
    baja_temp = temp < 36.0

    # Frecuencia cardíaca (lpm) según edad
    if edad <= 1:
        fc_base = (100, 160)
    elif edad <= 5:
        fc_base = (90, 140)
    elif edad <= 12:
        fc_base = (70, 120)
    else:
        fc_base = (60, 100)

    fc_min, fc_max = fc_base
    if aumento_temp:
        fc = random.randint(fc_min + 10, fc_max + 10)
    elif baja_temp:

        fc = random.randint(fc_min - 10, fc_max - 10)
    else:
        fc = random.randint(fc_min, fc_max)

    # Frecuencia respiratoria (rpm) según edad
    if edad <= 1:
        fr_base = (30, 60)
    elif edad <= 5:
        fr_base = (20, 40)
    elif edad <= 12:
        fr_base = (18, 30)
    else:
        fr_base = (12, 20)

    fr_min, fr_max = fr_base
    if aumento_temp:
        fr = random.randint(fr_min + 5, fr_max + 5)
    elif baja_temp:
        fr = random.randint(fr_min - 5, fr_max - 5)
    else:
        fr = random.randint(fr_min, fr_max)

    # Presión arterial (mmHg) ajustada por edad
    if edad < 18:
        sis_base = (90, 110)
        dias_base = (60, 70)
    elif edad < 40:
        sis_base = (110, 130)
        dias_base = (70, 85)
    else:
        sis_base = (120, 150)
        dias_base = (75, 95)

    sis_min, sis_max = sis_base
    dias_min, dias_max = dias_base

    if aumento_temp:
        sistolica = random.randint(sis_min + 5, sis_max + 5)
        diastolica = random.randint(dias_min + 3, dias_max + 3)
    elif baja_temp:
        sistolica = random.randint(sis_min - 5, sis_max - 5)
        diastolica = random.randint(dias_min - 3, dias_max - 3)
    else:
        sistolica = random.randint(sis_min, sis_max)
        diastolica = random.randint(dias_min, dias_max)

    return temp, (sistolica, diastolica), fc, fr


def evaluar_frecuencia_cardiaca(fc, edad):
    if edad <= 1:
        if fc < 100:
            return "Bradicardia"
        elif fc > 160:
            return "Taquicardia"
    elif edad <= 5:
        if fc < 90:
            return "Bradicardia"
        elif fc > 140:
            return "Taquicardia"
    elif edad <= 12:
        if fc < 70:
            return "Bradicardia"
        elif fc > 120:
            return "Taquicardia"
    elif edad <= 18:
        if fc < 60:
            return "Bradicardia"
        elif fc > 100:
            return "Taquicardia"
    else:
        if fc < 60:
            return "Bradicardia"
        elif fc > 100:
            return "Taquicardia"
    return "Normal"

def evaluar_presion_arterial(sistolica, diastolica, edad):
    if edad < 1:
        if sistolica < 70 or diastolica < 50:
            return "Hipotensión"
        elif sistolica > 100 or diastolica > 65:
            return "Hipertensión"
    elif edad <= 5:
        if sistolica < 80 or diastolica < 55:
            return "Hipotensión"
        elif sistolica > 110 or diastolica > 75:
            return "Hipertensión"
    elif edad <= 12:
        if sistolica < 90 or diastolica < 60:
            return "Hipotensión"
        elif sistolica > 120 or diastolica > 80:
            return "Hipertensión"
    elif edad <= 18:
        if sistolica < 100 or diastolica < 65:
            return "Hipotensión"
        elif sistolica > 130 or diastolica > 85:
            return "Hipertensión"
    else:
        if sistolica < 90 or diastolica < 60:
            return "Hipotensión"
        elif sistolica > 140 or diastolica > 90:
            return "Hipertensión"
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
    if edad < 12:
        return "No"

    if genero == 'Masculino':
        # Ajustamos las probabilidades para que el promedio total quede cercano a 16.9%
        if 12 <= edad <= 24:
            prob = 0.186  # 18.6%
        elif 25 <= edad <= 44:
            prob = 0.132  # 13.2%
        elif 45 <= edad <= 64:
            prob = 0.117  # 11.7%
        else:  # 65+
            prob = 0.062  # 6.2%

    elif genero == 'Femenino':
        # Ajustamos similar para mujeres con promedio 7.6%, se escalan proporcionalmente
        if 12 <= edad <= 24:
            prob = 0.08  # un poco menor que hombres, proporción basada en dato general
        elif 25 <= edad <= 44:
            prob = 0.055
        elif 45 <= edad <= 64:
            prob = 0.05
        else:  # 65+
            prob = 0.03
    return "Sí" if random.random() < prob else "No"

def asignar_consumo_alcohol(edad, genero):
    """
    Asigna si una persona consume alcohol, basándose en estadísticas reales por edad y género en Colombia.
    La probabilidad fue ajustada a partir de prevalencias por edad y género.
    """
    probabilidad = 0.0

    if genero == "Masculino":
        if 12 <= edad <= 17:
            probabilidad = 0.35  # Ligeramente más alta que la media escolar (72% de hombres)
        elif 18 <= edad <= 24:
            probabilidad = 0.60
        elif 25 <= edad <= 44:
            probabilidad = 0.70
        elif 45 <= edad <= 64:
            probabilidad = 0.65
        elif edad >= 65:
            probabilidad = 0.45
        else:
            probabilidad = 0.01  # Muy baja si menor de 12
    elif genero == "Femenino":
        if 12 <= edad <= 17:
            probabilidad = 0.29  # Más baja en mujeres escolares
        elif 18 <= edad <= 24:
            probabilidad = 0.48
        elif 25 <= edad <= 44:
            probabilidad = 0.58
        elif 45 <= edad <= 64:
            probabilidad = 0.52
        elif edad >= 65:
            probabilidad = 0.35
        else:
            probabilidad = 0.01

    return "Sí" if random.random() < probabilidad else "No"

def edad_ALL(n):
    # Proporciones para cada pico
    prop_pico1 = 0.6  # 60% en el primer pico (niños)
    prop_pico2 = 0.4  # 40% en el segundo pico (adultos)

    # Cantidades para cada pico
    n1 = int(n * prop_pico1)
    n2 = n - n1

    # Distribución normal para cada pico
    pico1 = np.random.normal(loc=3.5, scale=1.0, size=n1)   # pico en 2-5 años
    pico2 = np.random.normal(loc=55, scale=5.0, size=n2)    # pico en 50-60 años

    edades_bimodales = np.concatenate([pico1, pico2])

    # Limitar los valores a rangos plausibles
    edades_bimodales = np.clip(edades_bimodales, 0, 100)

    np.random.shuffle(edades_bimodales)  # Mezclar

    return edades_bimodales

def generar_datos_pacientes(num=100):
    datos = []

    edades_diagnostico = edad_ALL(num)

    for i in range(num):
        genero = random.choice(["Masculino", "Femenino"])
        edad = generar_edad()

        if genero == "Masculino":
            altura = round(np.random.normal(171, 7), 1)
            nombre = fake.first_name_male()
        else:
            altura = round(np.random.normal(158, 6), 1)
            nombre = fake.first_name_female()

        peso = peso_según_edad_genero(edad, genero)
        apellido = fake.last_name()
        fecha_consulta = fake.date_between(start_date='-6M', end_date='today')
        tipo_visita = random.choice(["Consulta general", "Control", "Urgencia", "Especialista"])
        proxima_cita = fecha_consulta + timedelta(days=random.randint(7, 60))
        temp, (sis, dias), fc, fr = generar_signos_vitales(edad, peso)
        tipo_sangre = random.choices(tipos_sangre, probabilidades)[0]
        fumador = asignar_fumador(edad, genero)

        datos.append({
            "ID Paciente": str(uuid.uuid4()),
            "Nombre": nombre,
            "Apellido": apellido,
            "Género": genero,
            "Edad": edad,
            "Altura (cm)": altura,
            "Peso (kg)": peso,
            "Temperatura (°C)": temp,
            "Evaluación Temperatura": evaluar_temperatura(temp),
            "Presión Sistólica": sis,
            "Presión Diastólica": dias,
            "Evaluación Presión": evaluar_presion_arterial(sis, dias, edad),
            "Frecuencia Cardíaca (lpm)": fc,
            "Evaluación FC": evaluar_frecuencia_cardiaca(fc, edad),
            "Frecuencia Respiratoria (rpm)": fr,
            "Tipo de Sangre": tipo_sangre,
            "Fumador": fumador,
            "Consume Alcohol": asignar_consumo_alcohol(edad, genero),
            "Edad de diagnóstico ALL (años)": round(edades_diagnostico[i], 1),
            "ID Consulta": str(uuid.uuid4()),
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
datos_pacientes = generar_datos_pacientes(100000)
guardar_en_csv(datos_pacientes)
print("Archivo CSV generado exitosamente.")
