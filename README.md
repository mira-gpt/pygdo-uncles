# pygdo-uncles

Collectible WeChall-player cards for PyGDO.

`GDO_UncleCard` is the canonical card-ID-to-nickname mapping table;
`GDO_UncleUserCard` stores unique player/card ownership pairs. Cards carry Crypto, Stegano, Programming, Exploit, Math, and Info ratings. The
catalog in `uncle.py` is fixed: each row maps one global top-100 WeChall name
to its permanent ID, rank and six immutable stats. Fresh players receive one
random starter card from ranks 1–50; a player with no cards receives one again.
Use `$uncle <user> <card>` to select an attacking card by ID or nickname; the
defender is assigned a random card. The fighting cards exchange hands after the
round. Each confrontation randomly draws one of all six stats; its paired
opposite defends: Crypto↔Stegano, Math↔Programming, Exploit↔Info.
The lower WeChall rank is favoured by rolling `rand(3, level)`; the other card
rolls `rand(1, level)`.
`$uncle.mob <card>` challenges a real, unowned rank-50–100 card. Winning adds
that exact card to the deck; mobs never take a card. WeChall ranks 1–50 have
the clearly higher random stat tier; ranks 51–100 are the lower tier.
`$uncles` displays your collection.
