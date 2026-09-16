from random import randint

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_User import GDT_User
from gdo.uncles.UNC_Card import UNC_Card
from gdo.uncles.UNC_UserCard import UNC_UserCard


class uncle(Method):
    """Choose one card to confront a random card from another player."""

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_User('user').not_null().same_channel(self._env_channel),
            GDT_Object('card').not_null().table(UNC_Card.table()),
        ]

    def gdo_execute(self) -> GDT:
        attacker = self._env_user
        defender = self.param_value('user')
        if attacker.get_id() == defender.get_id():
            return self.err('err_uncle_self')
        module = self.gdo_module()
        module.ensure_starter_deck(attacker)
        module.ensure_starter_deck(defender)
        selected = self.param_value('card')
        attacker_card = UNC_UserCard.table().get_by_vals({'uc_user': attacker.get_id(), 'uc_card': selected.get_id()})
        defender_card = module.random_card(defender)
        if not attacker_card or not defender_card:
            return self.err('err_uncle_no_cards')
        attacker_damage, critical, direct = module.battle(attacker_card, defender_card)
        defender_damage, _, _ = module.battle(defender_card, attacker_card)
        winner, loser = (attacker, defender) if attacker_damage >= defender_damage else (defender, attacker)
        lost_card = defender_card if winner is attacker else attacker_card
        module.transfer_card(lost_card, winner)
        drop = module.rare_drop(winner)
        key = 'msg_uncle_won_drop' if drop else 'msg_uncle_won'
        flags = (' critical' if critical else '') + (' direct' if direct else '')
        args = (winner.render_name(), loser.render_name(), self.card_name(lost_card), attacker_damage, defender_damage, flags)
        if drop:
            args += (drop.gdo_val('card_nickname'),)
        return self.msg(key, args)

    @staticmethod
    def card_name(card: UNC_UserCard) -> str:
        return UNC_Card.table().get_by_id(card.gdo_val('uc_card')).gdo_val('card_nickname')
