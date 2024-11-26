import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def get_data(file_path):
    logging.info("Odczytywanie danych z pliku")
    return pd.read_csv(file_path)


def clean_data(dataframe):
    logging.info("Czyszczenie danych")

    # Zamiana pustych danych na NA
    dataframe = dataframe.replace("", pd.NA)

    # Imputacja brakujących danych
    logging.info("Imputacja brakujących danych")
    for column in dataframe.columns:
        if dataframe[column].dtype == "object":
            dataframe[column].fillna(dataframe[column].mode()[0], inplace=True)
        else:
            dataframe[column].fillna(dataframe[column].mean(), inplace=True)

    return dataframe


def standardize_data(dataframe):
    logging.info("Standaryzacja danych")

    standard_scaler = StandardScaler()
    numerical_columns = dataframe.select_dtypes(include=["number"]).columns
    dataframe[numerical_columns] = standard_scaler.fit_transform(dataframe[numerical_columns])

    logging.info("Dane ustandaryzowane")
    return dataframe


def encode_categoricals(dataframe):
    logging.info("Transformowanie zmiennych kategorycznych")

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


def split_data(dataframe):
    logging.info("Usuwanie kolumny docelowej Exam_Score")
    y = dataframe["Exam_Score"]
    x = dataframe.drop("Exam_Score", axis=1)

    logging.info("Podział danych na zbiór testowy i treningowy")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    return x_train, x_test, y_train, y_test


def clean_split_data(file_path):
    dataframe = get_data(file_path)
    dataframe = clean_data(dataframe)
    dataframe = standardize_data(dataframe)
    dataframe = encode_categoricals(dataframe)
    x_train, x_test, y_train, y_test = split_data(dataframe)

    return x_train, x_test, y_train, y_test


def main(file_path):
    dataframe = clean_split_data(file_path)
    print(dataframe)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, encoding="utf-8")
    main("../dataset/StudentPerformanceFactors_basic.csv")
