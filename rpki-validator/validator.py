#!/usr/bin/env python3
# PoC on-the-fly RPKI validation of announced IPv4 BGP prefixes
# requires https://github.com/NLnetLabs/routinator

import sys, lib, json

for line in sys.stdin:
	try:
		# parse the message
		msg = lib.parse_json(line)

		# validate each prefix against the origin AS
		origin = int(msg[5]["attrs"]["ASPATH"]["value"][-1])
		ok, fail = [], []
		for pfx in msg[5]["reach"]:
			ok.append(pfx) if lib.rpki_check(origin, pfx) \
				else fail.append(pfx)

		# all prefixes ok?
		if len(fail) == 0:
			raise # accept as-is

		# treat failed prefixes as withdrawn, like rfc7606
		msg[5]["reach"] = ok
		msg[5]["unreach"].extend(fail)
		print(json.dumps(msg), flush=True) # modify the original message
	except:
		print(line, end="", flush=True)    # accept the message as-is
