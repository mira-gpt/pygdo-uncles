from gdo.base.GDT import GDT
from gdo.base.Method import Method


class unclewipe(Method):
    """Owner-only reset for Card Clash cards, ownership and game statistics."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'unclewipe'

    def gdo_user_permission(self) -> str | None:
        return 'owner'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_execute(self) -> GDT:
        self.gdo_module().wipe_game()
        return self.msg('msg_uncle_wiped')
