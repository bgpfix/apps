import sys
import json
import requests

# routinator HTTP validity check URL
URL = "http://127.0.0.1:31339/api/v1/validity"

# rpki_check returns false iff prefix+origin is RPKI invalid
def rpki_check(origin: int, prefix: str) -> bool:
	try:
		url = f"{URL}/{origin}/{prefix}"
		response = requests.get(url)
		response.raise_for_status()
		result = response.json()
		return result["validated_route"]["validity"]["state"] != "invalid"
	except Exception as err:
		print(err, file=sys.stderr)
		raise # pass the exception

# parse_json parses a message and checks if it announces IPv4 prefixes
def parse_json(line: str) -> object:
	msg = json.loads(line)
	if msg[4] != "UPDATE" or len(msg[5]["reach"]) == 0:
		raise Exception
	if "unreach" not in msg[5]:
		msg[5]["unreach"] = list() # in case it's needed later
	return msg
