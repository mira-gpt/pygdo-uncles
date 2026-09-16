from random import choice, randint, uniform
from pathlib import Path
import tomllib

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.GDO_Module import GDO_Module
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_UInt import GDT_UInt
from gdo.uncles.UNC_Card import UNC_Card
from gdo.uncles.UNC_UserCard import UNC_UserCard


class module_uncles(GDO_Module):
    """WeChall player cards: starter decks, confrontations, and card stakes."""

    def gdo_dependencies(self) -> list:
        return ['core', 'table', 'user']

    def gdo_classes(self) -> list[type[GDO]]:
        return [UNC_Card, UNC_UserCard]

    def gdo_user_config(self) -> list[GDT]:
        return [GDT_Bool('unc_starter_deck').not_null().initial('0').hidden()]

    def gdo_module_config(self) -> list[GDT]:
        return [GDT_UInt('unc_rare_drop').not_null().min(0).max(100).initial('5')]

    async def gdo_install(self):
        self.seed_starter_cards()

    def seed_starter_cards(self):
        catalog = Path(__file__).with_name('cards.toml')
        for card in tomllib.loads(catalog.read_text())['card']:
            UNC_Card.blank(card).soft_replace()

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
        for card in UNC_Card.table().select().where('card_rank >= 100').exec().fetch_all():
            self.add_card(user, card)
        user.save_setting('unc_starter_deck', '1')

    def random_card(self, user: GDO_User) -> UNC_UserCard | None:
        cards = UNC_UserCard.table().select().where(f'uc_user={user.get_id()} AND uc_amount>0').exec().fetch_all()
        return cards[randint(0, len(cards) - 1)] if cards else None

    @staticmethod
    def card_stats(card: UNC_UserCard) -> dict[str, int]:
        source = UNC_Card.table().get_by_id(card.gdo_val('uc_card'))
        return {
            key: int(source.gdo_val(f'card_{key}'))
            for key in ('crypto', 'stegano', 'programming', 'exploit', 'math', 'info', 'rating')
        }

    def battle(self, attacker: UNC_UserCard, defender: UNC_UserCard) -> tuple[int, bool, bool]:
        """FFXIV-like card damage: potency, main stat, mitigation, crit, direct hit, variance."""
        attack = self.card_stats(attacker)
        defense = self.card_stats(defender)
        potency = 100 + attack['crypto'] + attack['stegano']
        main_stat = attack['programming'] + attack['exploit'] + attack['math'] + attack['info']
        weapon_damage = attack['rating'] / 10
        determination = attack['math']
        mitigation = defense['crypto'] + defense['stegano'] + defense['info']
        damage = potency * (100 + main_stat) / 100
        damage *= (100 + weapon_damage + determination / 2) / 100
        damage *= 1000 / (1000 + mitigation * 4)
        critical = randint(1, 100) <= min(50, 5 + attack['exploit'] // 2)
        direct = randint(1, 100) <= min(50, 5 + attack['programming'] // 2)
        if critical:
            damage *= 1.4 + attack['exploit'] / 1000
        if direct:
            damage *= 1.25
        return max(1, round(damage * uniform(0.95, 1.05))), critical, direct

    def transfer_card(self, card: UNC_UserCard, winner: GDO_User):
        card.increase('uc_amount', -1)
        self.add_card(winner, UNC_Card.table().get_by_id(card.gdo_val('uc_card')))
