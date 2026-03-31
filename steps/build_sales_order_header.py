try:
    from .base import DataManagerStep
    from ..models.common import ExtensionPropertyModel
    from ..pos_extract import PosKeys
except ImportError:
    from steps.base import DataManagerStep
    from models.common import ExtensionPropertyModel
    from pos_extract import PosKeys


class SalesOrderHeaderStep(DataManagerStep):
    @staticmethod
    def _to_float(value, default=0.0):
        try:
            if value in (None, ""):
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

    def apply(self, data, order):
        pos_shift_id = data.get(PosKeys.BULLOCH_SHIFT_ID)
        pos_store_id = data.get(PosKeys.STORE_LOCATION_ID)
        pos_txn_id = data.get(PosKeys.TRANSACTION_ID)
        receipt_date = data.get("RECEIPTDATE")
        receipt_time = data.get("RECEIPTTIME")
        business_date = data.get("BUSINESSDATE") or receipt_date
        register_id = data.get(PosKeys.REGISTER_ID, "1")
        cashier_id = data.get("CASHIERID", "")

        terminal_id = data.get(PosKeys.TERMINAL_ID_META) or self._dm.build_terminal_id(
            pos_store_id, register_id
        )
        csu_shift_id = data.get(PosKeys.CSU_SHIFT_ID_META) or pos_shift_id

        total_net_amount = self._to_float(data.get("TRANSACTIONTOTALNETAMOUNT"))
        total_gross_amount = self._to_float(data.get("TRANSACTIONTOTALGROSSAMOUNT"))
        total_grand_amount = self._to_float(data.get("TRANSACTIONTOTALGRANDAMOUNT"))
        total_tax_net_amount = self._to_float(data.get("TRANSACTIONTOTALTAXNETAMOUNT"))

        loyalty_txn_id = data.get("LPELOYALTYTRANSACTIONID", "")
        mobila_invoice_number = data.get("MOBILAINVOICENUMBER", "")
        event_type = data.get("EVENTTYPE", "")

        order.Id = self._dm.build_transaction_id(csu_shift_id, pos_txn_id)
        order.StoreId = self._dm.get_store_id(pos_store_id)
        order.ChannelId = self._dm.get_channel_id(pos_store_id)
        order.CurrencyCode = self._dm.get_currency(pos_store_id)
        order.InventoryLocationId = self._dm.get_inventory_location(pos_store_id)
        order.BusinessDate = business_date
        order.ShiftId = csu_shift_id
        order.ShiftTerminalId = terminal_id
        order.TerminalId = terminal_id
        order.TransactionDate = receipt_date
        order.TransactionTime = self._dm.calculate_unix_timestamp(
            receipt_date, receipt_time
        )

        order.GrossAmount = total_gross_amount
        order.NetAmount = total_net_amount
        order.TotalAmount = total_grand_amount
        order.AmountPaid = total_grand_amount

        order.NetAmountWithoutTax = total_net_amount
        order.NetAmountWithNoTax = total_net_amount
        order.NetAmountWithTax = total_grand_amount
        order.SubtotalAmount = total_gross_amount
        order.SubtotalAmountWithoutTax = total_gross_amount
        order.SubtotalSalesAmount = total_gross_amount

        order.ExtensionProperties.extend([
            ExtensionPropertyModel.create_string("BullochShiftId", pos_shift_id),
            ExtensionPropertyModel.create_string("StoreLocationId", pos_store_id),
            ExtensionPropertyModel.create_string("RegisterId", register_id),
            ExtensionPropertyModel.create_string("CashierId", cashier_id),
            ExtensionPropertyModel.create_string("ReceiptDate", receipt_date),
            ExtensionPropertyModel.create_int(
                "ReceiptTime",
                self._dm.time_to_seconds(receipt_time),
            ),
            ExtensionPropertyModel.create_decimal(
                "TransactionTotalNetAmount",
                total_net_amount,
            ),
            ExtensionPropertyModel.create_decimal(
                "TransactionTotalGrossAmount",
                total_gross_amount,
            ),
            ExtensionPropertyModel.create_decimal(
                "TransactionTotalTaxNetAmount",
                total_tax_net_amount,
            ),
            ExtensionPropertyModel.create_decimal(
                "TransactionTotalGrandAmount",
                total_grand_amount,
            ),
            ExtensionPropertyModel.create_string(
                "LpeLoyaltyTransactionId",
                loyalty_txn_id,
            ),
            ExtensionPropertyModel.create_string(
                "MobilaInvoiceNumber",
                mobila_invoice_number,
            ),
            ExtensionPropertyModel.create_string(
                "OUN",
                self._dm.get_oun(pos_store_id),
            ),
            ExtensionPropertyModel.create_string(
                "CsuBaseUrl",
                self._dm.get_csu_base_url(pos_store_id),
            ),
            ExtensionPropertyModel.create_string("EventType", event_type),
        ])
