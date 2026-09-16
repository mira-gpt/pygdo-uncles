from gdo.base.GDO import GDO
from gdo.base.Query import Query
from gdo.base.Render import Mode
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_Name import GDT_Name
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.uncles.GDO_UncleCard import GDO_UncleCard
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard


class uncles(MethodQueryTable):
    """The caller's current collectible card deck."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'uncles'

    def gdo_method_hidden(self) -> bool:
        return True

    def render_gdo(self, gdo: GDO, mode: Mode) -> str | dict:
        if mode == Mode.render_json:
            return super().render_gdo(gdo, mode)
        return gdo.render_name()

    def gdo_table(self) -> GDO:
        return GDO_UncleCard.table()

    def gdo_table_query(self) -> Query:
        self.gdo_module().ensure_starter_deck(GDO_User.current())
        cards = GDO_UncleCard.table()
        ownership = GDO_UncleUserCard.table()
        return cards.select().join(
            f'JOIN {ownership.gdo_table_name()} ON uc_card=card_id'
        ).where(f'uc_user={GDO_User.current().get_id()}').order('card_rank ASC')

    def gdo_table_headers(self) -> list:
        return [
            GDT_Name('card_nickname').label('card'),
            GDT_UInt('card_rank').label('rank'),
            GDT_UInt('card_followers').label('followers'),
            GDT_UInt('card_crypto').label('crypto'),
            GDT_UInt('card_stegano').label('stegano'),
            GDT_UInt('card_programming').label('programming'),
            GDT_UInt('card_exploit').label('exploit'),
            GDT_UInt('card_math').label('math'),
            GDT_UInt('card_info').label('info'),
            GDT_UInt('card_rating').label('rating'),
        ]
