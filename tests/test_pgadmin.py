import pandas as pd
from pandas.core.generic import FilePath
from pandas.testing import assert_frame_equal


ETALON_DATA = {
    'route_no': [
        "PG0063", "PG0063", "PG0063", "PG0063", "PG0225", "PG0225", "PG0225",
        "PG0225", "PG0158", "PG0158", "PG0274", "PG0274", "PG0321", "PG0045",
        "PG0045", "PG0045", "PG0045", "PG0414", "PG0112", "PG0112"
    ],
    'departure_airport': [
        "VKO", "VKO", "VKO", "VKO", "HGH", "HGH", "HGH", "HGH", "CLT",
        "CLT", "HYD", "HYD", "PRG", "PNQ", "PNQ", "PNQ", "PNQ", "PVG",
        "BOM", "BOM"
    ],
    'arrival_airport': [
        "LED", "LED", "LED", "LED", "PVG", "PVG", "PVG", "PVG", "JFK", "JFK",
        "DEL", "DEL", "FCO", "BOM", "BOM", "BOM", "BOM", "HND", "MAA", "MAA"
    ],
    'departure_airport_name': [
        "Внуково", "Внуково", "Внуково", "Внуково", "Сяошань", "Сяошань", "Сяошань",
        "Сяошань", "Шарлотт Дуглас", "Шарлотт Дуглас", "Раджив Ганди", "Раджив Ганди",
        "Вацлав Гавел", "Пуна", "Пуна", "Пуна", "Пуна", "Пудун", "Чхатрапати Шиваджи",
        "Чхатрапати Шиваджи"
    ],
    'actual_arrival': [
        "2025-11-30 23:55:34.369204+00", "2025-11-30 23:55:34.369204+00",
        "2025-11-30 23:55:34.369204+00", "2025-11-30 23:55:34.369204+00",
        "2025-11-30 23:54:55.815641+00", "2025-11-30 23:54:55.815641+00",
        "2025-11-30 23:54:55.815641+00", "2025-11-30 23:54:55.815641+00",
        "2025-11-30 23:38:28.331886+00", "2025-11-30 23:38:28.331886+00",
        "2025-11-30 23:37:18.031773+00", "2025-11-30 23:37:18.031773+00",
        "2025-11-30 23:30:17.447707+00", "2025-11-30 22:49:31.289294+00",
        "2025-11-30 22:49:31.289294+00", "2025-11-30 22:49:31.289294+00",
        "2025-11-30 22:49:31.289294+00", "2025-11-30 22:47:53.064747+00",
        "2025-11-30 22:07:36.156209+00", "2025-11-30 22:07:36.156209+00"
    ]
}


def execute_sql_query() -> pd.DataFrame:
    """Возвращает эталонные данные в виде DataFrame"""
    df = pd.DataFrame(ETALON_DATA)
    df.index = range(len(df))
    df.sort_index()
    return df


def test_csv_structure(csv_file: FilePath):
    """Проверяет структуру CSV-файла (столбцы и типы данных)"""
    df = pd.read_csv(csv_file)
    assert list(df.columns) == [
        'route_no',
        'departure_airport',
        'arrival_airport',
        'departure_airport_name',
        'actual_arrival'
    ]
    assert pd.api.types.is_string_dtype(df['route_no'])
    assert pd.api.types.is_string_dtype(df['departure_airport'])
    assert pd.api.types.is_string_dtype(df['arrival_airport'])
    assert pd.api.types.is_string_dtype(df['departure_airport_name'])


def test_sort_order(csv_file: FilePath):
    """Проверяет сортировку по actual_arrival (DESC)"""
    df = pd.read_csv(csv_file, parse_dates=['actual_arrival'])
    assert df['actual_arrival'].is_monotonic_decreasing, "Данные не отсортированы по убыванию даты"


def test_data_correctness(csv_file: FilePath):
    """Сравнивает данные CSV с результатом SQL-запроса"""
    df_csv = pd.read_csv(csv_file)
    df_db = execute_sql_query()
    assert_frame_equal(
        df_csv.reset_index(drop=True),
        df_db.reset_index(drop=True),
        check_dtype=False
    )
