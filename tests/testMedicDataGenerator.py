import unittest
from  medicDataGenerator.medicDataGenerator import (
    generar_datos_pacientes, tipos_sangre, evaluar_temperatura,
    evaluar_presion_arterial, evaluar_frecuencia_cardiaca)

class TestDatosPacientes(unittest.TestCase):
    def TestMedicDataGenerator(self):
        datos = generar_datos_pacientes(100)
        self.assertEqual(len(datos), 100)
        for paciente in datos:
            # Verificar tipos de datos básicos
            self.assertIn(paciente["Género"], ["Masculino", "Femenino"])
            self.assertIsInstance(paciente["Edad"], int)
            self.assertTrue(0 <= paciente["Edad"] <= 100)
            self.assertIsInstance(paciente["Altura (cm)"], float)
            self.assertTrue(130 <= paciente["Altura (cm)"] <= 200)  # rango plausible
            self.assertIsInstance(paciente["Peso (kg)"], float)
            self.assertTrue(1 <= paciente["Peso (kg)"] <= 150)  # rango amplio para peso
            # Temperatura
            temp = paciente["Temperatura (°C)"]
            self.assertTrue(35.0 <= temp <= 40.0)
            # Presión arterial
            self.assertTrue(40 <= paciente["Presión Sistólica"] <= 200)
            self.assertTrue(30 <= paciente["Presión Diastólica"] <= 130)
            # Frecuencia cardíaca y respiratoria
            self.assertTrue(20 <= paciente["Frecuencia Cardíaca (lpm)"] <= 200)
            self.assertTrue(10 <= paciente["Frecuencia Respiratoria (rpm)"] <= 60)
            # Tipo de sangre
            self.assertIn(paciente["Tipo de Sangre"], tipos_sangre)
            # Fumador y alcohol
            self.assertIn(paciente["Fumador"], ["Sí", "No"])
            self.assertIn(paciente["Consume Alcohol"], ["Sí", "No"])
            # Evaluaciones válidas
            self.assertIn(paciente["Evaluación Temperatura"], ["Normal", "Hipotermia", "Fiebre"])
            self.assertIn(paciente["Evaluación FC"], ["Normal", "Bradicardia", "Taquicardia"])
            self.assertIn(paciente["Evaluación Presión"], ["Normal", "Hipotensión", "Hipertensión"])

    def test_altura_genero(self):
        datos = generar_datos_pacientes(200)
        for paciente in datos:
            genero = paciente["Género"]
            altura = paciente["Altura (cm)"]
            # Altura plausible por género (con márgenes amplios pero razonables)
            if genero == "Masculino":
                self.assertTrue(140 <= altura <= 195)
            else:
                self.assertTrue(135 <= altura <= 180)

    def test_evaluaciones_extremas(self):
        pacientes = [
            {"Temperatura (°C)": 34.0, "Frecuencia Cardíaca (lpm)": 40, "Presión Sistólica": 85, "Presión Diastólica": 55, "Edad": 30},
            {"Temperatura (°C)": 39.5, "Frecuencia Cardíaca (lpm)": 130, "Presión Sistólica": 150, "Presión Diastólica": 100, "Edad": 20},
        ]
        self.assertEqual(evaluar_temperatura(pacientes[0]["Temperatura (°C)"]), "Hipotermia")
        self.assertEqual(evaluar_temperatura(pacientes[1]["Temperatura (°C)"]), "Fiebre")

        self.assertEqual(evaluar_frecuencia_cardiaca(pacientes[0]["Frecuencia Cardíaca (lpm)"], pacientes[0]["Edad"]), "Bradicardia")
        self.assertEqual(evaluar_frecuencia_cardiaca(pacientes[1]["Frecuencia Cardíaca (lpm)"], pacientes[1]["Edad"]), "Taquicardia")

        self.assertEqual(evaluar_presion_arterial(pacientes[0]["Presión Sistólica"], pacientes[0]["Presión Diastólica"], pacientes[0]["Edad"]), "Hipotensión")
        self.assertEqual(evaluar_presion_arterial(pacientes[1]["Presión Sistólica"], pacientes[1]["Presión Diastólica"], pacientes[1]["Edad"]), "Hipertensión")

    def test_ids_pacientes_unicos(self):
        datos = generar_datos_pacientes(1000)  # Genera 1000 pacientes
        ids_pacientes = [paciente["ID Paciente"] for paciente in datos]
        self.assertEqual(len(ids_pacientes), len(set(ids_pacientes)),
                         "Los IDs de paciente no son únicos")

    def test_ids_consultas_unicos(self):
        datos = generar_datos_pacientes(1000)  # Genera 1000 pacientes
        ids_consultas = [paciente["ID Consulta"] for paciente in datos]
        self.assertEqual(len(ids_consultas), len(set(ids_consultas)),
                         "Los IDs de consulta no son únicos")

if __name__ == '__main__':
    unittest.main()