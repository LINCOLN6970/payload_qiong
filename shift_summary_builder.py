from typing import Any, Dict, Optional

try:
    from .transaction_builder import TransactionPayloadBuilder
    from .pos_extract import PosKeys, materialize_shift_bundle
    from .steps.build_shift_summary_header import ShiftSummaryHeaderStep
    from .models.shift_summary import ShiftSummaryHeader
    from .data_manager import get_data_manager
except ImportError:
    from transaction_builder import TransactionPayloadBuilder
    from pos_extract import PosKeys, materialize_shift_bundle
    from steps.build_shift_summary_header import ShiftSummaryHeaderStep
    from models.shift_summary import ShiftSummaryHeader
    from data_manager import get_data_manager


def _to_float(v, default=0.0):
    try:
        if v in (None, ""):
            return default
        return float(v)
    except (TypeError, ValueError):
        return default



class ShiftSummaryPayloadBuilder:
    def __init__(
        self,
        txn_builder: Optional[TransactionPayloadBuilder] = None,
        data_manager=None,
    ):
        dm = data_manager if data_manager is not None else get_data_manager()
        self.txn_builder = txn_builder or TransactionPayloadBuilder(
            data_manager=dm
        )
        self.skip_reason: Optional[str] = None
        self._header_step = ShiftSummaryHeaderStep(dm)

    def build_dict(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        self.skip_reason = None
        bundle = materialize_shift_bundle(data)
        if bundle is None:
            self.skip_reason = "not a shift batch"
            return None

        txns = bundle.get(PosKeys.TRANSACTIONS) or []
        if not txns:
            self.skip_reason = "no transactions in shift"
            return None

        shift_summary_data = bundle.get(PosKeys.SHIFT_SUMMARY) or {}

        header = ShiftSummaryHeader()
        header.BULLOCHSHIFTID = bundle.get(PosKeys.BULLOCH_SHIFT_ID) or ""
        header.STORELOCATIONID = bundle.get(PosKeys.STORE_LOCATION_ID) or ""
        header.BEGINDATE = bundle.get(PosKeys.BEGIN_DATE) or ""
        header.ENDDATE = bundle.get(PosKeys.END_DATE) or ""

        header.CUSTOMERCOUNT = shift_summary_data.get("CUSTOMERCOUNT")
        header.DRAWERMANUALLYOPENED = shift_summary_data.get("DRAWERMANUALLYOPENED")
        header.NUMBEROFCASHDRAWEROPENS = shift_summary_data.get(
            "NUMBEROFCASHDRAWEROPENS"
        )
        header.NUMBEROFUNDOKEYSHIT = shift_summary_data.get("NUMBEROFUNDOKEYSHIT")
        header.NUMBEROFCLEARKEYSHIT = shift_summary_data.get("NUMBEROFCLEARKEYSHIT")
        header.NUMBEROFVOIDTRANSACTIONS = shift_summary_data.get(
            "NUMBEROFVOIDTRANSACTIONS"
        )
        header.ENDOFSHIFT = shift_summary_data.get("ENDOFSHIFT")
        header.CASHIERID = shift_summary_data.get("CASHIERID")
        header.ENDOFDAY = shift_summary_data.get("ENDOFDAY")

        self._header_step.apply(bundle, header)

        batch_terminal = bundle.get(PosKeys.TERMINAL_ID_META) or ""
        batch_shift = bundle.get(PosKeys.CSU_SHIFT_ID_META) or ""

        built_payloads: Dict[str, Dict[str, Any]] = {}
        order_ids = []
        metrics = {
            "tx_count": 0,
            "safe_drop_count": 0,
            "safe_drop_total": 0.0,
            "sales_total": 0.0,
        }

        for txn in txns:
            txn_merged = dict(txn)
            txn_merged[PosKeys.TERMINAL_ID_META] = batch_terminal
            txn_merged[PosKeys.CSU_SHIFT_ID_META] = batch_shift

            p = self.txn_builder.build_dict(txn_merged)
            if not p:
                continue

            if p.get("dropAndDeclareTransaction"):
                transaction_id = p.get("dropAndDeclareTransaction", {}).get("Id")
            else:
                transaction_id = p.get("Id")

            if transaction_id:
                built_payloads[str(transaction_id)] = p
                order_ids.append(str(transaction_id))

            is_pump_test = bool(txn.get("pump_test_lines"))
            is_safe_drop = bool(p.get("dropAndDeclareTransaction"))

            if not is_pump_test and not is_safe_drop:
                metrics["tx_count"] += 1

            if is_safe_drop:
                metrics["safe_drop_count"] += 1
                td = p.get("dropAndDeclareTransaction", {}).get("TenderDetails") or []
                if td:
                    metrics["safe_drop_total"] += _to_float(td[0].get("Amount"))

            metrics["sales_total"] += _to_float(p.get("NetAmount"))

        if not built_payloads:
            self.skip_reason = "no valid transaction payloads"
            return None

        header.TransactionsCount = metrics["tx_count"]
        header.SafeDropCount = metrics["safe_drop_count"]
        header.SafeDropTotal = metrics["safe_drop_total"]
        header.TotalSales = metrics["sales_total"]
        header.OrderId = order_ids

        return {
            "ShiftSummary": header.to_dict(),
            "Payloads": built_payloads,
        }