try:
    from .base import DataManagerStep
    from ..models.sales_line import SalesLineModel
    from ..models.common import ExtensionPropertyModel
    from ..pos_extract import PosKeys, LineKeys
    from ..utils.to_float import to_float
except ImportError:
    from steps.base import DataManagerStep
    from models.sales_line import SalesLineModel
    from models.common import ExtensionPropertyModel
    from pos_extract import PosKeys, LineKeys
    from utils.to_float import to_float


class FuelSalesLinesStep(DataManagerStep):
    DEFAULT_PRODUCT_ID = 5637146394

    def apply(self, data, order):
        fuel_lines = data.get(PosKeys.FUEL_LINES) or []

        for raw in fuel_lines:
            line = SalesLineModel()

            sales_qty = to_float(raw.get(LineKeys.SALES_QUANTITY))
            sales_amount = to_float(raw.get(LineKeys.SALES_AMOUNT))
            regular_price = to_float(raw.get(LineKeys.REGULAR_SELL_PRICE))
            actual_sales_price = to_float(raw.get(LineKeys.ACTUAL_SALES_PRICE))

            fuel_grade_id = raw.get(LineKeys.FUEL_GRADE_ID, "")
            service_level_code = raw.get(LineKeys.SERVICE_LEVEL_CODE, "")
            fuel_position_id = raw.get(LineKeys.FUEL_POSITION_ID, "")
            pos_store_id = data.get(PosKeys.STORE_LOCATION_ID, "")

            line.LineNumber = len(order.SalesLines) + 1
            line.Description = raw.get(LineKeys.DESCRIPTION, "")
            line.ProductId = self.DEFAULT_PRODUCT_ID
            line.ListingId = self.DEFAULT_PRODUCT_ID
            line.ItemId = self._dm.get_fuel_item_id(
                pos_store_id,
                fuel_grade_id,
                service_level_code,
            )
            line.Quantity = sales_qty
            line.QuantityOrdered = sales_qty
            line.Price = regular_price
            line.OriginalPrice = regular_price
            line.TotalAmount = sales_amount
            line.NetAmount = sales_amount
            line.NetAmountWithoutTax = sales_amount
            line.GrossAmount = sales_amount
            line.NetPrice = -sales_amount
            line.ReturnChannelId = order.ChannelId

            line.ExtensionProperties.extend([
                ExtensionPropertyModel.create_string("FuelGradeId", fuel_grade_id),
                ExtensionPropertyModel.create_string("FuelPositionId", fuel_position_id),
                ExtensionPropertyModel.create_string(
                    "ServiceLevelCode", service_level_code
                ),
                ExtensionPropertyModel.create_decimal(
                    "ActualSalesPrice", actual_sales_price
                ),
                ExtensionPropertyModel.create_string(
                    "EntryMethod", raw.get(LineKeys.ENTRY_METHOD, "")
                ),
                ExtensionPropertyModel.create_int("LineType", 4),
            ])

            order.SalesLines.append(line.to_dict())
