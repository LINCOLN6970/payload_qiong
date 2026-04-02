class ShiftSummaryHeader:
    """Shift-level header fields (align with formal payloads shape)."""

    def __init__(self):
        self.BULLOCHSHIFTID = ""
        self.STORELOCATIONID = ""
        self.BEGINDATE = ""
        self.ENDDATE = ""

        self.TransactionsCount = 0
        self.SafeDropCount = 0
        self.SafeDropTotal = 0.0
        self.TotalSales = 0.0

        self.BEGINTIME = 0
        self.ENDTIME = 0
        self.ShiftId = ""
        self.TerminalId = ""
        self.OUN = ""
        self.CsuBaseUrl = ""
        self.OrderId = []
        self.endOfShift = 0
        self.endOfDay = 0

        self.CUSTOMERCOUNT = None
        self.DRAWERMANUALLYOPENED = None
        self.NUMBEROFCASHDRAWEROPENS = None
        self.NUMBEROFUNDOKEYSHIT = None
        self.NUMBEROFCLEARKEYSHIT = None
        self.NUMBEROFVOIDTRANSACTIONS = None
        self.ENDOFSHIFT = None
        self.CASHIERID = None
        self.ENDOFDAY = None

    def to_dict(self):
        d = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            d[k] = v
        return d