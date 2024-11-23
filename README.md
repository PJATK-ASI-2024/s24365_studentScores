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

Wykorzystany dataset pochodzi z [Kaggle](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors/data).  
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

