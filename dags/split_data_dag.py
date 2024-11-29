import os

from airflow import DAG
from _datetime import datetime

from airflow.operators.python import PythonOperator
from sklearn.model_selection import train_test_split
import pandas as pd

# Przy odpalaniu DAGa w Airflow dostawalam segmentation fault - to jest workaround,
# z tego co wyczytalam nie jest to wina kodu a interakcji Airflow/ARM i proxy
os.environ["no_proxy"] = "*"


def read_data():
    dataframe = pd.read_json("/Users/zosia/uczelnia/4_rok/1_sem/studentScores/dags/processeddata/processed_data.txt", encoding="utf-8")
    return dataframe


def split_data(**kwargs):
    dataframe = kwargs["ti"].xcom_pull(task_ids="read_data")

    y = dataframe["Exam_Score"]
    x = dataframe.drop("Exam_Score", axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    kwargs["ti"].xcom_push(key="x_train", value=x_train.to_json())
    kwargs["ti"].xcom_push(key="x_test", value=x_test.to_json())
    kwargs["ti"].xcom_push(key="y_train", value=y_train.to_json())
    kwargs["ti"].xcom_push(key="y_test", value=y_test.to_json())


def save_data_to_file(file_name, data):
    with open(f"/Users/zosia/uczelnia/4_rok/1_sem/studentScores/dags/processeddata/{file_name}", "w",
              encoding="utf-8") as file:
        file.write(data)


def save_data(**kwargs):
    x_train = kwargs["ti"].xcom_pull(key="x_train", task_ids="split_data")
    x_test = kwargs["ti"].xcom_pull(key="x_test", task_ids="split_data")
    y_train = kwargs["ti"].xcom_pull(key="y_train", task_ids="split_data")
    y_test = kwargs["ti"].xcom_pull(key="y_test", task_ids="split_data")

    save_data_to_file("x_train.txt", x_train)
    save_data_to_file("x_test.txt", x_test)
    save_data_to_file("y_train.txt", y_train)
    save_data_to_file("y_test.txt", y_test)


with DAG("split_data_dag",
         start_date=datetime(2023, 1, 1),
         schedule_interval=None,
         catchup=False
         ) as dag:
    read_data = PythonOperator(
        task_id="read_data",
        python_callable=read_data
    )

    split_data = PythonOperator(
        task_id="split_data",
        python_callable=split_data
    )

    save_data = PythonOperator(
        task_id="save_data",
        python_callable=save_data
    )

    read_data >> split_data >> save_data
