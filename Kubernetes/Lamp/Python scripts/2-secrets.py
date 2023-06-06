import base64
import requests
import json

username = "klant1"
password = "test12345"
hostname = "klant1"


# function to create base64encoded version of a string to send to rancher for the creation of the secrets.
def plaintext_to_base64(string):
    encoded_bytes = base64.b64encode(string.encode("ascii"))
    coded_string_ascii = encoded_bytes.decode("ascii")

    return coded_string_ascii


username_b64 = plaintext_to_base64(username)
password_b64 = plaintext_to_base64(password)


url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/secrets"

payload = json.dumps({
    "type": "Opaque",
    "metadata": {
        "namespace": hostname,
        "name": hostname
    },
    "_type": "Opaque",
    "data": {
        "password": password_b64,
        "username": username_b64
    }
})
headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
    'Origin': 'https://172.26.51.0',
    'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/secret/create',
    'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)


