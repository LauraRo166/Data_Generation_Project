import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter

# Cargar datos
df = pd.read_csv('consultas_pacientes.csv')

# Normalizar Género
df["Género"] = df["Género"].str.strip().str.lower()
df = df[df["Género"].isin(["masculino", "femenino"])]

# -----------------------------
# 1. Distribución de Altura por Género
# -----------------------------
df["Altura (cm)"] = pd.to_numeric(df["Altura (cm)"], errors='coerce')
df = df.dropna(subset=["Altura (cm)"])
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df[df["Género"] == "masculino"], x="Altura (cm)", label="Masculino",
            color="#1f77b4", fill=True, alpha=0.5, linewidth=2)
sns.kdeplot(data=df[df["Género"] == "femenino"], x="Altura (cm)", label="Femenino",
            color="#e377c2", fill=True, alpha=0.5, linewidth=2)
plt.axvline(df[df["Género"] == "masculino"]["Altura (cm)"].mean(), color="#1f77b4", linestyle='--')
plt.axvline(df[df["Género"] == "femenino"]["Altura (cm)"].mean(), color="#e377c2", linestyle='--')
plt.xlabel("Altura (cm)")
plt.ylabel("Densidad")
plt.title("Distribución de Altura por Género")
plt.legend(title="Género")
plt.tight_layout()
plt.show()

# -----------------------------
# 2. Distribución de Tipos de Sangre
# -----------------------------
tipos_sangre = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
conteo = Counter(df['Tipo de Sangre'])
total = sum(conteo.values())
frecuencias = [(conteo.get(tipo, 0) / total) * 100 for tipo in tipos_sangre]
colores = ['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0', '#00BCD4', '#795548', '#607D8B']
plt.figure(figsize=(10, 6))
barras = plt.bar(tipos_sangre, frecuencias, color=colores)
for barra, valor in zip(barras, frecuencias):
    plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.5,
             f'{valor:.1f}%', ha='center', fontsize=10)
plt.title('Distribución Observada de Tipos de Sangre')
plt.ylabel('Porcentaje (%)')
plt.xlabel('Tipo de Sangre')
plt.ylim(0, max(frecuencias) + 5)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# -----------------------------
# 3. Dispersión Peso vs Edad
# -----------------------------
plt.figure(figsize=(10, 6))
plt.scatter(df['Edad'], df['Peso (kg)'], alpha=0.6, edgecolor='k')
plt.title('Dispersión de Peso vs Edad')
plt.xlabel('Edad (años)')
plt.ylabel('Peso (kg)')
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# 4. Fumadores por Género
# -----------------------------
df_fumadores = df[df["Fumador"] == "Sí"]
conteo_fumadores = df_fumadores["Género"].value_counts()
plt.figure(figsize=(7, 7))
plt.pie(conteo_fumadores, labels=conteo_fumadores.index.str.capitalize(),
        autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#e377c2'], textprops={'fontsize': 14})
plt.title("Distribución de Fumadores por Género", fontsize=16)
plt.axis('equal')
plt.tight_layout()
plt.show()

# -----------------------------
# 5. Distribución Edad Fumadores
# -----------------------------
plt.figure(figsize=(10, 6))
sns.kdeplot(df[df["Fumador"] == "Sí"]["Edad"], label="Fumadores", color="red", fill=True, alpha=0.5)
plt.title("Distribución de Edad según Fumador")
plt.xlabel("Edad")
plt.ylabel("Densidad")
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# 6. Medidas por Rango de Edad
# -----------------------------
def categorizar_edad(edad):
    if edad <= 11:
        return "Niños (0-11)"
    elif edad <= 18:
        return "Jóvenes (12-18)"
    elif edad <= 40:
        return "Adultos jóvenes (19-40)"
    elif edad <= 65:
        return "Adultos (41-65)"
    else:
        return "Mayores (66+)"

df["Rango de Edad"] = df["Edad"].apply(categorizar_edad)

def graficar_variable_por_rango(var):
    stats = df.groupby('Rango de Edad')[var].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Rango de Edad', y=var, data=stats, hue='Rango de Edad',
                palette="Set2", dodge=False, legend=False,
                order=["Niños (0-11)", "Jóvenes (12-18)", "Adultos jóvenes (19-40)",
                       "Adultos (41-65)", "Mayores (66+)"])
    plt.title(f'Media de {var} por Rango de Edad')
    plt.ylabel(var)
    plt.xlabel('Rango de Edad')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

variables = [
    "Frecuencia Cardíaca (lpm)",
    "Presión Sistólica",
    "Frecuencia Respiratoria (rpm)"
]
for var in variables:
    graficar_variable_por_rango(var)

# -----------------------------
# 7. Consumo de Alcohol por Género y Edad
# -----------------------------
consumo = df.groupby(["Rango de Edad", "Género"])["Consume Alcohol"].value_counts(normalize=True).rename("Proporción").reset_index()
consumo_si = consumo[consumo["Consume Alcohol"] == "Sí"]
plt.figure(figsize=(10, 6))
sns.barplot(data=consumo_si, x="Rango de Edad", y="Proporción", hue="Género", palette="Set1")
plt.title("Proporción de Consumo de Alcohol por Rango de Edad y Género")
plt.ylabel("Proporción que consume alcohol")
plt.xlabel("Rango de Edad")
plt.ylim(0, 1)
plt.legend(title="Género")
plt.tight_layout()
plt.show()

# -----------------------------
# 8. Distribución de Edad al Diagnóstico de ALL
# -----------------------------
df["Edad de diagnóstico ALL (años)"] = pd.to_numeric(df["Edad de diagnóstico ALL (años)"], errors='coerce')
plt.figure(figsize=(10, 6))
sns.kdeplot(df["Edad de diagnóstico ALL (años)"].dropna(), fill=True, color='purple', alpha=0.6, linewidth=2)
plt.title("Distribución de Edad al Diagnóstico de Leucemia Linfoblástica Aguda (ALL)")
plt.xlabel("Edad de diagnóstico (años)")
plt.ylabel("Densidad")
plt.grid(True)
plt.tight_layout()
plt.show()