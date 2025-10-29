#  Automotive NLP

An **NLP-powered feedback clustering and dynamic pricing system** for the automotive industry.  
This project analyzes customer complaints, clusters them by technical faults or car make/model, estimates repair costs dynamically, and helps service centers optimize profit margins.

Built with:
- **Python 3.10+**
- **Poetry** for dependency management
- **SQLAlchemy** + SQLite for storage
- **spaCy** + **TextBlob** for NLP
- **scikit-learn** for clustering
- **FastAPI** + **Typer** for API + CLI

---

## Features

- Collect structured **customer feedback** (text, car make, car model).
- Store data safely in **SQLite**.
- Run **NLP preprocessing** and **sentiment analysis**.
- **Cluster complaints** by technical faults (KMeans) or by make/model.
- **Dynamic repair cost suggestion** based on complaint frequency.
- Access via **CLI** or **REST API**.

---

##  Project Structure

```text
src/
 └── automotive_nlp/
     ├── __init__.py
     ├── cli.py              # Typer CLI
     ├── api.py              # FastAPI app
     ├── db/
     │    ├── __init__.py
     │    ├── models.py
     │    ├── schemas.py
     │    └── database.py
     ├── nlp/
     │    ├── __init__.py
     │    ├── preprocess.py
     │    └── sentiment.py
     ├── services/
     │    ├── feedback_service.py
     │    └── analysis_service.py
     └── utils/
          └── __init__.py
pyproject.toml
README.md
```

---

##  Installation

### 1. Install Poetry (Windows PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Then add Poetry to PATH:

```
%APPDATA%\Python\Scripts
```

Verify:

```powershell
poetry --version
```

### 2. Clone and install dependencies

```powershell
git clone https://github.com/NabeelKhan99/Automotive-NLP.git
cd automotive-nlp
poetry install
```

### 3. Activate virtual environment

```powershell
poetry shell
```

### 4. Install spaCy model

```powershell
python -m spacy download en_core_web_sm
```

---

##  Usage

### CLI (Typer)

Add feedback:

```powershell
poetry run automotive-nlp add-feedback --car-make Toyota --car-model Camry --text "Brakes squeak loudly"
```

Run analysis:

```powershell
poetry run automotive-nlp analyze --n-clusters 3
```

Cluster by make/model:

```powershell
poetry run automotive-nlp analyze --cluster-by-make True
```

---

### API (FastAPI)

Start the API:

```powershell
uvicorn automotive_nlp.api:app --host 0.0.0.0 --port 7860 --reload
```

Endpoints:
- `POST /feedback/` → Add feedback  
- `GET /feedbacks/` → List feedbacks  
- `GET /analyze/` → Run clustering  



---

## 🧪 Testing

Run tests with:

```powershell
poetry run pytest
```

---

## Example Output

CLI analysis:

```text
🔍 Analysis results:

Cluster: cluster_0  —  count: 3
  avg_sentiment: -0.65
  suggested_cost: $300.0
  examples:
    - Brakes squeak loudly when stopping
    - Brake pedal feels soft
    - Brakes grinding sound
```

---

## ☁️ Future: Cloud Deployment

Coming soon to your nearest cloud!!! 🚀☁️  
Stay tuned for Hugging Face Spaces, Railway, and other easy deployment options.  
