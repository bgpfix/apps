#!/usr/bin/env python3
# PoC on-the-fly RPKI validation of announced IPv4 BGP prefixes
# requires https://github.com/NLnetLabs/routinator

import sys
import lib

# routinator HTTP service root URL
URL = "http://127.0.0.1:31339"

for line in sys.stdin:
	# parse or accept line as-is
	line = line.strip()
	msg, origin = lib.msg_from_json(line)
	if not msg:
		lib.msg_accept(line)
		continue

	# validate each prefix
	ok, invalid = [], []
	for pfx in msg[5]["reach"]:
		invalid.append(pfx) if lib.is_invalid(URL, origin, pfx) else ok.append(pfx)

	# all prefixes good? accept line as-is
	if len(invalid) == 0:
		lib.msg_accept(line)
		continue

	# treat invalid prefixes as withdrawn, rfc7606 style
	msg[5]["reach"] = ok
	msg[5]["unreach"].extend(invalid)
	lib.msg_rewrite(msg)
