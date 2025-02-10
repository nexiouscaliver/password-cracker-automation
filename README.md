# Real-Time Password Strength Analyzer Backend

## Overview
This project implements the backend for a Real-Time Password Strength Analyzer using Python, Flask, and Celery. The application analyzes the strength of passwords by attempting to reverse-engineer their hash values using various techniques.

## Features
- **Password Cracking Methods**:
  - **Basic Techniques**:  
    - Brute Force  
    - Dictionary Attack  
    - Rainbow Table Lookup  
  - **Advanced Techniques**:  
    - Hybrid Attack (combining dictionary words with brute force appending)  
    - Rule-based Attack (using password mutation rules)  
    - Mask Attack (targeted guesses based on patterns)  
    - Markov Chain Attack (probabilistic password generation)  
    - Phonetic Attack (guessing based on pronunciation patterns)  
    - Machine Learning Guessing (using ML models)  
    - Combinator Attack (combining multiple dictionaries)
- **Progress Tracking**: Real-time updates on:
  - Total techniques attempted
  - Techniques completed
  - Techniques remaining
  - Detailed results for each technique
- **Distributed Architecture**: Utilizes Celery with Redis for task distribution.
- **RESTful APIs**:
  - Submit a hash for analysis
  - Check task progress
  - Retrieve results
- **Security**: Rate limiting and secure handling of sensitive data.
- **Containerization**: Docker and Docker Compose for streamlined deployment.

## Project Structure
```
password-analyzer-backend/
├── api/
│   └── routes.py
├── services/
│   └── password_cracker.py  # Core module with advanced password cracking techniques.
├── tasks/
│   └── celery_tasks.py
├── utils/
│   └── hash_utils.py
├── tests/
│   ├── test_api.py
│   └── test_password_cracker.py   # Unit tests for the cracking methods.
├── .gitignore
├── app.py
├── celery_worker.py
├── config.py
├── Dockerfile
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Setup

### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Running Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/password-analyzer-backend.git
   cd password-analyzer-backend
   ```

2. **Build and run the containers:**
   ```bash
   docker-compose up --build
   ```
   The Flask API will be available at `http://localhost:5000`.

### Testing
Run tests using:
```bash
pytest
```

## API Endpoints

- **Submit Hash for Analysis**
  - **URL:** `/api/submit`
  - **Method:** POST
  - **Payload Example:**
    ```json
    {
      "hash": "5f4dcc3b5aa765d61d8327deb882cf99",
      "hash_algorithm": "md5",
      "method": "rainbow_table",
      "extra_data": {
          "custom_dictionary": ["password", "admin"],
          "custom_rules": {"a": "@"},
          "max_length": 8
      }
    }
    ```
  - **Note:** The `method` field can be any one of:
    - `"brute_force"`, `"dictionary_attack"`, `"rainbow_table"`, `"hybrid_attack"`, `"rule_based_attack"`, `"mask_attack"`, `"markov_chain_attack"`, `"phonetic_attack"`, `"ml_guessing"`, `"combinator_attack"`, or `"all"`.

- **Check Task Status**
  - **URL:** `/api/status/<task_id>`
  - **Method:** GET

- **Retrieve Task Result**
  - **URL:** `/api/result/<task_id>`
  - **Method:** GET

## Advanced Cracking Techniques
The core functionality in `services/password_cracker.py` supports advanced techniques:
- **Hybrid Attack:** Combines dictionary words with brute force (e.g., appending numbers).
- **Rule-based Attack:** Applies mutation rules (e.g., replacing "a" with "@") to dictionary words.
- **Mask Attack:** Uses targeted patterns (e.g., starts with 'A' and ends with '123').
- **Markov Chain Attack:** Generates guesses using probabilistic models.
- **Phonetic Attack:** Leverages similar-sounding guesses.
- **Machine Learning Guessing:** Uses (or simulates) ML models to predict likely passwords.
- **Combinator Attack:** Combines words from multiple dictionaries.

## Cloud Deployment
- Configure environment variables as needed.
- The project is ready for deployment on AWS, GCP, or Azure.

## License
MIT License ;)
```

---