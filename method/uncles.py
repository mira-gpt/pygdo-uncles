from gdo.base.GDO import GDO
from gdo.base.Query import Query
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_Name import GDT_Name
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard


class uncles(MethodQueryTable):
    """The caller's current collectible card deck."""

    def gdo_table(self) -> GDO:
        return GDO_UncleUserCard.table()

    def gdo_table_query(self) -> Query:
        self.gdo_module().ensure_starter_deck(GDO_User.current())
        return GDO_UncleUserCard.table().select().join_object('uc_card').where(f'uc_user={GDO_User.current().get_id()}').order('card_rank ASC')

    def gdo_table_headers(self) -> list:
        return [
            GDT_Name('card_nickname').label('card'),
            GDT_UInt('card_rank').label('rank'),
            GDT_UInt('card_crypto').label('crypto'),
            GDT_UInt('card_stegano').label('stegano'),
            GDT_UInt('card_programming').label('programming'),
            GDT_UInt('card_exploit').label('exploit'),
            GDT_UInt('card_math').label('math'),
            GDT_UInt('card_info').label('info'),
            GDT_UInt('card_rating').label('rating'),
        ]
