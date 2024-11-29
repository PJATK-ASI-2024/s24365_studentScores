import os

from airflow import DAG
from _datetime import datetime

from airflow.operators.python import PythonOperator
from google.oauth2.service_account import Credentials
from sklearn.preprocessing import StandardScaler
import pandas as pd
import gspread

# Przy odpalaniu DAGa w Airflow dostawalam segmentation fault - to jest workaround,
# z tego co wyczytalam nie jest to wina kodu a interakcji Airflow/ARM i proxy
os.environ["no_proxy"] = "*"


def get_google_spreadsheet(worksheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file(
        "/Users/zosia/uczelnia/4_rok/1_sem/studentScores/secrets/asiprojekt-8ff60650e1f0.json"
    ).with_scopes(scope)

    client = gspread.authorize(credentials)
    return client.open("ASI_2024_Projekt").worksheet(worksheet_name)


def get_data_from_google_sheets():
    sheet = get_google_spreadsheet("Basic_train_data")
    return pd.DataFrame(sheet.get_all_records())


def clean_data(dataframe):
    dataframe = dataframe.replace("", pd.NA)

    for column in dataframe.columns:
        if dataframe[column].dtype == "object":
            dataframe[column].fillna(dataframe[column].mode()[0], inplace=True)
        else:
            dataframe[column].fillna(dataframe[column].mean(), inplace=True)

    return dataframe


def encode_categoricals(dataframe):
    ordinal_mappings = {
        "Parental_Involvement": {"Low": 0, "Medium": 1, "High": 2},
        "Access_to_Resources": {"Low": 0, "Medium": 1, "High": 2},
        "Motivation_Level": {"Low": 0, "Medium": 1, "High": 2},
        "Family_Income": {"Low": 0, "Medium": 1, "High": 2},
        "Teacher_Quality": {"Low": 0, "Medium": 1, "High": 2},
        "Peer_Influence": {"Negative": 0, "Neutral": 1, "Positive": 2}
    }

    binary_columns = [
        "Extracurricular_Activities",
        "Internet_Access",
        "Learning_Disabilities"
    ]

    categorical_columns = [
        "School_Type",
        "Parental_Education_Level",
        "Distance_from_Home",
        "Gender"
    ]

    for column, mapping in ordinal_mappings.items():
        dataframe[column] = dataframe[column].map(mapping)

    for column in binary_columns:
        dataframe[column] = dataframe[column].map({"Yes": 1, "No": 0})

    dataframe = pd.get_dummies(dataframe, columns=categorical_columns, drop_first=True, dtype=int)

    return dataframe


def standardize_data(dataframe):
    standard_scaler = StandardScaler()
    numerical_columns = dataframe.select_dtypes(include=["number"]).columns
    dataframe[numerical_columns] = standard_scaler.fit_transform(dataframe[numerical_columns])

    return dataframe


def prepare_data(**kwargs):
    dataframe = kwargs["ti"].xcom_pull(task_ids="get_data_from_google_sheets")
    dataframe = clean_data(dataframe)
    dataframe = encode_categoricals(dataframe)
    dataframe = standardize_data(dataframe)
    return dataframe


def save_data_locally(**kwargs):
    dataframe = kwargs["ti"].xcom_pull(task_ids="prepare_data")
    with open("/Users/zosia/uczelnia/4_rok/1_sem/studentScores/dags/processeddata/processed_data.txt", "w", encoding="utf-8") as file:
        file.write(dataframe.to_json())


def upload_data_to_google_sheets(**kwargs):
    dataframe = kwargs["ti"].xcom_pull(task_ids="prepare_data")
    sheet = get_google_spreadsheet("Basic_train_data_clean")
    sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


with DAG("process_data_dag",
         start_date=datetime(2023, 1, 1),
         schedule_interval=None,
         catchup=False
         ) as dag:
    get_data_from_google_sheets = PythonOperator(
        task_id="get_data_from_google_sheets",
        python_callable=get_data_from_google_sheets
    )

    prepare_data = PythonOperator(
        task_id="prepare_data",
        python_callable=prepare_data
    )

    upload_data_to_google_sheets = PythonOperator(
        task_id="upload_data_to_google_sheets",
        python_callable=upload_data_to_google_sheets
    )

    save_data_locally = PythonOperator(
        task_id="save_data_locally",
        python_callable=save_data_locally
    )

    get_data_from_google_sheets >> prepare_data >> save_data_locally >> upload_data_to_google_sheets
