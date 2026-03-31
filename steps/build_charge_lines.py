try:
    from .base import PayloadStep
    from ..models.charge_line import ChargeLineModel
    from ..models.common import ExtensionPropertyModel
    from ..pos_extract import PosKeys, LineKeys
    from ..utils.to_float import to_float
except ImportError:
    from steps.base import PayloadStep
    from models.charge_line import ChargeLineModel
    from models.common import ExtensionPropertyModel
    from pos_extract import PosKeys, LineKeys
    from utils.to_float import to_float


class ChargeLinesStep(PayloadStep):
    def apply(self, data, order):
        regular_lines = data.get(PosKeys.REGULAR_LINES) or []
        sales_lines = order.SalesLines or []

        for raw, sales_line_dict in zip(regular_lines, sales_lines):
            charge_lines = raw.get(PosKeys.CHARGE_LINES) or []
            if not charge_lines:
                continue

            sales_line_charges = sales_line_dict.setdefault("ChargeLines", [])

            for raw_charge in charge_lines:
                charge = ChargeLineModel()

                fee_id = raw_charge.get(LineKeys.FEE_ID)
                tax_level_id = raw_charge.get(LineKeys.TAX_LEVEL_ID)
                fee_amount = to_float(raw_charge.get(LineKeys.FEE_AMOUNT))
                tax_amount = to_float(raw_charge.get(LineKeys.TAX_COLLECTED_AMOUNT))

                charge.ChargeCode = fee_id or tax_level_id or ""
                charge.CalculatedAmount = fee_amount if fee_amount else tax_amount
                charge.Description = "Fee" if fee_id else "Tax"

                charge.ExtensionProperties.extend([
                    ExtensionPropertyModel.create_string("FeeId", fee_id or ""),
                    ExtensionPropertyModel.create_string(
                        "TaxLevelId", tax_level_id or ""
                    ),
                ])

                sales_line_charges.append(charge.to_dict())
