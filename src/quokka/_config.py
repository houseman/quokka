import os


class AlphaVantageConfig:
    @property
    def api_key(self) -> str | None:
        return os.environ.get("AV_API_KEY")

    @property
    def hostname(self) -> str:
        return os.environ.get("AV_HOSTNAME", "www.alphavantage.co")
