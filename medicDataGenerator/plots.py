import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter

# Cargar datos
df = pd.read_csv('consultas_pacientes.csv')


# Altura en base al Género
df["Género"] = df["Género"].str.strip().str.lower()
df = df[df["Género"].isin(["masculino", "femenino"])]
df["Altura (cm)"] = pd.to_numeric(df["Altura (cm)"], errors='coerce')
df = df.dropna(subset=["Altura (cm)"])
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df[df["Género"] == "masculino"], x="Altura (cm)", label="Masculino",
            color="#1f77b4", fill=True, alpha=0.5, linewidth=2)
sns.kdeplot(data=df[df["Género"] == "femenino"], x="Altura (cm)", label="Femenino",
            color="#e377c2", fill=True, alpha=0.5, linewidth=2)
media_m = df[df["Género"] == "masculino"]["Altura (cm)"].mean()
media_f = df[df["Género"] == "femenino"]["Altura (cm)"].mean()
plt.axvline(media_m, color="#1f77b4", linestyle='--', linewidth=1)
plt.axvline(media_f, color="#e377c2", linestyle='--', linewidth=1)
plt.xlabel("Altura (cm)")
plt.ylabel("Densidad")
plt.title("Distribución de Altura por Género")
plt.legend(title="Género")
plt.tight_layout()
plt.show()


# Tipo de sangre
tipos_sangre = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
conteo = Counter(df['Tipo de Sangre'])
total = sum(conteo.values())
frecuencias_observadas = [(conteo.get(tipo, 0) / total) * 100 for tipo in tipos_sangre]
colores = ['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0', '#00BCD4', '#795548', '#607D8B']
plt.figure(figsize=(10, 6))
barras = plt.bar(tipos_sangre, frecuencias_observadas, color=colores)
for barra, valor in zip(barras, frecuencias_observadas):
    plt.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.5,
             f'{valor:.1f}%', ha='center', va='bottom', fontsize=10)
plt.title('Distribución Observada de Tipos de Sangre', fontsize=14)
plt.ylabel('Porcentaje (%)', fontsize=12)
plt.xlabel('Tipo de Sangre', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.ylim(0, max(frecuencias_observadas) + 5)
plt.tight_layout()
plt.show()


# Dispersión Pesos por Edad
plt.figure(figsize=(10,6))
plt.scatter(df['Edad'], df['Peso (kg)'], alpha=0.6, edgecolor='k')
plt.title('Dispersión de Peso vs Edad')
plt.xlabel('Edad (años)')
plt.ylabel('Peso (kg)')
plt.grid(True)
plt.show()


# Fumador en base a genero
df["Género"] = df["Género"].str.strip().str.lower()
df = df[df["Género"].isin(["masculino", "femenino"])]
df_fumadores = df[df["Fumador"] == "Sí"]
conteo_fumadores = df_fumadores["Género"].value_counts()
colores = ['#1f77b4', '#e377c2']
plt.figure(figsize=(7,7))
plt.pie(conteo_fumadores, labels=conteo_fumadores.index.str.capitalize(),
        autopct='%1.1f%%', startangle=90, colors=colores, textprops={'fontsize': 14})
plt.title("Distribución de fumadores por género", fontsize=16)
plt.axis('equal')  # Para que la torta sea un círculo
plt.show()


# Fumador en base a edad
plt.figure(figsize=(10, 6))
sns.kdeplot(df[df["Fumador"] == "Sí"]["Edad"], label="Fumadores", color="red", fill=True, alpha=0.5)
plt.title("Distribución de Edad según Fumador / No Fumador")
plt.xlabel("Edad")
plt.ylabel("Densidad")
plt.legend()
plt.tight_layout()
plt.show()


# Frecuencias
variables = [
    "Frecuencia Cardíaca (lpm)",
    "Presión Sistólica",
    "Frecuencia Respiratoria (rpm)"
]
def graficar_variable(var):
    plt.figure(figsize=(10, 6))
    stats = df.groupby('Edad')[var].mean().reset_index()
    sns.barplot(x='Edad', y=var, data=stats, palette="Set2")
    plt.title(f'Media y desviación estándar de {var} por Edad')
    plt.ylabel(var)
    plt.xlabel('Edad')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
for var in variables:
    graficar_variable(var)