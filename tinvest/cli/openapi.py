from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

import typer
from pydantic import BaseModel
from pydantic.datetime_parse import parse_datetime

import tinvest as ti

openapi = typer.Typer()

DATETIME_HELP = (
    'Use one of [now, day, week, month, 6month, year] or any date-time format'
)


class OpenapiCtx(BaseModel):
    token: str = ''
    sandbox_token: str = ''
    use_sandbox: bool = False


class BaseApi:
    client: ti.SyncClient


def do_request(ctx: typer.Context, method, *args, **kwargs):
    if ctx.obj.use_sandbox:
        client = ti.SyncClient(ctx.obj.sandbox_token, use_sandbox=True)
    else:
        client = ti.SyncClient(ctx.obj.token)
    try:
        return method(client, *args, **kwargs).payload
    except ti.BadRequestError as e:
        typer.echo(f'500 {e.response.payload}')

    raise typer.Exit(code=1)


def convert_to_datetime(val: str) -> datetime:
    constants = {
        'now': datetime.utcnow(),
        'day': datetime.utcnow() - timedelta(days=1),
        'week': datetime.utcnow() - timedelta(days=7),
        'month': datetime.utcnow() - timedelta(days=31),
        '6month': datetime.utcnow() - timedelta(days=31 * 6),
        'year': datetime.utcnow() - timedelta(days=365),
    }
    if val in constants:
        return constants[val]
    return parse_datetime(val)


def dt_to_str(dt: datetime) -> str:
    return dt.ctime()


def show(*args):
    typer.echo('\t'.join(str(item) for item in args))


@openapi.callback()
def openapi_main(
    ctx: typer.Context,
    token: str = typer.Option('', envvar='TINVEST_TOKEN'),  # noqa:B008
    sandbox_token: str = typer.Option('', envvar='TINVEST_SANDBOX_TOKEN'),  # noqa:B008
    use_sandbox: bool = typer.Option(False, '--use-sandbox', '-s'),  # noqa:B008
):
    ctx.ensure_object(OpenapiCtx)
    ctx.obj.token = token
    ctx.obj.sandbox_token = sandbox_token
    ctx.obj.use_sandbox = use_sandbox


@openapi.command()
def sandbox_register(ctx: typer.Context, broker_account_type: ti.BrokerAccountType):
    payload = do_request(
        ctx,
        ti.SyncClient.register_sandbox_account,
        ti.SandboxRegisterRequest(broker_account_type=broker_account_type),
    )
    show(payload.broker_account_id, payload.broker_account_type.value)


@openapi.command()
def sandbox_currencies_balance(
    ctx: typer.Context,
    balance: float,
    currency: ti.SandboxCurrency,
    broker_account_id: Optional[str] = None,
):
    do_request(
        ctx,
        ti.SyncClient.set_sandbox_currencies_balance,
        ti.SandboxSetCurrencyBalanceRequest(balance=balance, currency=currency),
        broker_account_id,
    )


@openapi.command()
def sandbox_positions_balance(
    ctx: typer.Context,
    balance: float,
    figi: Optional[str] = None,
    broker_account_id: Optional[str] = None,
):
    do_request(
        ctx,
        ti.SyncClient.set_sandbox_positions_balance,
        ti.SandboxSetPositionBalanceRequest(balance=balance, figi=figi),
        broker_account_id,
    )


@openapi.command()
def sandbox_remove(ctx: typer.Context, broker_account_id: Optional[str] = None):
    do_request(ctx, ti.SyncClient.remove_sandbox_account, broker_account_id)


@openapi.command()
def sandbox_clear(ctx: typer.Context, broker_account_id: Optional[str] = None):
    do_request(ctx, ti.SyncClient.clear_sandbox_account, broker_account_id)


@openapi.command()
def orders(ctx: typer.Context, broker_account_id: Optional[str] = None):
    payload = do_request(ctx, ti.SyncClient.get_orders, broker_account_id)
    for order in payload:
        show(
            order.figi,
            order.order_id,
            order.operation.value,
            order.status.value,
            order.type_.value,
            order.price,
            order.requested_lots,
            order.executed_lots,
        )


@openapi.command()
def orders_limit_order(  # pylint:disable=too-many-arguments
    ctx: typer.Context,
    figi: str,
    operation: ti.OperationType,
    lots: int,
    price: float,
    broker_account_id: Optional[str] = None,
):
    payload = do_request(
        ctx,
        ti.SyncClient.post_orders_limit_order,
        figi,
        ti.LimitOrderRequest(
            operation=operation,
            lots=lots,
            price=price,
        ),
        broker_account_id,
    )
    show(
        payload.order_id,
        payload.commission and payload.commission.value,
        payload.commission and payload.commission.currency,
        payload.executed_lots,
        payload.operation.value,
        payload.status.value,
        payload.reject_reason,
        payload.message,
        payload.requested_lots,
    )


@openapi.command()
def orders_market_order(
    ctx: typer.Context,
    figi: str,
    operation: ti.OperationType,
    lots: int,
    broker_account_id: Optional[str] = None,
):
    payload = do_request(
        ctx,
        ti.SyncClient.post_orders_market_order,
        figi,
        ti.MarketOrderRequest(
            operation=operation,
            lots=lots,
        ),
        broker_account_id,
    )
    show(
        payload.order_id,
        payload.commission and payload.commission.value,
        payload.commission and payload.commission.currency,
        payload.executed_lots,
        payload.operation.value,
        payload.status.value,
        payload.reject_reason,
        payload.message,
        payload.requested_lots,
    )


