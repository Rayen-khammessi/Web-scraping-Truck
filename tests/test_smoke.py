from _future_ import annotations

import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(_file_).resolve().parent.parent


def load_module(relative_path: str, module_name: str):
    module_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


scrape_trucks = load_module("truck_project/scripts/scrape_trucks.py", "scrape_trucks")
clean_trucks = load_module("truck_project/scripts/clean_trucks.py", "clean_trucks")


def test_extract_year_from_registration_text() -> None:
    assert scrape_trucks.extract_year("10/2020") == 2020


def test_split_manufacturer_and_model_from_title() -> None:
    manufacturer, model = scrape_trucks.split_manufacturer_and_model(
        "SCANIA R450 6X2*4 RETARDER LED",
        "SCANIA",
    )

    assert manufacturer == "SCANIA"
    assert model == "R450 6X2*4 RETARDER LED"


def test_to_number_removes_units_and_symbols() -> None:
    assert clean_trucks.to_number("€46,450") == 46450.0
    assert clean_trucks.to_number("614,891 km") == 614891.0
