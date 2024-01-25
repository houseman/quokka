def test_intraday():
    from quokka import AlphaVantageClient

    client = AlphaVantageClient()

    output = client.intraday(symbol="IBM", interval=AlphaVantageClient.DataPointInterval.INTERVAL_60_MIN)

    assert output == {}
