"""Show portfolio candles.

    python -m examples.portfolio_candles
"""

import os
from datetime import datetime, timedelta
from typing import List, Tuple

import pandas as pd
import plotly.graph_objects as go

import tinvest as ti

client = ti.SyncClient(os.getenv('TINVEST_TOKEN', ''))


def main() -> None:
    payload = client.get_portfolio().payload
    figis = [(p.figi, p.name) for p in payload.positions]
    fig = get_figure(figis)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()


def get_figure(figis: List[Tuple[str, str]]) -> go.Figure:
    return go.Figure(
        data=[get_candlesstick(get_figi_data(figi), figi, name) for figi, name in figis]
    )


def get_candlesstick(df: pd.DataFrame, figi: str, name: str) -> go.Candlestick:
    return go.Candlestick(
        name=f'{name} {figi}',
        x=df['time'],
        open=df['o'],
        high=df['h'],
        low=df['l'],
        close=df['c'],
    )


def get_figi_data(figi: str) -> pd.DataFrame:
    now = datetime.now()
    payload = client.get_market_candles(
        figi=figi,
        from_=now - timedelta(days=31 * 12),
        to=now,
        interval=ti.CandleResolution.week,
    ).payload
    return pd.DataFrame(c.dict() for c in payload.candles)


if __name__ == '__main__':
    main()
