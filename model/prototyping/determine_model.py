import logging

from tpot import TPOTRegressor
from model.clean_split_data import clean_split_data


def tpot_evaluate(x_train, x_test, y_train, y_test):
    tpot = TPOTRegressor(
        generations=5,
        population_size=50,
        random_state=42,
        verbosity=2,
        scoring="r2",
    )

    logging.info("Szukanie najlepszego modelu z TPOT")
    tpot.fit(x_train, y_train)
    test_score = tpot.score(x_test, y_test)
    logging.info(f"Wynik modelu na danych testowych: {test_score}")

    logging.info("Generowanie najlepszego pipeline'u")
    tpot.export("best_pipeline.py")

    return tpot


def tpot_display_scores(tpot):
    pipelines = tpot.evaluated_individuals_
    unique_pipeline_types = set()

    for pipeline_name in pipelines.keys():
        pipeline_type = pipeline_name.split("(")[0]
        unique_pipeline_types.add(pipeline_type)

    pipeline_scores = {
        pipeline_type: max(
            pipelines[pipeline_name]["internal_cv_score"]
            for pipeline_name in pipelines
            if pipeline_name.startswith(pipeline_type)
        )
        for pipeline_type in unique_pipeline_types
    }

    top_pipelines = sorted(
        pipeline_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:3]

    logging.info("Najlepsze pipeline'y:")
    for rank, (pipeline_type, score) in enumerate(top_pipelines, start=1):
        print(f"Miejsce {rank}:")
        print(f"Rodzaj pipeline'u: {pipeline_type}")
        print(f"Wynik CV: {score}")
        print()


def main(file_path):
    x_train, x_test, y_train, y_test = clean_split_data(file_path)
    tpot = tpot_evaluate(x_train, x_test, y_train, y_test)
    tpot_display_scores(tpot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, encoding="utf-8")
    main("../../dataset/StudentPerformanceFactors_basic.csv")
