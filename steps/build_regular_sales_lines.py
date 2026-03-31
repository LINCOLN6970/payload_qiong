try:
    from .base import PayloadStep
    from ..models.sales_line import SalesLineModel
    from ..models.common import ExtensionPropertyModel
    from ..pos_extract import PosKeys, LineKeys
    from ..utils.to_float import to_float
except ImportError:
    from steps.base import PayloadStep
    from models.sales_line import SalesLineModel
    from models.common import ExtensionPropertyModel
    from pos_extract import PosKeys, LineKeys
    from utils.to_float import to_float


class RegularSalesLinesStep(PayloadStep):
    DEFAULT_PRODUCT_ID = 0

    def apply(self, data, order):
        regular_lines = data.get(PosKeys.REGULAR_LINES) or []

        for raw in regular_lines:
            line = SalesLineModel()

            sales_qty = to_float(raw.get(LineKeys.SALES_QUANTITY), 1.0)
            sales_amount = to_float(raw.get(LineKeys.SALES_AMOUNT))
            regular_price = to_float(raw.get(LineKeys.REGULAR_SELL_PRICE))
            actual_sales_price = to_float(raw.get(LineKeys.ACTUAL_SALES_PRICE))

            item_id = raw.get(LineKeys.INVENTORY_ITEM_ID, "")
            pos_code = raw.get(LineKeys.POS_CODE, "")
            pos_code_format = raw.get(LineKeys.POS_CODE_FORMAT, "")
            pos_code_modifier = raw.get(LineKeys.POS_CODE_MODIFIER, "")
            item_type_code = raw.get(LineKeys.ITEM_TYPE_CODE, "")
            item_type_subcode = raw.get(LineKeys.ITEM_TYPE_SUBCODE, "")
            merchandise_code = raw.get(LineKeys.MERCHANDISE_CODE, "")
            entry_method = raw.get(LineKeys.ENTRY_METHOD, "")
            price_override_reason = raw.get(LineKeys.PRICE_OVERRIDE_REASON, "")
            price_override_price = raw.get(LineKeys.PRICE_OVERRIDE_PRICE)

            line.LineNumber = len(order.SalesLines) + 1
            line.Description = raw.get(LineKeys.DESCRIPTION, "")
            line.ProductId = self.DEFAULT_PRODUCT_ID
            line.ListingId = self.DEFAULT_PRODUCT_ID
            line.ItemId = item_id
            line.Quantity = sales_qty
            line.QuantityOrdered = sales_qty
            line.Price = actual_sales_price if actual_sales_price else regular_price
            line.OriginalPrice = regular_price
            line.TotalAmount = sales_amount
            line.NetAmount = sales_amount
            line.NetAmountWithoutTax = sales_amount
            line.GrossAmount = sales_amount
            line.NetPrice = -sales_amount
            line.ReturnChannelId = order.ChannelId
            line.IsPriceOverridden = bool(
                price_override_reason or price_override_price
            )

            line.ExtensionProperties.extend([
                ExtensionPropertyModel.create_int("LineType", 1),
                ExtensionPropertyModel.create_string("EntryMethod", entry_method),
                ExtensionPropertyModel.create_string("POSCode", pos_code),
                ExtensionPropertyModel.create_string("POSCodeFormat", pos_code_format),
                ExtensionPropertyModel.create_string("POSCodeModifier", pos_code_modifier),
                ExtensionPropertyModel.create_string("ItemTypeCode", item_type_code),
                ExtensionPropertyModel.create_string(
                    "ItemTypeSubCode", item_type_subcode
                ),
                ExtensionPropertyModel.create_string(
                    "MerchandiseCode", merchandise_code
                ),
                ExtensionPropertyModel.create_decimal(
                    "ActualSalesPrice", actual_sales_price
                ),
                ExtensionPropertyModel.create_string(
                    "PriceOverrideReason", price_override_reason
                ),
            ])

            order.SalesLines.append(line.to_dict())
