import json
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional
from functools import lru_cache

def _default_config_path() -> Path:
    return Path(__file__).resolve().parent / "config" / "qilong_mapping.json"


def _load_mapping_file(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Qilong mapping file not found: {path}")
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Mapping root must be a JSON object")
    return data


def _indexes_from_raw(data: Dict[str, Any]):
    stores = data.get("stores") or {}
    if not isinstance(stores, dict):
        raise ValueError("'stores' must be a JSON object")

    fuel_raw = data.get("fuel_items") or []
    if not isinstance(fuel_raw, list):
        raise ValueError("'fuel_items' must be a JSON array")
    fuel_item_map = {}
    for row in fuel_raw:
        key = (
            str(row.get("pos_store_id", "")),
            str(row.get("fuel_grade_id", "")),
            str(row.get("service_level_code", "")),
        )
        fuel_item_map[key] = str(row.get("item_id", ""))

    tender_raw = data.get("tender_types") or []
    if not isinstance(tender_raw, list):
        raise ValueError("'tender_types' must be a JSON array")
    tender_type_map = {}
    for row in tender_raw:
        key = (
            str(row.get("tender_code", "")),
            str(row.get("tender_subcode", "")),
        )
        tender_type_map[key] = str(row.get("tender_type_id", ""))

    return stores, fuel_item_map, tender_type_map


class QilongDataManager:
    """
    Loads store / fuel / tender mappings from config/qilong_mapping.json
    (or a path you pass in).
    """

    def __init__(self, config_path: Optional[Path] = None):
        path = Path(config_path) if config_path is not None else _default_config_path()
        raw = _load_mapping_file(path)
        self.store_map, self.fuel_item_map, self.tender_type_map = _indexes_from_raw(
            raw
        )


    def get_store_id(self, pos_store_id: str) -> str:
        store = self.store_map.get(str(pos_store_id), {})
        return store.get("store_id", f"ac4_{pos_store_id}" if pos_store_id else "")

    def get_channel_id(self, pos_store_id: str):
        store = self.store_map.get(str(pos_store_id), {})
        return store.get("channel_id", pos_store_id)

    def get_currency(self, pos_store_id: str) -> str:
        store = self.store_map.get(str(pos_store_id), {})
        return store.get("currency", "CAD")

    def get_inventory_location(self, pos_store_id: str) -> str:
        store = self.store_map.get(str(pos_store_id), {})
        return store.get("inventory_location_id", "Default")

    def get_oun(self, pos_store_id: str) -> str:
        store = self.store_map.get(str(pos_store_id), {})
        return store.get("oun", "")

    def get_csu_base_url(self, pos_store_id: str) -> str:
        store = self.store_map.get(str(pos_store_id), {})
        return store.get("csu_base_url", "")

    def build_transaction_id(self, shift_id: str, txn_id: str) -> str:
        if shift_id and txn_id:
            return f"{shift_id}-{txn_id}"
        return txn_id or ""

    def build_terminal_id(self, pos_store_id: str, register_id: str) -> str:
        if pos_store_id and register_id:
            return f"{pos_store_id}-{register_id}"
        return ""

    def calculate_unix_timestamp(self, receipt_date: str, receipt_time: str):
        if not receipt_date:
            return 0

        time_str = receipt_time or "00:00:00"
        try:
            dt = datetime.strptime(
                f"{receipt_date} {time_str}",
                "%Y-%m-%d %H:%M:%S",
            )
            return int(dt.timestamp())
        except ValueError:
            return 0

    def time_to_seconds(self, receipt_time: str) -> int:
        if not receipt_time:
            return 0

        try:
            h, m, s = map(int, receipt_time.split(":"))
            return h * 3600 + m * 60 + s
        except ValueError:
            return 0

    def get_fuel_item_id(self, pos_store_id: str, fuel_grade_id: str, service_level_code: str) -> str:
        key = (
            str(pos_store_id or ""),
            str(fuel_grade_id or ""),
            str(service_level_code or ""),
        )
        return self.fuel_item_map.get(key, "000006056")

    def get_tender_type_id(self, tender_code: str, tender_subcode: str) -> str:
        key = (str(tender_code or ""), str(tender_subcode or ""))
        return self.tender_type_map.get(key, str(tender_code or ""))

@lru_cache(maxsize=1)
def get_data_manager():
    return QilongDataManager()