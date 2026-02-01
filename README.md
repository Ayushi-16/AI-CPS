# AI-based Cyber-Physical System for Bitcoin Price Forecasting

This repository provides an **end-to-end AI-based Cyber-Physical System (AI-CPS)** for
**Bitcoin (BTC–EUR) price forecasting**, realized as part of the course  
**“M. Grum: Advanced AI-based Application Systems”**  
at the **Junior Chair for Business Information Science, esp. AI-based Application Systems,
University of Potsdam**.

The system follows the **AI-CPS paradigm** by strictly separating **knowledge**, **activation**,
**learning**, and **code** into decentralized, containerized components that interact at runtime
via Docker and a shared external volume.

---

## Conceptual AI-CPS Architecture

The project follows the reference architecture of the AI-CPS platform:

- **Knowledge Base** – Persisted AI and OLS models representing system knowledge  
- **Activation Base** – Situational input data triggering model application  
- **Learning Base** – Training and validation datasets for model creation and evaluation  
- **Code Base** – Algorithmic routines for training, validation, and application  

These components are realized as **independent Docker images** and orchestrated
via **Docker Compose**, enabling **node-independent and reproducible deployment**.

---

## Project Overview

The AI-CPS forecasts Bitcoin closing prices (BTC–EUR) using two complementary approaches:

- **Artificial Neural Network (ANN)** – Captures non-linear market dynamics using deep learning  
- **Ordinary Least Squares (OLS)** – Statistical linear regression baseline for interpretability  

Both models are trained on the same dataset and evaluated on identical test data,
allowing a **direct performance comparison**.

---

## Dataset Description

**Source**  
Historical BTC–EUR price data scraped from  
https://finance.yahoo.com/quote/BTC-EUR/history/

**Features**
- Open – Opening price (EUR)
- High – Daily high price (EUR)
- Low – Daily low price (EUR)
- Volume – Trading volume

**Target**
- Close – Daily closing price (EUR)

**Time Span**
- 01.01.2025 – 01.01.2026

**Prepared Files**
- joint_data_collection.csv  
- training_data.csv (80%)  
- test_data.csv (20%)  
- activation_data.csv (single test instance)

---

## Model Performance Summary

| Model | Task | Performance |
|-----|-----|------------|
| ANN (TensorFlow/Keras) | Non-linear regression | R² ≈ 0.9765 |
| OLS (Statsmodels) | Linear regression | R² ≈ 0.9975 |

Diagnostic plots, learning curves, and scatter plots are stored as part of the learning base
and documented in the project report.

---

## Project Structure

```text
AI-CPS/
├── 📁 code/                             # Original scripts
│   ├── clean_data.ipynb
│   ├── LinearRegDiagnostic.py
│   ├── scrape_data.py
│   ├── train_ann.py
│   └── train_ols.py
├── 📁 data/                             # Raw and processed CSV datasets
│   ├── activation_data.csv
│   ├── bitcoin_stock_data.csv
│   ├── joint_data_collection.csv
│   ├── test_data.csv
│   └── training_data.csv
├── 📁 documentation/                    # Model performance and visualizations
│   ├── 📁 ANN/                          # ANN metrics, model, and plots
│   └── 📁 OLS/                          # OLS metrics, pickles, and diagnostic plots
├── 📁 images/                           # Decentralized Docker Base Images
│   ├── 📁 activationBase_bitcoin_forecast/
│   │   ├── activation_data.csv
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   └── README.md
│   ├── 📁 codeBase_bitcoin_forecast/
│   │   ├── activation_data.csv
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   ├── LinearRegDiagnostic.py
│   │   ├── train_ann.py
│   │   └── train_ols.py
│   ├── 📁 knowledgeBase_bitcoin_forecast/
│   │   ├── currentSolution.keras
│   │   ├── docker-compose.yml
│   │   └── Dockerfile
│   └── 📁 learningBase_bitcoin_forecast/
│       ├── 📁 train/
│       ├── 📁 validation/
│       ├── docker-compose.yml
│       └── Dockerfile
├── 📁 results/                          # Exported content from the ai_system volume
│   ├── 📁 activationBase/
│   ├── 📁 codeBase/
│   │   ├── 📁 data/
│   │   └── 📁 documentation/ANN/
│   ├── 📁 knowledgeBase/
│   └── 📁 images/learningBase_bitcoin_forecast/
├── .gitignore                           # Git exclusion rules
├── CITATION.cff                         # Citation metadata
├── docker-compose.yml                   # Main AI-CPS Orchestrator
├── LICENSE                              # AGPL-3.0 License
├── README.md                            # Project documentation
└── requirements.txt                     # Python dependencies

```
## Docker Based Deployment

### External Volume

All components communicate via the external Docker volume:

ai_system

Mounted as:

ai_system:/tmp

This enables **decoupled storage and runtime integration**, as required by the AI-CPS concept.

---

### Pull Required Images

docker pull ghoshayan/knowledgebase_bitcoin_forecast:latest  
docker pull ghoshayan/codebase_bitcoin_forecast:latest  
docker pull ghoshayan/learningbase_bitcoin_forecast:latest  
docker pull ayushi1612/activationbase_bitcoin_forecast:latest  

---

### Create External Volume

docker volume create ai_system

---

### Run AI-CPS Application (ANN + OLS)

docker compose up --pull always --remove-orphans

---

### Export Results from Volume

docker run --rm \
  -v ai_system:/data \
  -v $(pwd)/results:/export \
  busybox sh -c "cp -a /data/. /export/"

---

## Project Team

- Ayan Ghosh  
- Ayushi Garachh  

---

## Course Information

This project was created as part of the course  
**“M. Grum: Advanced AI-based Application Systems”**  
by the **Junior Chair for Business Information Science, esp. AI-based Application Systems**  
at the **University of Potsdam**.

---

## License

GNU Affero General Public License v3.0 (AGPL-3.0)

