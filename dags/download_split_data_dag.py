import os

from airflow import DAG
from _datetime import datetime

from airflow.operators.python import PythonOperator
from google.oauth2.service_account import Credentials
from sklearn.model_selection import train_test_split
import pandas as pd
import gspread

# Przy odpalaniu DAGa w Airflow dostawalam segmentation fault - to jest workaround,
# z tego co wyczytalam nie jest to wina kodu a interakcji bibliotek z ARM i proxy
os.environ["no_proxy"] = "*"


def get_data(file_path):
    return pd.read_csv(file_path)


def download_data(**kwargs):
    dataframe = get_data("/Users/zosia/uczelnia/4_rok/1_sem/studentScores/dags/StudentPerformanceFactors.csv")
    dataframe = dataframe.dropna()
    return dataframe.to_json()


def split_data(**kwargs):
    dataframe = pd.read_json(kwargs["ti"].xcom_pull(task_ids="download_data"))
    basic_train_data, additional_train_data = train_test_split(dataframe, test_size=0.3, random_state=42)

    kwargs["ti"].xcom_push(key="basic_train_data", value=basic_train_data.to_json())
    kwargs["ti"].xcom_push(key="additional_train_data", value=additional_train_data.to_json())


def upload_data(**kwargs):
    upload_data_to_google_sheets("Basic_train_data", kwargs["ti"]
                                 .xcom_pull(key="basic_train_data", task_ids="split_data"))
    upload_data_to_google_sheets("Additional_train_data", kwargs["ti"]
                                 .xcom_pull(key="additional_train_data", task_ids="split_data"))


def upload_data_to_google_sheets(worksheet_name, data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file(
        "/Users/zosia/uczelnia/4_rok/1_sem/studentScores/secrets/asiprojekt-8ff60650e1f0.json"
    ).with_scopes(scope)

    client = gspread.authorize(credentials)
    sheet = client.open("ASI_2024_Projekt").worksheet(worksheet_name)

    dataframe = pd.read_json(data)
    sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


with DAG("download_split_data_dag",
         start_date=datetime(2023, 1, 1),
         schedule_interval=None,
         catchup=False
         ) as dag:
    download_data = PythonOperator(
        task_id="download_data",
        python_callable=download_data
    )

    split_data = PythonOperator(
        task_id="split_data",
        python_callable=split_data,
        provide_context=True
    )

    upload_data = PythonOperator(
        task_id="upload_data",
        python_callable=upload_data
    )

    download_data >> split_data >> upload_data
