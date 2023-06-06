import requests
import json

url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/services"
hostname = "klant2"

payload = json.dumps({
    "type": "service",
    "metadata": {
        "namespace": hostname,
        "name": "wordpress-"+hostname
    },
    "spec": {
        "ports": [
            {
                "port": 80,
                "protocol": "TCP",
                "targetPort": 80
            }
        ],
        "sessionAffinity": "None",
        "type": "ClusterIP",
        "selector": {
            "app": "wordpress",
            "tier": "web"
        }
    }
})
headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
    'Origin': 'https://172.26.51.0',
    'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/service/create',
    'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.status_code)