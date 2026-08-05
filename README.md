\# Customer Churn Prediction Platform



An end-to-end machine learning platform for predicting customer churn using \*\*Python, LightGBM, FastAPI, Streamlit, and Docker\*\*.



The project takes customer information, processes it through a trained machine learning pipeline, and returns a churn prediction with probability and a configurable decision threshold.



\## 🚀 Features



\* Customer churn prediction using LightGBM

\* Probability-based churn prediction

\* Configurable classification threshold

\* Interactive Streamlit dashboard

\* REST API built with FastAPI

\* Automatic API documentation with Swagger UI

\* Dockerized application

\* Production-oriented project structure

\* Health-check endpoint

\* Input validation with Pydantic

\* OpenAPI specification



\## 🧠 Machine Learning



The platform uses a trained \*\*LightGBM classifier\*\* to predict whether a customer is likely to churn.



The API returns:



\* `churn\_prediction` — binary prediction

\* `churn\_label` — `Yes` or `No`

\* `churn\_probability` — predicted churn probability

\* `threshold` — classification threshold used for the prediction



Example response:



```json

{

&#x20; "churn\_prediction": 1,

&#x20; "churn\_label": "Yes",

&#x20; "churn\_probability": 0.3103,

&#x20; "threshold": 0.3

}

```



\## 🏗️ Project Structure



```text

Customer-Churn-Prediction-Platform/

│

├── api/

│   └── main.py

│

├── config/

│

├── data/

│   └── raw/

│

├── models/

│

├── notebooks/

│

├── src/

│   └── prediction.py

│

├── streamlit\_app/

│   └── app.py

│

├── tests/

│

├── .dockerignore

├── .gitignore

├── Dockerfile

├── requirements.txt

└── README.md

```



\## 🛠️ Tech Stack



\### Programming \& Data Science



\* Python 3.12

\* Pandas

\* NumPy

\* Scikit-learn

\* SciPy



\### Machine Learning



\* LightGBM

\* XGBoost

\* CatBoost



\### Application



\* Streamlit

\* FastAPI

\* Uvicorn

\* Pydantic



\### Deployment



\* Docker

\* Docker Desktop

\* WSL 2



\## 🔌 API



The FastAPI application provides the following endpoints:



| Method | Endpoint   | Description            |

| ------ | ---------- | ---------------------- |

| GET    | `/`        | API root               |

| GET    | `/health`  | Health check           |

| POST   | `/predict` | Predict customer churn |



\### Health Check



```text

GET http://127.0.0.1:8000/health

```



Example:



```json

{

&#x20; "status": "healthy"

}

```



\### Swagger Documentation



When the API is running, interactive documentation is available at:



```text

http://127.0.0.1:8000/docs

```



OpenAPI specification:



```text

http://127.0.0.1:8000/openapi.json

```



\## ▶️ Run Locally



Create and activate the virtual environment:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



\### Start FastAPI



```powershell

uvicorn api.main:app --host 127.0.0.1 --port 8000

```



API documentation:



```text

http://127.0.0.1:8000/docs

```



\### Start Streamlit



In another terminal:



```powershell

.\\.venv\\Scripts\\Activate.ps1

streamlit run streamlit\_app/app.py

```



The dashboard will normally be available at:



```text

http://localhost:8501

```



\## 🐳 Run with Docker



Build the Docker image:



```powershell

docker build -t customer-churn-platform:latest .

```



Run the application:



```powershell

docker run -d --name customer-churn-app -p 8501:8501 customer-churn-platform:latest

```



Check the running container:



```powershell

docker ps

```



Open:



```text

http://localhost:8501

```



The Docker image includes `libgomp1`, which is required by LightGBM/OpenMP in the slim Python image.



\## 🧪 Validation



The application has been tested successfully with:



\* Docker image build

\* LightGBM import inside Docker

\* All major ML library imports inside Docker

\* Streamlit dashboard

\* FastAPI startup

\* `/docs` endpoint

\* `/openapi.json` endpoint

\* `/health` endpoint

\* `/predict` endpoint

\* Customer input validation

\* Successful churn prediction response



Example API response:



```text

HTTP 200 OK

```



\## 📊 Example Prediction



For a sample customer, the API returned:



```json

{

&#x20; "churn\_prediction": 1,

&#x20; "churn\_label": "Yes",

&#x20; "churn\_probability": 0.3103,

&#x20; "threshold": 0.3

}

```



Because the predicted probability is above the configured threshold of `0.3`, the customer is classified as likely to churn.



\## 🎯 Project Goal



The goal of this project is to demonstrate an end-to-end machine learning workflow:



```text

Customer Data

&#x20;     ↓

Data Processing

&#x20;     ↓

Feature Preparation

&#x20;     ↓

LightGBM Model

&#x20;     ↓

Churn Probability

&#x20;     ↓

Decision Threshold

&#x20;     ↓

Churn Prediction

&#x20;     ↓

Streamlit Dashboard / FastAPI

```



\## 📌 Future Improvements



Potential future enhancements include:



\* SHAP-based model explainability

\* Batch prediction endpoint

\* Authentication and API security

\* Automated model retraining

\* CI/CD pipeline

\* Automated testing

\* Model monitoring

\* Prediction logging

\* Cloud deployment

\* Production database integration



\## 👨‍💻 Author



\*\*Muzamil Rasul\*\*



Machine Learning \& Data Science | Python | Forecasting | Churn Prediction | AI Agents



