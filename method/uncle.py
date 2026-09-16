from random import randint

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_User import GDT_User
from gdo.date.Time import Time
from gdo.uncles.GDO_UncleCard import GDO_UncleCard
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard
from gdo.uncles.GDT_UncleCard import GDT_UncleCard


class uncle(Method):
    """Choose one card to confront a random card from another player."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'uncle'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [
            # IRC nicknames repeat across connectors. A duel names somebody
            # on the current network, even when they are elsewhere on it.
            GDT_User('user').same_server().not_null(),
            GDT_UncleCard('card').default_random_own_card(),
        ]

    async def gdo_execute(self) -> GDT:
        attacker = self._env_user
        defender = self.param_value('user')
        if attacker.get_id() == defender.get_id():
            return self.err('err_uncle_self')
        module = self.gdo_module()
        now = int(Time.get_time())
        cooldown = module.get_config_value('uncle_cooldown')
        until = int(attacker.get_setting_value('uncle_last_human')) + cooldown
        if until > now:
            return self.err('err_uncle_cooldown', (Time.human_duration(until - now),))
        module.ensure_starter_deck(attacker)
        module.ensure_starter_deck(defender)
        selected = self.param_value('card')
        attacker_card = GDO_UncleUserCard.table().get_by_vals({'uc_user': attacker.get_id(), 'uc_card': selected.get_id()})
        defender_card = module.random_card(defender)
        if not attacker_card or not defender_card:
            return self.err('err_uncle_no_cards')
        attacker.save_setting('uncle_last_human', str(now))
        attacker.increase_setting('uncles_played')
        defender.increase_setting('uncles_played')
        attacker_damage, defender_damage, attack_skill, defense_skill, attacker_max, defender_max = module.battle(attacker_card, defender_card)
        winner, loser = (attacker, defender) if attacker_damage >= defender_damage else (defender, attacker)
        winner.increase_setting('uncles_won')
        lost_card = defender_card if winner is attacker else attacker_card
        module.claim_card(winner, lost_card)
        verb = module.verb()
        if winner is attacker:
            await defender.send('msg_uncle_opponent_lost', (
                self.card_name(lost_card), attacker.render_displayname(),
            ))
            key = 'msg_uncle_won'
            args = (
                self.card_title(attacker_card), attack_skill, attacker_damage, attacker_max,
                self.card_title(defender_card), defense_skill, defender_damage, defender_max,
                attacker.render_displayname(), self.card_name(attacker_card), verb, defender.render_displayname(), self.card_name(defender_card),
            )
        else:
            await defender.send('msg_uncle_opponent_won', (
                self.card_name(lost_card), attacker.render_displayname(),
            ))
            key = 'msg_uncle_lost'
            args = (
                self.card_title(attacker_card), attack_skill, attacker_damage, attacker_max,
                self.card_title(defender_card), defense_skill, defender_damage, defender_max,
                defender.render_displayname(), self.card_name(defender_card), verb, attacker.render_displayname(), self.card_name(attacker_card),
            )
        return self.msg(key, args)

    @staticmethod
    def card_name(card: GDO_UncleUserCard) -> str:
        return GDO_UncleCard.table().get_by_id(card.gdo_val('uc_card')).gdo_val('card_nickname')

    @staticmethod
    def card_title(card: GDO_UncleUserCard) -> str:
        return GDO_UncleCard.table().get_by_id(card.gdo_val('uc_card')).render_name()
