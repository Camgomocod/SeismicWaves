from obspy import read
import pandas as pd 
import matplotlib.pyplot as plt





def analyze_sampling_rates(data_directory):
    """
    Analiza la frecuencia de muestreo de todos los archivos mseed 
    del directorio 

    Args: 
        data_directory (str): Ruta al directorio con los archivos mseed
    """
    import os 
    from collections import Counter

    samplig_rates = []

    # Recorrer todos los archivos .mseed el el directorio
    for filename in os.listdir(data_directory):
        if filename.endswith('.mseed'):
            filepath = os.path.join(data_directory, filename)
            try:
                st = read(filepath)
                samplig_rates.append(st[0].stats.sampling_rate)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
    rates_count = Counter(samplig_rates)

    # Visualización
    plt.figure(figsize=(10, 6))
    plt.bar([
        str(rate) for rate in rates_count.keys()], 
        rates_count.values(), 
        color='skyblue'
    )
    plt.title('Distribución de Frecuencias de Muestreo')
    plt.xlabel('Frecuencia de Muestreo (Hz)')
    plt.ylabel('Número de Archivos')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show()

    # Estadisticás 
    print("\nEstadísticas de Frecuencias de Muestreo:")
    print(f"Frecuencia de muestreo mínima: {min(samplig_rates)} Hz")
    print(f"Total de archivos: {len(samplig_rates)}")
    for rate, count in rates_count.items():
        print(f"Frecuencia de muestreo {rate} Hz: {count} archivos")

# Uso de la función
data_dir = '/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SismicWaves/data/raw/test'
analyze_sampling_rates(data_dir)