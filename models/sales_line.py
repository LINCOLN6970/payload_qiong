class SalesLineModel:
    def __init__(self):
        self.LineNumber = 0
        self.Description = ""
        self.ProductId = 0
        self.ListingId = 0
        self.ItemId = ""
        self.Quantity = 0.0
        self.QuantityOrdered = 0.0
        self.Price = 0.0
        self.OriginalPrice = 0.0
        self.TotalAmount = 0.0
        self.NetAmount = 0.0
        self.NetAmountWithoutTax = 0.0
        self.GrossAmount = 0.0
        self.NetPrice = 0.0
        self.ReturnChannelId = None
        self.UnitOfMeasureSymbol = ""
        self.SalesOrderUnitOfMeasure = ""
        self.IsPriceOverridden = False
        self.ChargeLines = []
        self.ExtensionProperties = []

    def to_dict(self):
        return {
            "LineNumber": self.LineNumber,
            "Description": self.Description,
            "ProductId": self.ProductId,
            "ListingId": self.ListingId,
            "ItemId": self.ItemId,
            "Quantity": self.Quantity,
            "QuantityOrdered": self.QuantityOrdered,
            "Price": self.Price,
            "OriginalPrice": self.OriginalPrice,
            "TotalAmount": self.TotalAmount,
            "NetAmount": self.NetAmount,
            "NetAmountWithoutTax": self.NetAmountWithoutTax,
            "GrossAmount": self.GrossAmount,
            "NetPrice": self.NetPrice,
            "ReturnChannelId": self.ReturnChannelId,
            "UnitOfMeasureSymbol": self.UnitOfMeasureSymbol,
            "SalesOrderUnitOfMeasure": self.SalesOrderUnitOfMeasure,
            "IsPriceOverridden": self.IsPriceOverridden,
            "ChargeLines": [x.to_dict() for x in self.ChargeLines],
            "ExtensionProperties": [x.to_dict() for x in self.ExtensionProperties],
        }