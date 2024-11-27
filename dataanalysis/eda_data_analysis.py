import logging
import io
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport


def read_data(file_path):
    logging.info("Wczytywanie danych")
    dataframe = pd.read_csv(file_path)

    return dataframe


def eda_analysis(dataframe):
    logging.info("Analiza danych")

    data = "------------------ Opis kolumn ------------------\n"
    buffer = io.StringIO()
    dataframe.info(buf=buffer)
    data += buffer.getvalue()
    data += "\n\n------------------ Analiza danych numerycznych ------------------\n"
    data += dataframe.describe().to_string()
    data += "\n\n------------------ Brakujące dane ------------------\n"
    missing_columns = dataframe.isnull().sum()
    data += missing_columns[missing_columns > 0].to_string()

    return data


def generate_plots(dataframe):
    logging.info("Generowanie wykresów")

    # Heatmapa
    logging.info("Generowanie heatmapy")
    sb.heatmap(dataframe.isnull())
    plt.title("Heatmapa brakujących danych")

    plt.savefig("../dataanalysis/diagrams/Heatmap.png")
    plt.close()

    # Zmienne kategoryczne
    logging.info("Generowanie wykresów opisujących zmienne kategoryczne")
    categorical_columns = dataframe.select_dtypes(include=["object", "category"]).columns

    for column in categorical_columns:
        plt.figure()
        dataframe[column].value_counts().plot(kind='bar')

        plt.title(f'Rozkład zmiennej {column}')
        plt.xlabel(column)
        plt.ylabel('Liczność')

        plt.savefig(f"../dataanalysis/diagrams/categoricalcolumns/{column}.png")

    # Macierz korelacji
    logging.info("Generowanie macierzy korelacji")
    numerical_columns = dataframe.select_dtypes(include=["number"]).columns
    corr_matrix = dataframe[numerical_columns].corr()

    plt.figure()
    sb.heatmap(corr_matrix, annot=True, fmt=".2f")
    plt.title("Macierz korelacji")

    plt.savefig("../dataanalysis/diagrams/Correlation_matrix.png")
    plt.close()


def save_results(data):
    logging.info("Zapisywanie wyników analizy EDA do pliku")
    with open('eda_analysis.txt', 'w', encoding="utf-8") as file:
        file.write(data)


def generate_report(dataframe):
    logging.info("Generowanie raportu pandas profiling")
    report = ProfileReport(dataframe, explorative=True)
    report.to_file('pandas_profiling_report.html')


def main(file_path):
    dataframe = read_data(file_path)
    data = eda_analysis(dataframe)
    save_results(data)
    generate_plots(dataframe)
    generate_report(dataframe)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        encoding='utf-8')
    main("../dataset/StudentPerformanceFactors_basic.csv")
