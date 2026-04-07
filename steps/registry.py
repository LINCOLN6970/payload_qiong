REGISTRY: dict[str, type] = {}

def register(name: str, cls: type) -> None:
    REGISTRY[name] = cls

def get_step(name: str) -> type:
    if name not in REGISTRY:
        raise KeyError(f"Unknown step: {name}")
    return REGISTRY[name]