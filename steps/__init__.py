from .registry import get_step, register

from .build_sales_order_header import SalesOrderHeaderStep
from .build_regular_sales_lines import RegularSalesLinesStep
from .build_charge_lines import ChargeLinesStep
from .build_fuel_sales_lines import FuelSalesLinesStep
from .build_tender_line import TenderLinesStep
from .build_shift_summary_header import ShiftSummaryHeaderStep


register("sales_order_header", SalesOrderHeaderStep)
register("regular_sales_lines", RegularSalesLinesStep)
register("charge_lines", ChargeLinesStep)
register("fuel_sales_lines", FuelSalesLinesStep)
register("tender_lines", TenderLinesStep)



register("shift_summary_header", ShiftSummaryHeaderStep)

TRANSACTION_STEP_ORDER = [
    "sales_order_header",
    "regular_sales_lines",
    "charge_lines",
    "fuel_sales_lines",
    "tender_lines",
]

__all__ = [
    "get_step",
    "register",
    "TRANSACTION_STEP_ORDER",
    "SalesOrderHeaderStep",

]