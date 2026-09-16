from random import randint

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_User import GDT_User
from gdo.uncles.GDO_UncleCard import GDO_UncleCard
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard


class uncle(Method):
    """Choose one card to confront a random card from another player."""

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_User('user').not_null().same_channel(self._env_channel),
            GDT_String('card').not_null().maxlen(64),
        ]

    def gdo_execute(self) -> GDT:
        attacker = self._env_user
        defender = self.param_value('user')
        if attacker.get_id() == defender.get_id():
            return self.err('err_uncle_self')
        module = self.gdo_module()
        module.ensure_starter_deck(attacker)
        module.ensure_starter_deck(defender)
        selected = self.get_card(self.param_val('card'))
        attacker_card = selected and GDO_UncleUserCard.table().get_by_vals({'uc_user': attacker.get_id(), 'uc_card': selected.get_id()})
        defender_card = module.random_card(defender)
        if not attacker_card or not defender_card:
            return self.err('err_uncle_no_cards')
        attacker_damage, critical, direct = module.battle(attacker_card, defender_card)
        defender_damage, _, _ = module.battle(defender_card, attacker_card)
        winner, loser = (attacker, defender) if attacker_damage >= defender_damage else (defender, attacker)
        lost_card = defender_card if winner is attacker else attacker_card
        module.exchange_cards(attacker_card, defender_card)
        drop = module.rare_drop(winner)
        key = 'msg_uncle_won_drop' if drop else 'msg_uncle_won'
        flags = (' critical' if critical else '') + (' direct' if direct else '')
        args = (winner.render_name(), loser.render_name(), self.card_name(lost_card), attacker_damage, defender_damage, flags)
        if drop:
            args += (drop.gdo_val('card_nickname'),)
        return self.msg(key, args)

    @staticmethod
    def card_name(card: GDO_UncleUserCard) -> str:
        return GDO_UncleCard.table().get_by_id(card.gdo_val('uc_card')).gdo_val('card_nickname')

    @staticmethod
    def get_card(card: str) -> GDO_UncleCard | None:
        """Cards are addressed by their permanent ID or nickname."""
        if card.isdecimal():
            return GDO_UncleCard.table().get_by_id(card)
        return GDO_UncleCard.table().get_by_vals({'card_nickname': card})
