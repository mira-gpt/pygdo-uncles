from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard
from gdo.uncles.GDT_UncleCard import GDT_UncleCard


class unclecard(Method):
    """Inspect a fixed WeChall card and its current ownership count."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'unclecard'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_UncleCard('card').default_random_own_card()]

    def gdo_execute(self) -> GDT:
        card = self.param_value('card')
        if card is None:
            return self.err('err_uncle_card_unknown')
        owned = GDO_UncleUserCard.table().count_where(f'uc_card={card.get_id()}')
        return self.msg('msg_unclecard', (
            card.render_name(),
            card.gdo_val('card_rank'),
            card.gdo_val('card_followers'),
            card.gdo_val('card_crypto'),
            card.gdo_val('card_stegano'),
            card.gdo_val('card_programming'),
            card.gdo_val('card_exploit'),
            card.gdo_val('card_math'),
            card.gdo_val('card_info'),
            card.gdo_val('card_rating'),
            owned,
        ))
