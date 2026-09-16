from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Util import StringsUtil
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_UInt import GDT_UInt


class GDO_UncleCard(GDO):
    """Canonical fixed mapping of card IDs to WeChall-player nicknames and stats."""

    def render_name(self) -> str:
        return f'{self.get_id()}-{StringsUtil.utf8obfuscate(self.gdo_val("card_nickname"))}'

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('card_id'),
            GDT_Name('card_nickname').not_null().unique(),
            GDT_UInt('card_rank').not_null().bytes(1),
            GDT_UInt('card_followers').not_null().initial('0').bytes(1),
            GDT_UInt('card_crypto').not_null().bytes(1),
            GDT_UInt('card_stegano').not_null().bytes(1),
            GDT_UInt('card_programming').not_null().bytes(1),
            GDT_UInt('card_exploit').not_null().bytes(1),
            GDT_UInt('card_math').not_null().bytes(1),
            GDT_UInt('card_info').not_null().bytes(1),
            GDT_UInt('card_rating').not_null().bytes(1),
        ]
