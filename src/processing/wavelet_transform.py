import os
import pandas as pd
import numpy as np
from obspy import read
from tqdm import tqdm
import scipy.stats as stats
import matplotlib.pyplot as plt
import pywt

class Wavelets():
    def __init__(self):
        self.augmented_data_path = '/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SeismicWaves/data/procesed/used_data/training_augmented'
        self.features_path = '/mnt/c/Users/Usuario/Documents/Studies/GicoProject/SeismicWaves/data/procesed/features'
        
    def extract_wavelet_features(self, signal, wavelet='db4', level=4):
        """Extract statistical features from wavelet decomposition of a signal.
        Args:
            signal: Input signal array
            wavelet: Wavelet type to use
            level: Decomposition level
        Returns:
            array: Feature vector containing statistical measures"""
        # Perform wavelet decomposition
        coeffs = pywt.wavedec(signal, wavelet, level=level)
        
        # Initialize feature list
        features = []
        
        # Extract features from each coefficient level
        for coef in coeffs:
            # Statistical features
            features.extend([
                np.mean(coef),           # Mean
                np.std(coef),            # Standard deviation
                stats.skew(coef),        # Skewness
                stats.kurtosis(coef),    # Kurtosis
                np.percentile(coef, 75), # 75th percentile
                np.percentile(coef, 25), # 25th percentile
                np.max(coef),            # Maximum
                np.min(coef),            # Minimum
                np.sum(np.abs(coef)),    # L1 norm
                np.sqrt(np.sum(coef**2)),# L2 norm
                stats.entropy(np.abs(coef)), # Signal entropy
                np.median(np.abs(coef))  # Median absolute deviation
            ])
            
        return np.array(features)

    def process_seismic_files(self, data_path, arrival_times_csv):
        """Process all seismic files and extract wavelet features.
        Args:
            data_path: Path to directory containing MSEED files
            arrival_times_csv: Path to CSV with arrival times
        Returns:
            tuple: (features array, arrival times array, file names)"""
        # Read arrival times
        arrivals_df = pd.read_csv(arrival_times_csv)
        
        features_list = []
        arrival_times = []
        file_names = []
        
        print('Extracting wavelet features...')
        for _, row in tqdm(arrivals_df.iterrows(), total=len(arrivals_df)):
            file_path = os.path.join(data_path, row['augmented_file'])
            
            try:
                # Read seismic signal
                st = read(file_path)
                signal = st[0].data
                
                # Extract features
                features = self.extract_wavelet_features(signal)
                features_list.append(features)
                arrival_times.append(row['arrival_time'])
                file_names.append(row['augmented_file'])
                
            except Exception as e:
                print(f'Error processing {file_path}: {str(e)}')
                continue
        
        return np.array(features_list), np.array(arrival_times), file_names
