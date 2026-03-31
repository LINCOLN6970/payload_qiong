try:
    from ..data_manager import get_data_manager
except ImportError:
    from data_manager import get_data_manager


class PayloadStep:
    def apply(self, data, payload):
        raise NotImplementedError("Payload steps must implement apply().")


class DataManagerStep(PayloadStep):
    """Steps that need store/tender/fuel mappings."""

    def __init__(self, data_manager=None):
        self._dm = data_manager if data_manager is not None else get_data_manager()