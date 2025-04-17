# SismicWaves
GICO. Predictions P seismic waves.


## Structure 

```bash
cnn_wavelets_project/
├── data/                       ← Archivos .mseed, .csv, .npz, etc.
│   ├── raw/                    ← Datos originales
│   └── processed/              ← Datos filtrados, normalizados, recortados
│
├── notebooks/                 ← Pruebas y visualizaciones rápidas
│   └── 01_visualizacion.ipynb
│
├── src/                       ← Código fuente principal
│   ├── preprocessing/         ← Wavelets, normalización, padding, etc.
│   │   ├── wavelet_transform.py
│   │   ├── mseed_loader.py
│   │   └── utils.py
│   │
│   ├── dataset/               ← PyTorch Dataset o TF Data pipeline
│   │   └── seismo_dataset.py
│   │
│   ├── models/                ← Arquitecturas de redes
│   │   └── cnn_wavelet_model.py
│   │
│   └── training/              ← Ciclo de entrenamiento y evaluación
│       ├── train.py
│       └── evaluate.py
│
├── experiments/               ← Resultados, métricas, modelos guardados
│   ├── logs/
│   └── checkpoints/
│
├── requirements.txt           ← Librerías necesarias
├── config.yaml / config.py    ← Parámetros de entrenamiento
└── README.md                  ← Descripción del proyecto

```