import requests
import json

url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/networking.k8s.io.ingresses"

hostname = "klant1"


payload = json.dumps({
    "type": "networking.k8s.io.ingress",
    "metadata": {
        "namespace": hostname,
        "annotations": {
            "kubernetes.io/ingress.class": "nginx",
            "cert-manager.io/cluster-issuer": "wp-prod-issuer"
        },
        "name": "webserver-"+hostname
    },
    "spec": {
        "rules": [
            {
                "host": "www."+hostname+".motoyohosting.uk",
                "http": {
                    "paths": [
                        {
                            "backend": {
                                "service": {
                                    "port": {
                                        "number": 80
                                    },
                                    "name": "webserver-"+hostname
                                }
                            },
                            "path": "/",
                            "pathType": "Prefix"
                        }
                    ]
                }
            }
        ],
        "backend": {},
        "tls": [
            {
                "hosts": [
                    "www."+hostname+".motoyohosting.uk"
                ],
                "secretName": "webserver-"+hostname+"-tls"
            }
        ]
    },
    "cacheObject": {
        "useNestedBackendField": True,
        "showPathType": True
    }
})
headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
    'Origin': 'https://172.26.51.0',
    'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/networking.k8s.io.ingress/create',
    'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.status_code)
