"""Qilong extract shape: field names and single-transaction normalization."""

from typing import Any, Dict, Optional


class PosKeys:
    """Top-level transaction / wrapper keys from _pos_data.json."""

    TRANSACTIONS = "Transactions"
    REGULAR_LINES = "regular_lines"
    FUEL_LINES = "fuel_lines"
    TENDER_LINES = "tender_lines"
    CHARGE_LINES = "charge_lines"

    STORE_LOCATION_ID = "STORELOCATIONID"
    REGISTER_ID = "REGISTERID"
    BULLOCH_SHIFT_ID = "BULLOCHSHIFTID"
    TRANSACTION_ID = "TRANSACTIONID"
    PROCESSING_STATUS = "ProcessingStatus"

    TERMINAL_ID_META = "_terminal_id"
    CSU_SHIFT_ID_META = "_csu_shift_id"

    # --- 加到 PosKeys 类里（推荐）---
    SHIFT_SUMMARY = "ShiftSummary"
    BEGIN_DATE = "BEGINDATE"
    END_DATE = "ENDDATE"
    BEGIN_TIME = "BEGINTIME"
    END_TIME = "ENDTIME"


class LineKeys:
    """Shared POS line / tender field names (XML-style UPPERCASE)."""

    SALES_QUANTITY = "SALESQUANTITY"
    SALES_AMOUNT = "SALESAMOUNT"
    REGULAR_SELL_PRICE = "REGULARSELLPRICE"
    ACTUAL_SALES_PRICE = "ACTUALSALESPRICE"
    DESCRIPTION = "DESCRIPTION"
    ENTRY_METHOD = "ENTRYMETHOD"
    INVENTORY_ITEM_ID = "INVENTORYITEMID"
    POS_CODE = "POSCODE"
    POS_CODE_FORMAT = "POSCODEFORMAT"
    POS_CODE_MODIFIER = "POSCODEMODIFIER"
    ITEM_TYPE_CODE = "ITEMTYPECODE"
    ITEM_TYPE_SUBCODE = "ITEMTYPESUBCODE"
    MERCHANDISE_CODE = "MERCHANDISECODE"
    PRICE_OVERRIDE_REASON = "PRICEOVERRIDEREASON"
    PRICE_OVERRIDE_PRICE = "PRICEOVERRIDEPRICE"
    FUEL_GRADE_ID = "FUELGRADEID"
    SERVICE_LEVEL_CODE = "SERVICELEVELCODE"
    FUEL_POSITION_ID = "FUELPOSITIONID"
    TENDER_AMOUNT = "TENDERAMOUNT"
    TENDER_CODE = "TENDERCODE"
    TENDER_SUBCODE = "TENDERSUBCODE"
    ACCOUNT_ID = "ACCOUNTID"
    FEE_ID = "FEEID"
    TAX_LEVEL_ID = "TAXLEVELID"
    FEE_AMOUNT = "FEEAMOUNT"
    TAX_COLLECTED_AMOUNT = "TAXCOLLECTEDAMOUNT"


def materialize_transaction(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    From a full _pos_data bundle or a single-transaction dict, return one
    transaction dict with terminal / shift metadata defaulted.

    Returns None when the bundle contains ``Transactions`` but it is empty.
    """
    if PosKeys.TRANSACTIONS in data:
        txns = data.get(PosKeys.TRANSACTIONS) or []
        if not txns:
            return None
        txn = dict(txns[0])
    else:
        txn = dict(data)

    store_id = txn.get(PosKeys.STORE_LOCATION_ID, "") or ""
    register_id = txn.get(PosKeys.REGISTER_ID, "1") or "1"
    bulloch_shift_id = txn.get(PosKeys.BULLOCH_SHIFT_ID, "") or ""

    txn.setdefault(
        PosKeys.TERMINAL_ID_META,
        f"{store_id}-{register_id}" if store_id and register_id else "",
    )
    txn.setdefault(PosKeys.CSU_SHIFT_ID_META, bulloch_shift_id)

    return txn


def is_shift_batch(data: Dict[str, Any]) -> bool:
    """True for shift XML extract (has ShiftSummary + Transactions list)."""
    return PosKeys.SHIFT_SUMMARY in data and isinstance(
        data.get(PosKeys.TRANSACTIONS), list
    )


def materialize_shift_bundle(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Copy shift root and set batch-level _terminal_id / _csu_shift_id for injection
    into each transaction (mirrors formal shift builder).
    Returns None if not a shift batch shape.
    """
    if not is_shift_batch(data):
        return None

    bundle = dict(data)
    store_id = bundle.get(PosKeys.STORE_LOCATION_ID, "") or ""
    txns = bundle.get(PosKeys.TRANSACTIONS) or []
    register_id = "1"
    if txns:
        register_id = (txns[0].get(PosKeys.REGISTER_ID) or "1") or "1"
    bulloch = bundle.get(PosKeys.BULLOCH_SHIFT_ID, "") or ""

    bundle.setdefault(
        PosKeys.TERMINAL_ID_META,
        f"{store_id}-{register_id}" if store_id and register_id else "",
    )
    bundle.setdefault(PosKeys.CSU_SHIFT_ID_META, bulloch)
    return bundle