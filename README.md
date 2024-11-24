# Wynik końcowy uczniów

## Problem biznesowy

Na wyniki uczniów w edukacji wpływa wiele czynników, nie tylko ich wrodzone zdolności. Bardzo
wiele zależy od ich sytuacji ekonomicznej i relacji w domu, a także życia społecznego wśród rówieśników.

Wiedząc, które z tych elementów mają najbardziej negatywny wpływ na ich wyniki, szkoła mogłaby wprowadzić
odpowiednie narzędzia zapobiegawcze i pomóc uczniom, zanim ich wyniki w nauce zaczną się pogarszać.

## Cel

Celem projektu jest wytrenowanie modelu, który będzie przewidywać, jaki wynik uzyska uczeń
o danych cechach, takich jak wiek, płeć, informacje o rodzicach, sytuacja ekonomiczna, miejsce zamieszkania,
życie towarzyskie itd.

Projekt pokaże, które czynniki najbardziej wpływają na niepowodzenie uczniów w edukacji. 
Może on pomóc np. szkołom, rodzicom czy psychologom we wcześniejszym zidentyfikowaniu, którzy uczniowie
potrzebują wsparcia.


## Informacje o źródle danych

Wykorzystany dataset pochodzi z [Kaggle](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors/data). \
Zawiera on 20 kolumn i 6607 wierszy.

### Kolumny w datasecie

Liczbowe:
- *hours_studied* - czas spędzony na nauce w ciągu tygodnia,
- *sleep_hours* - średni czas snu podczas każdej nocy,
- *previous_scores* - wyniki z poprzednich egzaminów,
- *tutoring_sessions* - ilość korepetycji, na które uczeń uczęszcza w ciągu miesiąca,
- *physical_activity* - średnia ilość godzin w tygodniu spędzona na aktywności fizycznej,
- *exam_score* - ostateczny wynik egzaminu;

Binarne - tak lub nie:
- *extracurricular_activities* - udział w zajęciach dodatkowych,
- *internet_access* - czy uczeń ma dostęp do internetu,
- *learning_disabilities* - czy uczeń ma specyficzne trudności w nauce;

Kategoryczne - wysoki, średni lub niski:
- *parental_involvement* - poziom zaangażowania rodziców ucznia w jego naukę,
- *access_to_resources* - dostęp do źródeł edukacji,
- *motivation_level* - poziom motywacji ucznia,
- *family_income* - poziom dochodu rodziny,
- *teacher_quality* - poziom kwalifikacji nauczycieli;

Inne:
- *attendance* - obecność ucznia na zajęciach (procent),
- *school_type* - rodzaj szkoły (publiczna/prywatna),
- *peer_influence* - wpływ otoczenia na ucznia (pozytywny/neutralny/negatywny),
- *parental_education_level* - najwyższy poziom wykształcenia wśród rodziców (magisterskie/wyższe/średnie),
- *distance_from_home* - odległość domu ucznia od szkoły (blisko/przeciętnie/daleko),
- *gender* - płeć ucznia (kobieta/mężczyzna).

### Uzasadnienie wyboru zbioru danych

Wybrałam ten dataset, bo porusza on istotną kwestię, która mnie interesuje - jak duży wpływ na edukację człowieka
mają czynniki od niego niezależne, i na ile potencjał danego ucznia może być ograniczony brakiem zasobów i zaangażowania rodzicow.

## Dobór modelu za pomocą narzędzia AutoML (TPOT)

Do ewaluacji najlepszego modelu wybrałam narzędzie TPOT. \
Po wykonaniu analizy na wyczyszczonych danych treningowych otrzymałam następujące wyniki:

### #1: LinearSVR (71,03%)

LinearSVR, czyli *Linear Support Vector Regressor*, działa dobrze na danych w moim projekcie, ponieważ np. cechy *hours_studied*,
*sleep_hours* i *attendance* są liniowo skorelowane ze zmienną docelową *exam_score*. \
Zmienne kategoryczne w moim przypadku nie wpływają tak mocno na zmienną docelową, jak numeryczne, więc ten model dobrze radzi sobie z przewidywaniem wyniku końcowego. \
Dodatkowo wprowadza on margines tolerancji, dzięki czemu jest mniej wrażliwy na odstające wartości, których jest dosyć
sporo w moich danych.

### #2: ElasticNetCV (70,98%)

ElasticNetCV, podobnie jak LinearSVR, dobrze radzi sobie z danymi z zależnościami liniowymi. Oprócz tego wprowadza on
regularyzację L1 i L2, które modyfikują wagi danych kolumn - dla nieistotnych wprowadzają niższe lub zerowe wagi. 
Moje dane zawierają wiele cech, które w różnym stopniu wpływają na skutecznośc modelu, dzięki czemu regularyzacja pomaga 
wyeliminować zbędne cechy i zapobiec przetrenowaniu modelu.

### #3: RidgeCV (70,97%)

RidgeCV jest częścią ElasticNetCV - używa regularyzacji L2, która modyfikuje wagi nieistotnych cech. Nie usuwa on całkiem
danych cech, ale nadaje im niski współczynnik, dzięki czemu zmniejsza ich potencjalnie negatywny wpływ na wynik.

## Wybrany model

Wybrałam model LinearSVR, ponieważ uzyskał on największy wynik, a także ze względu na jego umiejętność ignorowania wartości odstających. \
Logarytmizacja zmiennej docelowej mogłaby w podobny sposób zniwelować ich wpływ, ale chciałam uniknąć modyfikowania jej -
wybór modelu LinearSVR powazala mi zachować oryginalne dane, równocześnie nie poświęcając dokładności modelu.

Ostateczne parametry modelu, które zostały wyliczone przez TPOT:

    LinearSVR(input_matrix, C=15.0, dual=True, epsilon=0.1, loss=epsilon_insensitive, tol=0.01)

## Wyniki prototypu - model LinearSVC

Ostateczny wynik, jaki uzyskał mój prototyp:

	R²: 0.7274814514817167
	RMSE: 0.5268476553368098
	MAE: 0.11562836992452702

Biorąc pod uwagę duży zakres zmiennej docelowej Exam_Score, wynik mojego modelu jest dobry - jednak jest miejsce na poprawę jego
skuteczności.