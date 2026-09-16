from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDO_User import GDO_User
from gdo.uncles.GDO_UncleCard import GDO_UncleCard
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard


class GDT_UncleCard(GDT_Object):
    """A reference to one immutable WeChall Card Clash card."""

    def __init__(self, name: str):
        super().__init__(name)
        self.table(GDO_UncleCard.table())
        self._default_random_own_card = False

    def default_random_own_card(self, default_random: bool = True):
        self._default_random_own_card = default_random
        return self.default_random(default_random)

    def query_default_random(self, multiple: int = None):
        if not self._default_random_own_card:
            return super().query_default_random(multiple)
        cards = GDO_UncleCard.table()
        ownership = GDO_UncleUserCard.table()
        query = cards.select().join(
            f'JOIN {ownership.gdo_table_name()} ON uc_card=card_id'
        ).where(f'uc_user={GDO_User.current().get_id()}').order('RAND()')
        if multiple:
            return query.limit(multiple).exec().fetch_all()
        return query.first().exec().fetch_object()
