from airflow import DAG
from _datetime import datetime

from airflow.operators.python import PythonOperator
from google.oauth2.service_account import Credentials
from sklearn.model_selection import train_test_split
import gspread

from model.clean_split_data import get_data


def download_data(**kwargs):
    dataframe = get_data("../dataset/StudentPerformanceFactors.csv")
    return dataframe.to_json()


def split_data(**kwargs):
    dataframe = kwargs['ti']
    basic_train_data, additional_train_data = train_test_split(dataframe, test_size=0.3, random_state=42)

    return {
        "basic_train_data": basic_train_data.to_json(),
        "additional_train_data": additional_train_data.to_json()
    }


def upload_data(**kwargs):
    upload_data_to_google_sheets("Basic train data", kwargs['ti'].xcom_pull(key="basic_train_data"))
    upload_data_to_google_sheets("Additional train data", kwargs['ti'].xcom_pull(key="additional_train_data"))


def upload_data_to_google_sheets(sheet_name, dataframe):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file('/opt/airflow/dags/secret.json', scope=scope)
    client = gspread.authorize(credentials)

    sheet = client.open("ASI 2024 Projekt").worksheet()


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