@openapi.command()
def orders_cancel(
    ctx: typer.Context, order_id: str, broker_account_id: Optional[str] = None
):
    do_request(ctx, ti.SyncClient.post_orders_cancel, order_id, broker_account_id)


@openapi.command()
def portfolio(ctx: typer.Context, broker_account_id: Optional[str] = None):
    payload = do_request(ctx, ti.SyncClient.get_portfolio, broker_account_id)
    for position in payload.positions:
        show(
            position.figi,
            position.lots,
            position.average_position_price and position.average_position_price.value,
            position.balance,
            position.expected_yield and position.expected_yield.value,
            position.name,
        )


@openapi.command()
def portfolio_currencies(ctx: typer.Context, broker_account_id: Optional[str] = None):
    payload = do_request(ctx, ti.SyncClient.get_portfolio_currencies, broker_account_id)
    for currency in payload.currencies:
        show(
            currency.currency.value,
            currency.balance,
            currency.blocked or 0.0,
        )


@openapi.command()
def market_stocks(ctx: typer.Context):
    payload = do_request(ctx, ti.SyncClient.get_market_stocks)
    _show_instruments_payload(payload)


@openapi.command()
def market_bonds(ctx: typer.Context):
    payload = do_request(ctx, ti.SyncClient.get_market_bonds)
    _show_instruments_payload(payload)


@openapi.command()
def market_etfs(ctx: typer.Context):
    payload = do_request(ctx, ti.SyncClient.get_market_etfs)
    _show_instruments_payload(payload)


@openapi.command()
def market_currencies(ctx: typer.Context):
    payload = do_request(ctx, ti.SyncClient.get_market_currencies)
    _show_instruments_payload(payload)


@openapi.command()
def market_orderbook(ctx: typer.Context, figi: str, depth: int):
    payload = do_request(ctx, ti.SyncClient.get_market_orderbook, figi, depth)
    show('FIGI', payload.figi)
    show('Status', payload.trade_status.value)
    show('Close price', payload.close_price)
    show('Last price', payload.last_price)
    show('Face value', payload.face_value)
    show('Limit down', payload.limit_down)
    show('Limit up', payload.limit_up)
    show('Min price increment', payload.min_price_increment)
    show('Depth', payload.depth)
    show('Orders')
    orders_ = []
    for order in payload.asks:
        orders_.append(('<  ', order))
    for order in payload.bids:
        orders_.append(('  >', order))
    orders_.sort(key=lambda o: o[1].price, reverse=True)
    for order_type, order in orders_:
        show('', order_type, order.price, order.quantity)


@openapi.command()
def market_candles(
    ctx: typer.Context,
    figi: str,
    interval: ti.CandleResolution,
    from_: str = typer.Argument(..., metavar='FROM', help=DATETIME_HELP),
    to: str = typer.Argument('now', help=DATETIME_HELP),
):
    payload = do_request(
        ctx,
        ti.SyncClient.get_market_candles,
        figi,
        convert_to_datetime(from_),
        convert_to_datetime(to),
        interval,
    )
    for candle in payload.candles:
        show(
            candle.figi,
            candle.time,
            candle.o,
            candle.c,
            candle.h,
            candle.l,
            candle.v,
            candle.interval.value,
        )


@openapi.command()
def market_search_by_figi(ctx: typer.Context, figi: str):
    payload = do_request(ctx, ti.SyncClient.get_market_search_by_figi, figi=figi)
    show(
        payload.figi,
        payload.currency and payload.currency.value,
        payload.lot,
        payload.min_price_increment,
        payload.ticker,
        payload.name,
    )


@openapi.command()
def market_search_by_ticker(ctx: typer.Context, ticker: str):
    payload = do_request(ctx, ti.SyncClient.get_market_search_by_ticker, ticker=ticker)
    _show_instruments_payload(payload)


def _show_instruments_payload(payload: ti.MarketInstrumentList):
    for instrument in payload.instruments:
        show(
            instrument.figi,
            instrument.currency and instrument.currency.value,
            instrument.lot,
            instrument.min_quantity,
            instrument.min_price_increment,
            instrument.ticker,
            instrument.name,
        )
    show('Total', payload.total)


@openapi.command()
def operations(
    ctx: typer.Context,
    from_: str = typer.Argument(..., metavar='FROM', help=DATETIME_HELP),
    to: str = typer.Argument('now', help=DATETIME_HELP),
    figi: Optional[str] = None,
    broker_account_id: Optional[str] = None,
):
    payload = do_request(
        ctx,
        ti.SyncClient.get_operations,
        convert_to_datetime(from_),
        convert_to_datetime(to),
        figi,
        broker_account_id,
    )
    for operation in payload.operations:
        show(
            dt_to_str(operation.date),
            operation.payment,
            operation.currency.value,
            operation.status.value,
            operation.figi,
            operation.id,
        )
    if not payload.operations:
        return
    commissions = defaultdict(list)
    for operation in payload.operations:
        if operation.operation_type == ti.OperationTypeWithCommission.broker_commission:
            commissions[operation.currency].append(operation.payment)
    typer.echo('\nCommissions')
    for currency, values in commissions.items():
        show('', currency.value, sum(values) * -1)


@openapi.command()
def accounts(ctx: typer.Context):
    payload = do_request(ctx, ti.SyncClient.get_accounts)
    for account in payload.accounts:
        show(account.broker_account_id, account.broker_account_type.value)
