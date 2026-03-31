class SalesOrderModel:
    def __init__(self):
        self.Id = None
        self.StoreId = None
        self.ChannelId = None
        self.CurrencyCode = None
        self.InventoryLocationId = None
        self.BusinessDate = None
        self.ShiftId = None
        self.ShiftTerminalId = None
        self.TerminalId = None
        self.TransactionDate = None
        self.TransactionTime = None

        self.GrossAmount = 0.0
        self.NetAmount = 0.0
        self.TotalAmount = 0.0
        self.AmountPaid = 0.0

        self.NetAmountWithoutTax = 0.0
        self.NetAmountWithNoTax = 0.0
        self.NetAmountWithTax = 0.0
        self.SubtotalAmount = 0.0
        self.SubtotalAmountWithoutTax = 0.0
        self.SubtotalSalesAmount = 0.0

        self.SalesLines = []
        self.TenderLines = []
        self.ChargeLines = []
        self.IncomeExpenseLines = []

        self.ExtensionProperties = []

    def to_dict(self):
        return {
            "Id": self.Id,
            "StoreId": self.StoreId,
            "ChannelId": self.ChannelId,
            "CurrencyCode": self.CurrencyCode,
            "InventoryLocationId": self.InventoryLocationId,
            "BusinessDate": self.BusinessDate,
            "ShiftId": self.ShiftId,
            "ShiftTerminalId": self.ShiftTerminalId,
            "TerminalId": self.TerminalId,
            "TransactionDate": self.TransactionDate,
            "TransactionTime": self.TransactionTime,
            "GrossAmount": self.GrossAmount,
            "NetAmount": self.NetAmount,
            "TotalAmount": self.TotalAmount,
            "AmountPaid": self.AmountPaid,
            "NetAmountWithoutTax": self.NetAmountWithoutTax,
            "NetAmountWithNoTax": self.NetAmountWithNoTax,
            "NetAmountWithTax": self.NetAmountWithTax,
            "SubtotalAmount": self.SubtotalAmount,
            "SubtotalAmountWithoutTax": self.SubtotalAmountWithoutTax,
            "SubtotalSalesAmount": self.SubtotalSalesAmount,
            "SalesLines": self.SalesLines,
            "TenderLines": self.TenderLines,
            "ChargeLines": self.ChargeLines,
            "IncomeExpenseLines": self.IncomeExpenseLines,
            "ExtensionProperties": [x.to_dict() for x in self.ExtensionProperties],
        }