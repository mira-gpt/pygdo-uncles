# pygdo-uncles

Collectible WeChall-player cards for PyGDO.

`GDO_UncleCard` is the canonical card-ID-to-nickname mapping table;
`GDO_UncleUserCard` stores unique player/card ownership pairs. Cards carry Crypto, Stegano, Programming, Exploit, Math, and Info ratings. The
catalog in `cards.toml` is fixed: card ID 1 is always `ray`, with immutable
stats. Fresh players receive ten low-rating starter cards from ranks 100–200.
Use `$uncle <user> <card>` to select an attacking card by ID or nickname; the
defender is assigned a random card. The fighting cards exchange hands after the
round. `$uncle.mob <card>` provides a safe PvE route: mobs normally roll rank
50–100, with a rare stronger spawn, and never take a card,
but wins can yield a rare unowned top-card. Fights use a compact FFXIV-like
potency, mitigation, critical-hit, direct-hit, and variance calculation.
`$uncles` displays your collection.
