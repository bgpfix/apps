#!/usr/bin/env python3
# PoC on-the-fly RPKI validation of announced IPv4 BGP prefixes
# requires https://github.com/NLnetLabs/routinator

import sys, lib, json

for line in sys.stdin:
	try:
		msg = lib.parse_json(line)

		# validate prefixes vs. the origin AS
		origin = int(msg[5]["attrs"]["ASPATH"]["value"][-1])
		ok, fail = [], []
		for pfx in msg[5]["reach"]:
			ok.append(pfx) if lib.rpki_check(origin, pfx) \
				else fail.append(pfx)

		# treat invalid prefixes as withdrawn, like rfc7606
		if len(fail) > 0:
			msg[5]["reach"] = ok
			msg[5]["unreach"].extend(fail)
			print(json.dumps(msg), flush=True) # rewrite msg
		else:
			raise # accept as-is
	except:
		print(line, end="", flush=True)
