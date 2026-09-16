from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Result import ResultType
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_String import GDT_String
from gdo.uncles.GDO_UncleUserCard import GDO_UncleUserCard


class unclestats(Method):
    """Rank Card Clash players by the number of cards they own."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'unclestats'

    def gdo_method_hidden(self) -> bool:
        return True

    def gdo_execute(self) -> GDT:
        result = GDO_UncleUserCard.table().select(
            'uc_user, COUNT(*) AS unc_cards'
        ).group('uc_user').order('unc_cards DESC, uc_user ASC').exec()
        ranking = []
        for place, row in enumerate(result.iter(ResultType.ASSOC), 1):
            user = GDO_User.table().get_by_id(row['uc_user'])
            ranking.append(f"{place}-{user.render_name()} ({row['unc_cards']})")
        return GDT_String('result').text('msg_unclestats', (', '.join(ranking),))
