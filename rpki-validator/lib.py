import json
import requests

# is_invalid returns true iff prefix+origin is RPKI invalid
def is_invalid(ROOT: str, origin: int, prefix: str) -> bool:
	url = f"{ROOT}/api/v1/validity/{origin}/{prefix}"
	response = requests.get(url)
	response.raise_for_status()
	result = response.json()
	return result["validated_route"]["validity"]["state"] == "invalid"


# msg_decode parses and checks if a message announces IPv4 prefixes with a sane origin
def msg_from_json(line: str) -> tuple[object, int]:
	try:
		msg = json.loads(line)
		if msg[4] != "UPDATE":
			raise Exception
		elif len(msg[5]["reach"]) == 0:
			raise Exception
		elif "unreach" not in msg[5]:
			msg[5]["unreach"] = list() # in case it's needed later
		return msg, int(msg[5]["attrs"]["ASPATH"]["value"][-1])
	except:
		return (None, 0)

def msg_accept(line: str):
	print(line, flush=True)
	
def msg_rewrite(msg: object):
	print(json.dumps(msg), flush=True)
