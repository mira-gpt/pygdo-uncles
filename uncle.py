"""Fixed WeChall Card Clash catalog, based on the global top-100 ranking."""

from random import Random


TOP_100 = (
    'rayaseiren', 'dloser', 'jusb3', 'jablonskim', 'ytbjplh', 'tehron', 'Caesum', 'tenflo', 'sisyang', 'Xaav',
    'noother', 'phoenix1204', 'lordOric', 'thefinder', 'Akorlith', 'xseris', 'TheHiveMind', 'quangntenemy', 'wekito', 'MrKaLiMaN',
    'yachoor', 'j_m', 'kumaus', 'Hertz', 'nurfed', 'mathpseudo', 'madbat2', 'tripleedged', 'livinskull', 'flipp',
    'destiny2097', 'love0day', 'HvT', 'cheerfulbull', 'S0410N3', 'Fox1337', 'Spaulding', 'bashrc', 'maf-ia', 'Munto',
    'criple_ripper', 'r777_', 'Jos18', 'Mawekl', 'martek', 'Ne0Lux-C1Ph3r', 'AhnMo', 'Mart', 'neoxquick', 'faust',
    'smutley', 'harvestsnow', 'Undr', 'Cerades', 'kr1shn4murt1', 'steven18', 'mirmo', 'paipai', 'Garfield', 'gnumpty',
    'sinan', 'peterkodo', 'Holographic', 'bolofecal', 'r_karoly', 'TaRaSS', 'SatUrN', 'rubiya', 'alucardo', 'sysfail',
    'kwisatz', 'hds', 'x64', 'MrStorm', 'kismet', 'xp45g', 'LoneWolf219', 'korkinsson', 'cls', 'makler2004',
    'shadum', 'stypr', 'matrixman', 'hervas', 'bagy', 'rijman', 'MuffinX', 'Kender', 'jjk', 'Chaosdreamer',
    'Rex_Mundi', 'Celcious', 'Elian', 'lesnik7', 'Mtuc', 'TEO', 'Stupefy', 'totoiste', 'saiwa', 'UnTaran',
)


def cards() -> list[dict[str, int | str]]:
    """Return one immutable row per ranked player: ID, name, rank and six stats."""
    rows = []
    rng = Random('WeChall Card Clash Top 100')
    for card_id, username in enumerate(TOP_100, 1):
        # WeChall ranks 1-50 are the stronger card tier.
        low, high = (3, 10) if card_id <= 50 else (1, 5)
        stats = {
            'crypto': rng.randint(low, high),
            'stegano': rng.randint(low, high),
            'programming': rng.randint(low, high),
            'exploit': rng.randint(low, high),
            'math': rng.randint(low, high),
            'info': rng.randint(low, high),
        }
        rows.append({
            'id': card_id,
            'username': username,
            'rank': card_id,
            'followers': rng.randint(0, 100),
            **stats,
        })
    return rows
