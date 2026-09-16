from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_String import GDT_String
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard
from gdo.uncles.method.uncle import uncle


class uncle_mob(Method):
    """A safe PvE confrontation against a generated WeChall-rank mob."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'uncle.mob'

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_String('card').not_null().maxlen(64)]

    def gdo_execute(self) -> GDT:
        user = self._env_user
        module = self.gdo_module()
        module.ensure_starter_deck(user)
        catalog_card = uncle.get_card(self.param_val('card'))
        player_card = catalog_card and GDO_UncleUserCard.table().get_by_vals({
            'uc_user': user.get_id(), 'uc_card': catalog_card.get_id(),
        })
        if not player_card:
            return self.err('err_uncle_card_missing')

        mob = module.mob_card()
        player_damage, critical, direct = module.battle(player_card, mob)
        mob_damage, _, _ = module.battle(mob, player_card)
        mob_name = mob.gdo_val('card_nickname')
        if player_damage < mob_damage:
            return self.msg('msg_uncle_mob_lost', (mob_name, player_damage, mob_damage))
        drop = module.rare_drop(user)
        flags = (' critical' if critical else '') + (' direct' if direct else '')
        key = 'msg_uncle_mob_won_drop' if drop else 'msg_uncle_mob_won'
        args = (mob_name, player_damage, mob_damage, flags)
        if drop:
            args += (drop.gdo_val('card_nickname'),)
        return self.msg(key, args)
