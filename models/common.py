class ExtensionPropertyModel:
    def __init__(self, key: str, value: dict):
        self.Key = key
        self.Value = value

    def to_dict(self):
        return {
            "Key": self.Key,
            "Value": self.Value,
        }

    @classmethod
    def create_string(cls, key: str, value):
        return cls(key, {"StringValue": "" if value is None else str(value)})

    @classmethod
    def create_decimal(cls, key: str, value):
        try:
            decimal_value = 0.0 if value in (None, "") else float(value)
        except (TypeError, ValueError):
            decimal_value = 0.0
        return cls(key, {"DecimalValue": decimal_value})

    @classmethod
    def create_int(cls, key: str, value):
        try:
            int_value = 0 if value in (None, "") else int(value)
        except (TypeError, ValueError):
            int_value = 0
        return cls(key, {"IntegerValue": int_value})