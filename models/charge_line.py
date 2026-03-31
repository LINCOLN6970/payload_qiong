class ChargeLineModel:
    def __init__(self):
        self.ChargeCode = ""
        self.CalculatedAmount = 0.0
        self.Description = ""
        self.ExtensionProperties = []

    def to_dict(self):
        return {
            "ChargeCode": self.ChargeCode,
            "CalculatedAmount": self.CalculatedAmount,
            "Description": self.Description,
            "ExtensionProperties": [x.to_dict() for x in self.ExtensionProperties],
        }