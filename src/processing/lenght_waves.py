import pandas as pd
from tqdm import tqdm
from obspy import read
import numpy as np
import os
import matplotlib.pyplot as plt

val_data_path = "/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SeismicWaves/data/procesed/used_data/training_augmented/val"
test_data_path = "/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SeismicWaves/data/procesed/used_data/testing"
train_data_path = "/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SeismicWaves/data/procesed/used_data/training_augmented/augmented"


def analyze_signal_lengths(data_path):
    """
    Analiza las longitudes de las señales en un directorio.

    Args:
        data_path: Ruta al directorio con archivos MSEED

    Returns:
        dict: Estadísticas de longitud de señales
    """
    lengths = []
    files_df = pd.read_csv(os.path.join(data_path, "feature_files.csv"))

    print(f"Analizando señales en {data_path}...")
    for file in tqdm(files_df["file"]):
        file_path = os.path.join(data_path, file)
        try:
            st = read(file_path)
            signal_length = len(st[0].data)
            lengths.append(signal_length)
        except Exception as e:
            print(f"Error procesando {file}: {str(e)}")
            continue

    stats = {
        "min_length": min(lengths),
        "max_length": max(lengths),
        "mean_length": np.mean(lengths),
        "median_length": np.median(lengths),
        "std_length": np.std(lengths),
        "p95_length": np.percentile(lengths, 95),
        "num_signals": len(lengths),
    }

    return stats, lengths


# Analizar cada conjunto de datos
train_stats, train_lengths = analyze_signal_lengths(train_data_path)
val_stats, val_lengths = analyze_signal_lengths(val_data_path)
test_stats, test_lengths = analyze_signal_lengths(test_data_path)

# Mostrar resultados
print("\nEstadísticas de longitud de señales:")
print("\nConjunto de entrenamiento:")
for key, value in train_stats.items():
    print(f"{key}: {value:.2f}")

print("\nConjunto de validación:")
for key, value in val_stats.items():
    print(f"{key}: {value:.2f}")

print("\nConjunto de prueba:")
for key, value in test_stats.items():
    print(f"{key}: {value:.2f}")

# Visualizar distribución de longitudes
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.hist(train_lengths, bins=50)
plt.title("Longitudes - Entrenamiento")
plt.xlabel("Longitud")
plt.ylabel("Frecuencia")

plt.subplot(132)
plt.hist(val_lengths, bins=50)
plt.title("Longitudes - Validación")
plt.xlabel("Longitud")

plt.subplot(133)
plt.hist(test_lengths, bins=50)
plt.title("Longitudes - Prueba")
plt.xlabel("Longitud")

plt.tight_layout()
plt.show()
