from random import choice, randint

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.GDO_Module import GDO_Module
from gdo.core.GDO_User import GDO_User
from gdo.core.GDO_UserSetting import GDO_UserSetting
from gdo.core.GDT_UInt import GDT_UInt
from gdo.date.GDT_Duration import GDT_Duration
from gdo.uncles.GDO_UncleCard import GDO_UncleCard
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard
from gdo.uncles.uncle import cards


UNCLE_VERBS = (
    'outcodes',
    'outsmarts',
    'encrypts',
    'debugs',
    'decompiles',
    'stack-smashes',
    'packet-sniffs',
    'rubber-ducks',
    'segfaults',
    'hash-cracks',
)


class module_uncles(GDO_Module):
    """WeChall player cards: starter decks, confrontations, and card stakes."""

    def gdo_dependencies(self) -> list:
        return ['core', 'table', 'user']

    def gdo_classes(self) -> list[type[GDO]]:
        return [GDO_UncleCard, GDO_UncleUserCard]

    def gdo_user_config(self) -> list[GDT]:
        return [
            GDT_UInt('uncles_played').not_null().initial('0').hidden(),
            GDT_UInt('uncles_won').not_null().initial('0').hidden(),
            GDT_UInt('uncle_last_human').not_null().initial('0').hidden(),
        ]

    def gdo_module_config(self) -> list[GDT]:
        return [GDT_Duration('uncle_cooldown').not_null().min(0).initial('10m')]

    async def gdo_install(self):
        self.seed_starter_cards()

    def seed_starter_cards(self):
        if GDO_UncleCard.table().count_where() >= 100:
            return
        for card in cards():
            row = {
                'card_id': card['id'],
                'card_nickname': card['username'],
                'card_rank': card['rank'],
                'card_followers': card['followers'],
                **{f'card_{key}': card[key] for key in ('crypto', 'stegano', 'programming', 'exploit', 'math', 'info')},
            }
            row['card_rating'] = sum(row[f'card_{key}'] for key in ('crypto', 'stegano', 'programming', 'exploit', 'math', 'info'))
            GDO_UncleCard.blank({key: str(value) for key, value in row.items()}).soft_replace()

    @staticmethod
    def add_card(user: GDO_User, card: GDO_UncleCard):
        if not GDO_UncleUserCard.table().get_by_vals({'uc_user': user.get_id(), 'uc_card': card.get_id()}):
            GDO_UncleUserCard.blank({
                'uc_user': user.get_id(),
                'uc_card': card.get_id(),
            }).insert()

    def ensure_starter_deck(self, user: GDO_User):
        if GDO_UncleUserCard.table().get_by_vals({'uc_user': user.get_id()}):
            return
        card = GDO_UncleCard.table().select().where(
            'card_rank BETWEEN 1 AND 50'
        ).order('RAND()').first().exec().fetch_object()
        self.add_card(user, card)

    def wipe_game(self):
        """Reset Card Clash data without touching users or any other module."""
        GDO_UncleUserCard.table().delete_where('1')
        GDO_UncleCard.table().delete_where('1')
        GDO_UserSetting.table().delete_where(
            "uset_key IN ('uncles_played', 'uncles_won', 'uncle_last_human', 'unc_starter_deck')"
        )
        self.seed_starter_cards()

    def random_card(self, user: GDO_User) -> GDO_UncleUserCard | None:
        cards = GDO_UncleUserCard.table().select().where(f'uc_user={user.get_id()}').exec().fetch_all()
        return cards[randint(0, len(cards) - 1)] if cards else None

    @staticmethod
    def verb() -> str:
        return choice(UNCLE_VERBS)

    @staticmethod
    def card_stats(card: GDO_UncleUserCard | GDO_UncleCard) -> dict[str, int]:
        source = card if isinstance(card, GDO_UncleCard) else GDO_UncleCard.table().get_by_id(card.gdo_val('uc_card'))
        return {
            key: int(source.gdo_val(f'card_{key}'))
            for key in ('rank', 'followers', 'crypto', 'stegano', 'programming', 'exploit', 'math', 'info', 'rating')
        }

    def battle(self, attacker: GDO_UncleUserCard | GDO_UncleCard, defender: GDO_UncleUserCard | GDO_UncleCard) -> tuple[int, int, str, str, int, int]:
        """Roll one offensive discipline against its paired defensive discipline."""
        attack = self.card_stats(attacker)
        defense = self.card_stats(defender)
        # One of all eight stats is tested per confrontation. Its matching
        # counterpart on the defender card is the sole defensive value.
        attack_key, defense_key = choice((
            ('rank', 'followers'),
            ('followers', 'rank'),
            ('crypto', 'stegano'),
            ('stegano', 'crypto'),
            ('math', 'programming'),
            ('programming', 'math'),
            ('exploit', 'info'),
            ('info', 'exploit'),
        ))
        attack_level = attack[attack_key]
        defense_level = defense[defense_key]
        # A lower global rank is stronger. Keep the displayed rank human
        # readable while turning it into a positive fight level for the roll.
        if attack_key == 'rank':
            attack_level = 100 - attack_level
        if defense_key == 'rank':
            defense_level = 100 - defense_level
        attacker_rank = int((attacker if isinstance(attacker, GDO_UncleCard) else GDO_UncleCard.table().get_by_id(attacker.gdo_val('uc_card'))).gdo_val('card_rank'))
        defender_rank = int((defender if isinstance(defender, GDO_UncleCard) else GDO_UncleCard.table().get_by_id(defender.gdo_val('uc_card'))).gdo_val('card_rank'))
        attacker_better = attacker_rank < defender_rank
        defender_better = defender_rank < attacker_rank
        attacker_min = 1 + int(attacker_better)
        defender_min = 1 + int(defender_better)
        attacker_max = attack_level + (2 if attacker_better else 0)
        defender_max = defense_level + (2 if defender_better else 0)
        attack_roll = randint(attacker_min, attacker_max) if attacker_max >= attacker_min else attack_level
        defense_roll = randint(defender_min, defender_max) if defender_max >= defender_min else defense_level
        return attack_roll, defense_roll, attack_key, defense_key, attacker_max, defender_max

    def mob_card(self, user: GDO_User) -> GDO_UncleCard | None:
        """Mobs drop one random lower card the user does not already own."""
        cards = GDO_UncleCard.table()
        ownership = GDO_UncleUserCard.table()
        return cards.select().where(
            f'card_rank BETWEEN 51 AND 100 AND card_id NOT IN ('
            f'SELECT uc_card FROM {ownership.gdo_table_name()} WHERE uc_user={user.get_id()})'
        ).order('RAND()').limit(1).first().exec().fetch_object()

    def claim_card(self, winner: GDO_User, loser_card: GDO_UncleUserCard):
        """The loser transfers their card; combat itself never creates cards."""
        card = GDO_UncleCard.table().get_by_id(loser_card.gdo_val('uc_card'))
        loser_card.delete()
        self.add_card(winner, card)
