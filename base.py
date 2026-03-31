class BasePayloadBuilder:
    def __init__(self, model_cls, steps=None):
        self.model_cls = model_cls
        self.steps = list(steps or [])
        self.skip_reason = None

    def build(self, data):
        self.skip_reason = None
        return self._build(data)

    def build_dict(self, data):
        payload = self.build(data)
        if payload is None:
            return None
        return payload.to_dict()

    def _build(self, data):
        payload = self.model_cls()
        for step in self.steps:
            step.apply(data, payload)
        return payload