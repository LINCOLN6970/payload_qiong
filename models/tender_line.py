class TenderLineModel:
    def __init__(self):
        self.StoreId = None
        self.TerminalId = None
        self.TransactionId = None
        self.Amount = 0.0
        self.AmountInTenderedCurrency = 0.0
        self.AmountInCompanyCurrency = 0.0
        self.ChannelId = None
        self.TenderTypeId = ""
        self.LineNumber = 0
        self.CustomerId = ""
        self.ExtensionProperties = []

    def to_dict(self):
        return {
            "StoreId": self.StoreId,
            "TerminalId": self.TerminalId,
            "TransactionId": self.TransactionId,
            "Amount": self.Amount,
            "AmountInTenderedCurrency": self.AmountInTenderedCurrency,
            "AmountInCompanyCurrency": self.AmountInCompanyCurrency,
            "ChannelId": self.ChannelId,
            "TenderTypeId": self.TenderTypeId,
            "LineNumber": self.LineNumber,
            "CustomerId": self.CustomerId,
            "ExtensionProperties": [x.to_dict() for x in self.ExtensionProperties],
        }