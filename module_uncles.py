from random import choice, randint, uniform
from pathlib import Path
import tomllib

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.GDO_Module import GDO_Module
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_UInt import GDT_UInt
from gdo.uncles.GDO_UncleCard import GDO_UncleCard
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard


class module_uncles(GDO_Module):
    """WeChall player cards: starter decks, confrontations, and card stakes."""

    def gdo_dependencies(self) -> list:
        return ['core', 'table', 'user']

    def gdo_classes(self) -> list[type[GDO]]:
        return [GDO_UncleCard, GDO_UncleUserCard]

    def gdo_user_config(self) -> list[GDT]:
        return [GDT_Bool('unc_starter_deck').not_null().initial('0').hidden()]

    def gdo_module_config(self) -> list[GDT]:
        return [GDT_UInt('unc_rare_drop').not_null().min(0).max(100).initial('5')]

    async def gdo_install(self):
        self.seed_starter_cards()

    def seed_starter_cards(self):
        catalog = Path(__file__).with_name('cards.toml')
        for card in tomllib.loads(catalog.read_text())['card']:
            GDO_UncleCard.blank(card).soft_replace()

    def rare_drop(self, user: GDO_User) -> GDO_UncleCard | None:
        if randint(1, 100) > self.get_config_value('unc_rare_drop'):
            return None
        cards = GDO_UncleCard.table().select().where('card_rank <= 100').exec().fetch_all()
        cards = [card for card in cards if not GDO_UncleUserCard.table().get_by_vals({'uc_user': user.get_id(), 'uc_card': card.get_id()})]
        card = choice(cards) if cards else None
        if card:
            self.add_card(user, card)
        return card

    @staticmethod
    def add_card(user: GDO_User, card: GDO_UncleCard):
        if not GDO_UncleUserCard.table().get_by_vals({'uc_user': user.get_id(), 'uc_card': card.get_id()}):
            GDO_UncleUserCard.blank({
                'uc_user': user.get_id(),
                'uc_card': card.get_id(),
            }).insert()

    def ensure_starter_deck(self, user: GDO_User):
        if user.get_setting_value('unc_starter_deck'):
            return
        for card in GDO_UncleCard.table().select().where('card_rank >= 100').exec().fetch_all():
            self.add_card(user, card)
        user.save_setting('unc_starter_deck', '1')

    def random_card(self, user: GDO_User) -> GDO_UncleUserCard | None:
        cards = GDO_UncleUserCard.table().select().where(f'uc_user={user.get_id()}').exec().fetch_all()
        return cards[randint(0, len(cards) - 1)] if cards else None

    @staticmethod
    def card_stats(card: GDO_UncleUserCard | GDO_UncleCard) -> dict[str, int]:
        source = card if isinstance(card, GDO_UncleCard) else GDO_UncleCard.table().get_by_id(card.gdo_val('uc_card'))
        return {
            key: int(source.gdo_val(f'card_{key}'))
            for key in ('crypto', 'stegano', 'programming', 'exploit', 'math', 'info', 'rating')
        }

    def battle(self, attacker: GDO_UncleUserCard | GDO_UncleCard, defender: GDO_UncleUserCard | GDO_UncleCard) -> tuple[int, bool, bool]:
        """FFXIV-like damage over the three WeChall offence/defence stat pairs."""
        attack = self.card_stats(attacker)
        defense = self.card_stats(defender)
        # The first stat of every pair attacks the second stat of its opponent.
        # Crypto -> Stegano, Math -> Programming, Exploit -> Infosec.
        offence = attack['crypto'] + attack['math'] + attack['exploit']
        mitigation = defense['stegano'] + defense['programming'] + defense['info']
        potency = 100 + offence
        weapon_damage = attack['rating'] / 10
        damage = potency * (100 + weapon_damage) / 100
        damage *= 1000 / (1000 + mitigation * 4)
        critical = randint(1, 100) <= min(50, 5 + attack['exploit'] // 2)
        direct = randint(1, 100) <= min(50, 5 + attack['math'] // 2)
        if critical:
            damage *= 1.4 + attack['exploit'] / 1000
        if direct:
            damage *= 1.25
        return max(1, round(damage * uniform(0.95, 1.05))), critical, direct

    @staticmethod
    def mob_card() -> GDO_UncleCard:
        """Most mobs are rank 50-100; a 5% roll creates a precious high-rank encounter."""
        rank = randint(1, 49) if randint(1, 100) <= 5 else randint(50, 100)
        power = 105 - rank
        return GDO_UncleCard.blank({
            'card_id': 0,
            'card_nickname': f'Rank {rank} mob',
            'card_rank': rank,
            'card_crypto': power,
            'card_stegano': power,
            'card_programming': power,
            'card_exploit': power,
            'card_math': power,
            'card_info': power,
            'card_rating': power * 6,
        })

    @staticmethod
    def exchange_cards(a: GDO_UncleUserCard, b: GDO_UncleUserCard):
        a_card, b_card = a.gdo_val('uc_card'), b.gdo_val('uc_card')
        if a_card != b_card:
            a.save_val('uc_card', b_card)
            b.save_val('uc_card', a_card)
