import os
import pandas as pd
import numpy as np
from obspy import read
from tqdm import tqdm


class ArrivalTime: 
    def __init__(self):
        """
        Initialize the ArrivalTime object with a given arrival time.

        Args:
            arrival_time (str): The arrival time in the format 'YYYY-MM-DDTHH:MM:SS'.
        """
        self.testing_data_path = '/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SeismicWaves/data/procesed/used_data/testing'
        self.test_csv_path = '/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SeismicWaves/data/raw/VT_P_training.csv'
    

    def process_arrival_times(self, data_path, data_name):
        """Procesa los tiempos de llegada para el conjunto de prueba."""
        # Leer CSV con tiempos de llegada de prueba
        test_df = pd.read_csv(self.test_csv_path)
        
        # Preparar DataFrame para almacenar tiempos de llegada
        test_times_df = pd.DataFrame(columns=['file', 'arrival_time'])
        
        print('Procesando tiempos de llegada del conjunto de prueba...')
        for _, row in tqdm(test_df.iterrows(), total=len(test_df)):
            file_id = row['archivo']
            mseed_file = f"{file_id:08d}.mseed"
            file_path = os.path.join(data_path, mseed_file)
            
            try:
                # Leer señal y obtener tiempo relativo
                st = read(file_path)
                absolute_p_time = row['lec_p']
                relative_p_time = absolute_p_time - st[0].stats.starttime.timestamp
                
                # Agregar al DataFrame
                test_times_df = pd.concat([test_times_df, pd.DataFrame([{
                    'file': mseed_file,
                    'arrival_time': relative_p_time
                }])], ignore_index=True)
                
            except Exception as e:
                continue
        
        # Guardar tiempos de llegada
        test_times_df.to_csv(os.path.join(self.features_path, f'{data_name}.csv'), index=False)
        np.save(os.path.join(self.features_path, data_name), test_times_df['arrival_time'].values)
        
        print(f'Tiempos de llegada guardados en {data_path}/{data_name}.csv')
        print(f'y {self.features_path}/test_arrival_times.npy')
        
        return test_times_df

