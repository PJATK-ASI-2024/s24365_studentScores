import logging
import os

import numpy as np
import pandas as pd
from airflow import DAG
from _datetime import datetime

from airflow.operators.python import PythonOperator
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVR

# Przy odpalaniu DAGa w Airflow dostawalam segmentation fault - to jest workaround,
# z tego co wyczytalam nie jest to wina kodu a interakcji Airflow/ARM i proxy
os.environ["no_proxy"] = "*"


def train_model():
    dataframe = pd.read_json("/Users/zosia/uczelnia/4_rok/1_sem/studentScores/dags/processeddata/processed_data.txt",
                             encoding="utf-8")

    y = dataframe["Exam_Score"]
    x = dataframe.drop("Exam_Score", axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    model = LinearSVR(C=15.0, dual=True, epsilon=0.1, loss="epsilon_insensitive", tol=0.01, max_iter=50000)

    if hasattr(model, 'random_state'):
        setattr(model, 'random_state', 42)

    model.fit(x_train, y_train)
    results = model.predict(x_test)

    return model, results, y_test


def evaluate_model(y_test, results):
    r2 = r2_score(y_test, results)
    rmse = np.sqrt(mean_squared_error(y_test, results))
    mae = mean_absolute_error(y_test, results)

    data = "Wyniki modelu LinearSVC:\n"
    data += f"\tR²: {r2}\n"
    data += f"\tRMSE: {rmse}\n"
    data += f"\tMAE: {mae}\n"

    return data


def train_evaluate_model(**kwargs):
    model, results, y_test = train_model()
    data = evaluate_model(y_test, results)

    kwargs["ti"].xcom_push(key="data", value=data)


def save_results(**kwargs):
    results = kwargs["ti"].xcom_pull(key="data")

    with open("/Users/zosia/uczelnia/4_rok/1_sem/studentScores/dags/results/model_results.txt", "w",
              encoding="utf-8") as file:
        file.write(results)


with DAG("train_model_dag",
         start_date=datetime(2023, 1, 1),
         schedule_interval=None,
         catchup=False
         ) as dag:
    train_evaluate_model = PythonOperator(
        task_id="train_evaluate_model",
        python_callable=train_evaluate_model
    )

    save_results = PythonOperator(
        task_id="save_results",
        python_callable=save_results
    )

    train_evaluate_model >> save_results
