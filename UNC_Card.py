from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_UInt import GDT_UInt


class UNC_Card(GDO):
    """A WeChall-player card and its six challenge-discipline ratings."""

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('card_id'),
            GDT_Name('card_nickname').not_null().unique(),
            GDT_UInt('card_rank').not_null(),
            GDT_UInt('card_crypto').not_null(),
            GDT_UInt('card_stegano').not_null(),
            GDT_UInt('card_programming').not_null(),
            GDT_UInt('card_exploit').not_null(),
            GDT_UInt('card_math').not_null(),
            GDT_UInt('card_info').not_null(),
            GDT_UInt('card_rating').not_null(),
        ]
