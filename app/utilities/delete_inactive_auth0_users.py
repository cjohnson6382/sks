import requests
import hashlib
import json

from jose import jwk
from jose import jws

client_id = "02sOpNNmZkx6HeLRTM5dHp0Qyjd40fFW"
client_secret = "TBziVKkjIqydBPVnpkb6iNpY67WJER1GjA_Qj2DqeqPGNbKBEFlOy2iujcrwN8UJ"

url = "https://cjohnson6382.auth0.com/oauth/token"
data = {
	"client_id": client_id,
	"client_secret": client_secret,
	"audience": "https://cjohnson6382.auth0.com/api/v2/",
	"grant_type": "client_credentials"
}

r = requests.post(url, data=data)

resp_json = r.json()
access_token = resp_json['access_token']

url = "https://cjohnson6382.auth0.com/api/v2/clients"
headers = {"Authorization": "Bearer %s" % access_token }
r = requests.get(url, headers=headers)
resp_json = r.json()
auth0_active_users = [ { "client_id": user.get("client_id"), "name": user.get("name") } for user in resp_json]

delete_names = [
	"leo@rosettablock.com",
	"jason@rosettablock.com",
	"chris@rosettablock.com",
	"cjohnson6382@gmail.com",
	"test_user",
	"target"
]

inactive_users = [user for user in auth0_active_users if any([a in user.get("name") for a in delete_names])]

deleted_users = []
failed_deletes = []
for user in inactive_users:
	final_url = url + "/" + user.get("client_id")
	r = requests.delete(final_url, headers=headers)
	deleted_users.append(user) if r.status_code == 204 else failed_deletes.append(user)

print({ "deleted_users": deleted_users, "failed_deletes": failed_deletes })