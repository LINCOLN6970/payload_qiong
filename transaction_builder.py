try:
    from .base import BasePayloadBuilder
    from .models.sales_order import SalesOrderModel
    from .steps.build_sales_order_header import SalesOrderHeaderStep
    from .steps.build_regular_sales_lines import RegularSalesLinesStep
    from .steps.build_charge_lines import ChargeLinesStep
    from .steps.build_fuel_sales_lines import FuelSalesLinesStep
    from .steps.build_tender_line import TenderLinesStep
    from .pos_extract import PosKeys, materialize_transaction
    from .data_manager import get_data_manager
except ImportError:
    from base import BasePayloadBuilder
    from models.sales_order import SalesOrderModel
    from steps.build_sales_order_header import SalesOrderHeaderStep
    from steps.build_regular_sales_lines import RegularSalesLinesStep
    from steps.build_charge_lines import ChargeLinesStep
    from steps.build_fuel_sales_lines import FuelSalesLinesStep
    from steps.build_tender_line import TenderLinesStep
    from pos_extract import PosKeys, materialize_transaction
    from data_manager import get_data_manager


class TransactionPayloadBuilder(BasePayloadBuilder):
    def __init__(self, data_manager=None):
        dm = data_manager if data_manager is not None else get_data_manager()
        steps = [
            SalesOrderHeaderStep(dm),
            RegularSalesLinesStep(),
            ChargeLinesStep(),
            FuelSalesLinesStep(dm),
            TenderLinesStep(dm),
        ]
        super().__init__(SalesOrderModel, steps)

    def _build(self, data):
        txn = self._normalize_input(data)
        if txn is None:
            return None

        if not self._pre_build_validation(txn):
            return None

        payload = super()._build(txn)

        if not self._post_build_validation(payload):
            return None

        return payload

    def _normalize_input(self, data):
        txn = materialize_transaction(data)
        if txn is None:
            self.skip_reason = "no transaction data"
            return None
        return txn

    def _pre_build_validation(self, txn):
        processing_status = txn.get(PosKeys.PROCESSING_STATUS)
        if processing_status == "Skipped":
            self.skip_reason = "processing skipped"
            return False

        txn_id = txn.get(PosKeys.TRANSACTION_ID)
        if not txn_id:
            self.skip_reason = "missing transaction id"
            return False

        has_sales = bool(txn.get(PosKeys.REGULAR_LINES)) or bool(
            txn.get(PosKeys.FUEL_LINES)
        )
        has_tender = bool(txn.get(PosKeys.TENDER_LINES))

        if not has_sales and not has_tender:
            self.skip_reason = "empty transaction input"
            return False

        return True

    def _post_build_validation(self, payload):
        if payload is None:
            self.skip_reason = "no payload"
            return False

        has_sales_lines = bool(getattr(payload, "SalesLines", None))
        has_tender_lines = bool(getattr(payload, "TenderLines", None))
        has_income_expense = bool(getattr(payload, "IncomeExpenseLines", None))

        if (
            not has_sales_lines
            and not has_tender_lines
            and not has_income_expense
        ):
            self.skip_reason = "empty payload"
            return False

        return True
