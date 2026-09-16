from random import randint

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_User import GDT_User
from gdo.uncles.UNC_Card import UNC_Card
from gdo.uncles.UNC_UserCard import UNC_UserCard


class uncle(Method):
    """Confront another player; the defeated player's selected card changes hands."""

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_User('user').not_null().same_channel(self._env_channel)]

    def gdo_execute(self) -> GDT:
        winner = self._env_user
        loser = self.param_value('user')
        if winner.get_id() == loser.get_id():
            return self.err('err_uncle_self')
        module = self.gdo_module()
        module.ensure_starter_deck(winner)
        module.ensure_starter_deck(loser)
        winner_card = module.random_card(winner)
        loser_card = module.random_card(loser)
        if not winner_card or not loser_card:
            return self.err('err_uncle_no_cards')
        winner_rating = self.card_rating(winner_card) + randint(0, 20)
        loser_rating = self.card_rating(loser_card) + randint(0, 20)
        if loser_rating > winner_rating:
            winner, loser = loser, winner
            winner_card, loser_card = loser_card, winner_card
            winner_rating, loser_rating = loser_rating, winner_rating
        module.transfer_card(loser_card, winner)
        drop = module.rare_drop(winner)
        key = 'msg_uncle_won_drop' if drop else 'msg_uncle_won'
        args = (winner.render_name(), loser.render_name(), self.card_name(loser_card), winner_rating, loser_rating)
        if drop:
            args += (drop.gdo_val('card_nickname'),)
        return self.msg(key, args)

    @staticmethod
    def card_rating(card: UNC_UserCard) -> int:
        return int(UNC_Card.table().get_by_id(card.gdo_val('uc_card')).gdo_val('card_rating'))

    @staticmethod
    def card_name(card: UNC_UserCard) -> str:
        return UNC_Card.table().get_by_id(card.gdo_val('uc_card')).gdo_val('card_nickname')
