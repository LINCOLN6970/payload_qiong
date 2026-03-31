"""QilongDataManager: load config/qilong_mapping.json and expose lookups.

Run from project root:
    cd path/to/payloads_qilong && pytest -q
"""

from pathlib import Path

import pytest

from data_manager import QilongDataManager, get_data_manager

# 与仓库里 config/qilong_mapping.json 一致时用这些期望值
_STORE = "33370"
_EXPECTED_STORE_ID = "ac4_33370"
_EXPECTED_CHANNEL_ID = 5637192654
_EXPECTED_CURRENCY = "CAD"
_EXPECTED_FUEL_KEY = (_STORE, "4", "self")
_EXPECTED_ITEM_ID = "000006056"
_EXPECTED_TENDER = ("2", "VISA", "2")  # code, subcode, type_id


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def test_config_file_exists(project_root):
    assert (project_root / "config" / "qilong_mapping.json").is_file()


def test_default_constructor_loads_mapping():
    dm = QilongDataManager()
    assert dm.get_store_id(_STORE) == _EXPECTED_STORE_ID
    assert dm.get_currency(_STORE) == _EXPECTED_CURRENCY
    assert dm.get_inventory_location(_STORE) == "Default"
    assert dm.get_oun(_STORE) == "00013588"
    assert dm.fuel_item_map[_EXPECTED_FUEL_KEY] == _EXPECTED_ITEM_ID
    assert dm.get_fuel_item_id(*_EXPECTED_FUEL_KEY) == _EXPECTED_ITEM_ID
    code, subcode, tid = _EXPECTED_TENDER
    assert dm.get_tender_type_id(code, subcode) == tid


def test_get_channel_id_preserves_numeric_type_from_json():
    dm = QilongDataManager()
    # JSON 里是整数则加载后仍是 int
    assert dm.get_channel_id(_STORE) == _EXPECTED_CHANNEL_ID


def test_unknown_store_falls_back_for_store_id():
    dm = QilongDataManager()
    assert dm.get_store_id("99999") == "ac4_99999"
    assert dm.get_channel_id("99999") == "99999"


def test_get_data_manager_returns_working_instance():
    dm = get_data_manager()
    assert isinstance(dm, QilongDataManager)
    assert dm.get_store_id(_STORE) == _EXPECTED_STORE_ID


def test_missing_config_path_raises(tmp_path):
    missing = tmp_path / "does_not_exist.json"
    with pytest.raises(FileNotFoundError):
        QilongDataManager(config_path=missing)