"""

"""

from abc import ABC, abstractmethod

from vnpy.event import EventEngine, Event

from .event import (EVENT_TICK, EVENT_ORDER, EVENT_TRADE, EVENT_ACCOUNT,
                    EVENT_POSITION, EVENT_LOG, EVENT_CONTRACT)
from .object import (TickData, OrderData, TradeData, AccountData, PositionData,
                     LogData, ContractData, SubscribeRequest, OrderRequest,
                     CancelRequest)


class Gateway(ABC):
    """
    Abstract gateway class for creating gateways connection 
    to different trading systems.
    """

    def __init__(self, event_engine: EventEngine, gateway_name: str):
        """"""
        self.event_engine = event_engine
        self.gateway_name = gateway_name

    def on_event(self, type: str, data: Any = None):
        """
        General event push.
        """
        event = Event(type, data)
        self.event_engine.put(event)

    def on_tick(self, tick: TickData):
        """
        Tick event push.
        Tick event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_TICK, tick)
        self.on_event(EVENT_TICK + tick.vt_symbol, tick)

    def on_trade(self, trade: TradeData):
        """
        Trade event push.
        Trade event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_TRADE, trade)
        self.on_event(EVENT_TRADE + trade.vt_symbol, trade)

    def on_order(self, order: OrderData):
        """
        Order event push.
        Order event of a specific vt_orderid is also pushed.
        """
        self.on_event(EVENT_ORDER, order)
        self.on_event(EVENT_ORDER + order.vt_orderid, order)

    def on_position(self, position: PositionData):
        """
        Position event push.
        Position event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_POSITION, position)
        self.on_event(EVENT_POSITION + position.vt_symbol, position)

    def on_account(self, account: AccountData):
        """
        Account event push.
        Account event of a specific vt_accountid is also pushed.
        """
        self.on_event(EVENT_ACCOUNT, account)
        self.on_event(EVENT_ACCOUNT + account.vt_accountid, account)

    def on_log(self, log: LogData):
        """
        Log event push.
        """
        self.on_event(EVENT_LOG, log)

    def on_contract(self, contract: ContractData):
        """
        Contract event push.
        """
        self.on_event(EVENT_CONTRACT, contract)

    @abstractmethod
    def connect(self):
        """
        Start gateway connection.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close gateway connection.
        """
        pass

    @abstractmethod
    def subscribe(self, req: SubscribeRequest):
        """
        Subscribe tick data update.
        """
        pass

    @abstractmethod
    def send_order(self, req: OrderRequest):
        """
        Send a new order.
        """
        pass

    @abstractmethod
    def cancel_order(self, req: CancelRequest):
        """
        Cancel an existing order.
        """
        pass

    @abstractmethod
    def query_account(self):
        """
        Query account balance.
        """
        pass

    @abstractmethod
    def query_position(self):
        """
        Query holding positions.
        """
        pass