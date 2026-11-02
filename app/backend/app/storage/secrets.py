import base64


class SecretStorage:
    """MVP secret abstraction.

    TODO: replace with OS keychain/KMS-backed encryption before production use.
    """

    @staticmethod
    def store(value: str | None) -> str | None:
        if not value:
            return None
        encoded = base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii")
        return f"mvp:v1:{encoded}"

    @staticmethod
    def reveal(value: str | None) -> str | None:
        if not value:
            return None
        if not value.startswith("mvp:v1:"):
            return value
        encoded = value.removeprefix("mvp:v1:")
        return base64.urlsafe_b64decode(encoded.encode("ascii")).decode("utf-8")

    @staticmethod
    def mask(value: str | None) -> str | None:
        revealed = SecretStorage.reveal(value)
        if not revealed:
            return None
        tail = revealed[-4:] if len(revealed) >= 4 else revealed
        return f"****{tail}"
