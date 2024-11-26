import logging

import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.svm import LinearSVR

from model.clean_split_data import clean_split_data


def train_model(x_train, y_train, x_test):
    logging.info("Trenowanie modelu LinearSVC")
    model = LinearSVR(C=15.0, dual=True, epsilon=0.1, loss="epsilon_insensitive", tol=0.01, max_iter=50000)

    if hasattr(model, 'random_state'):
        setattr(model, 'random_state', 42)

    model.fit(x_train, x_test)
    results = model.predict(y_train)

    return model, results


def evaluate_model(y_test, results):
    logging.info("Obliczanie wyniku modelu")
    r2 = r2_score(y_test, results)
    rmse = np.sqrt(mean_squared_error(y_test, results))
    mae = mean_absolute_error(y_test, results)

    logging.info("Wyniki modelu LinearSVC:")

    data = "Wyniki modelu LinearSVC:\n"
    data += f"\tR²: {r2}\n"
    data += f"\tRMSE: {rmse}\n"
    data += f"\tMAE: {mae}\n"

    return data


def save_results(data):
    logging.info("Zapisywanie wyników modelu do pliku")
    with open('linearsvc_score.txt', 'w', encoding="utf-8") as file:
        file.write(data)


def main(file_path):
    x_train, y_train, x_test, y_test = clean_split_data(file_path)
    model, results = train_model(x_train, y_train, x_test)
    data = evaluate_model(y_test, results)
    save_results(data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, encoding="utf-8")
    main("../../dataset/StudentPerformanceFactors_basic.csv")
