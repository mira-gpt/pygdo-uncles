from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.uncles.GDT_UncleCard import GDT_UncleCard
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard
from gdo.uncles.method.uncle import uncle


class uncle_mob(Method):
    """A safe PvE confrontation against a generated WeChall-rank mob."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'unclemob'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_UncleCard('card').default_random_own_card()]

    def gdo_execute(self) -> GDT:
        user = self._env_user
        module = self.gdo_module()
        module.ensure_starter_deck(user)
        catalog_card = self.param_value('card')
        player_card = (
            catalog_card and GDO_UncleUserCard.table().get_by_vals({
                'uc_user': user.get_id(), 'uc_card': catalog_card.get_id(),
            })
        ) or module.random_card(user)
        if not player_card:
            return self.err('err_uncle_card_missing')

        mob = module.mob_card(user)
        if not mob:
            return self.err('err_uncle_no_cards')
        user.increase_setting('uncles_played')
        player_damage, mob_damage, attack_skill, defense_skill, player_max, mob_max = module.battle(player_card, mob)
        mob_name = mob.gdo_val('card_nickname')
        combat = (
            f'WCCClash: {uncle.card_title(player_card)}({attack_skill}:{player_damage}/{player_max}) '
            f'vs. {mob.render_name()}({defense_skill}:{mob_damage}/{mob_max})'
        )
        if player_damage < mob_damage:
            return self.msg('msg_uncle_mob_lost', (combat, mob_name, uncle.card_name(player_card)))
        user.increase_setting('uncles_won')
        module.add_card(user, mob)
        return self.msg('msg_uncle_mob_won', (combat, user.render_displayname(), uncle.card_name(player_card), mob_name))
