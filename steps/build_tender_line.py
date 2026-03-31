try:
    from .base import DataManagerStep
    from ..models.tender_line import TenderLineModel
    from ..models.common import ExtensionPropertyModel
    from ..pos_extract import PosKeys, LineKeys
    from ..utils.to_float import to_float
except ImportError:
    from steps.base import DataManagerStep
    from models.tender_line import TenderLineModel
    from models.common import ExtensionPropertyModel
    from pos_extract import PosKeys, LineKeys
    from utils.to_float import to_float


class TenderLinesStep(DataManagerStep):
    def apply(self, data, order):
        tender_lines = data.get(PosKeys.TENDER_LINES) or []

        for raw in tender_lines:
            amount = to_float(raw.get(LineKeys.TENDER_AMOUNT))
            if amount == 0:
                continue

            tender_code = raw.get(LineKeys.TENDER_CODE, "")
            tender_subcode = raw.get(LineKeys.TENDER_SUBCODE, "")

            line = TenderLineModel()
            line.StoreId = order.StoreId
            line.TerminalId = order.TerminalId
            line.TransactionId = order.Id
            line.Amount = amount
            line.AmountInTenderedCurrency = amount
            line.AmountInCompanyCurrency = amount
            line.ChannelId = order.ChannelId
            line.TenderTypeId = self._dm.get_tender_type_id(
                tender_code,
                tender_subcode,
            )
            line.LineNumber = len(order.TenderLines) + 1
            line.CustomerId = raw.get(LineKeys.ACCOUNT_ID, "")

            line.ExtensionProperties.extend([
                ExtensionPropertyModel.create_string(
                    "TenderSubCode",
                    tender_subcode,
                ),
            ])

            order.TenderLines.append(line.to_dict())
