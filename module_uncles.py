from random import choice, randint

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.GDO_Module import GDO_Module
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_UInt import GDT_UInt
from gdo.uncles.UNC_Card import UNC_Card
from gdo.uncles.UNC_UserCard import UNC_UserCard
from gdo.wechall.method.ranking import ranking


class module_uncles(GDO_Module):
    """WeChall player cards: starter decks, confrontations, and card stakes."""

    def gdo_dependencies(self) -> list:
        return ['core', 'table', 'user', 'wechall']

    def gdo_classes(self) -> list[type[GDO]]:
        return [UNC_Card, UNC_UserCard]

    def gdo_user_config(self) -> list[GDT]:
        return [GDT_Bool('unc_starter_deck').not_null().initial('0').hidden()]

    def gdo_module_config(self) -> list[GDT]:
        return [GDT_UInt('unc_rare_drop').not_null().min(0).max(100).initial('5')]

    async def gdo_install(self):
        self.seed_starter_cards()

    def seed_starter_cards(self):
        if UNC_Card.table().count_where():
            return
        users = ranking().gdo_table_query().limit(200).exec().fetch_all()
        for rank, user in enumerate(users[:100], 1):
            self.seed_card(user.get_name(), rank)
        for index, user in enumerate(users[99:200:10]):
            self.seed_card(user.get_name(), 100 + index * 10)

    @staticmethod
    def seed_card(nickname: str, rank: int):
        strength = max(1, 60 - rank // 3)
        stats = [max(1, strength + ((rank * factor) % 11) - 5) for factor in (3, 5, 7, 11, 13, 17)]
        UNC_Card.blank({
                'card_nickname': nickname,
                'card_rank': rank,
                'card_crypto': stats[0],
                'card_stegano': stats[1],
                'card_programming': stats[2],
                'card_exploit': stats[3],
                'card_math': stats[4],
                'card_info': stats[5],
                'card_rating': sum(stats),
            }).insert()

    def rare_drop(self, user: GDO_User) -> UNC_Card | None:
        if randint(1, 100) > self.get_config_value('unc_rare_drop'):
            return None
        cards = UNC_Card.table().select().where('card_rank <= 100').exec().fetch_all()
        card = choice(cards) if cards else None
        if card:
            self.add_card(user, card)
        return card

    @staticmethod
    def add_card(user: GDO_User, card: UNC_Card):
        owned = UNC_UserCard.table().get_by_vals({'uc_user': user.get_id(), 'uc_card': card.get_id()})
        if owned:
            owned.increase('uc_amount', 1)
        else:
            UNC_UserCard.blank({
                'uc_user': user.get_id(),
                'uc_card': card.get_id(),
                'uc_amount': '1',
            }).insert()

    def ensure_starter_deck(self, user: GDO_User):
        if user.get_setting_value('unc_starter_deck'):
            return
        for card in UNC_Card.table().select().exec().fetch_all():
            self.add_card(user, card)
        user.save_setting('unc_starter_deck', '1')

    def random_card(self, user: GDO_User) -> UNC_UserCard | None:
        cards = UNC_UserCard.table().select().where(f'uc_user={user.get_id()} AND uc_amount>0').exec().fetch_all()
        return cards[randint(0, len(cards) - 1)] if cards else None

    def transfer_card(self, card: UNC_UserCard, winner: GDO_User):
        card.increase('uc_amount', -1)
        self.add_card(winner, UNC_Card.table().get_by_id(card.gdo_val('uc_card')))
