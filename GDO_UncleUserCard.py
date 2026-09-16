from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_User import GDT_User
from gdo.uncles.GDO_UncleCard import GDO_UncleCard


class GDO_UncleUserCard(GDO):
    """A unique player/card ownership pair — each player holds at most one copy."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_User('uc_user').primary().cascade_delete(),
            GDT_Object('uc_card').primary().table(GDO_UncleCard.table()).cascade_delete(),
        ]
