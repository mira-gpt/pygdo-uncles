# pygdo-uncles

Collectible WeChall-player cards for PyGDO.

Cards carry Crypto, Stegano, Programming, Exploit, Math, and Info ratings. The
catalog in `cards.toml` is fixed: card ID 1 is always `ray`, with immutable
stats. Fresh players receive ten low-rating starter cards from ranks 100–200.
Use `$uncle <user> <card>` to select an attacking card; the defender
is assigned a random card. Fights use a compact FFXIV-like potency, mitigation,
critical-hit, direct-hit, and variance calculation. The loser stakes their card.
`$uncles` displays your collection.
