# ml-from-scratch

Progetto del corso di Machine Learning (3° anno): pipeline end-to-end che classifica il
**tipo di fondo stradale** (asfalto, pavé, sterrato) dalle vibrazioni misurate da sensori
inerziali, usando il dataset **PVS – Passive Vehicular Sensors** (Kaggle).

> README iniziale: verrà completato nella fase 12 (consegna).

## Struttura

```text
src/          codice riutilizzabile (config, caricamento, finestre, feature, modelli, valutazione)
notebooks/    notebook principale: progetto_pvs.ipynb
figures/      grafici generati dal notebook
data/raw/     dataset PVS scaricato da Kaggle (non versionato)
data/processed/  tabella delle finestre in formato parquet (non versionata)
```

## Setup dell'ambiente

Serve Python 3.12 (con 3.14 alcune dipendenze, come `numba` usato da `shap` e `umap-learn`,
potrebbero non avere ancora i wheel).

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dataset

Il dataset non è nel repository (troppo grande). Link:
https://www.kaggle.com/datasets/jefmenegazzo/pvs-passive-vehicular-sensors-datasets

Va scaricato in `data/raw/`, con una cartella per registrazione (`PVS1` … `PVS9`).

## Esecuzione

```bash
source .venv/bin/activate
jupyter lab notebooks/progetto_pvs.ipynb
```
