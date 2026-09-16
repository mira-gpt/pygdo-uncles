from gdo.base.GDT import GDT
from gdo.base.Method import Method


class unclegame(Method):
    """Public quick reference for WeChall Card Clash."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'unclegame'

    def gdo_execute(self) -> GDT:
        return self.msg('msg_unclegame')
