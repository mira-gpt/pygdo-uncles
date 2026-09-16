from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_User import GDT_User
from gdo.uncles.UNC_Card import UNC_Card


class UNC_UserCard(GDO):
    """One card stack owned by one player."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_User('uc_user').primary().cascade_delete(),
            GDT_Object('uc_card').primary().table(UNC_Card.table()).cascade_delete(),
            GDT_UInt('uc_amount').not_null().initial('1'),
        ]
