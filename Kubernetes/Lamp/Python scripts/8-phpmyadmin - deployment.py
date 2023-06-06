import requests
import json

url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

hostname = "klant1"


payload = json.dumps({
    "type": "apps.deployment",
    "metadata": {
        "namespace": hostname,
        "labels": {
            "component": "phpmyadmin-"+hostname,
            "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-phpmyadmin"
        },
        "name": "phpmyadmin-"+hostname
    },
    "spec": {
        "replicas": 1,
        "template": {
            "spec": {
                "restartPolicy": "Always",
                "containers": [
                    {
                        "imagePullPolicy": "Always",
                        "name": "phpmyadmin",
                        "volumeMounts": [
                            {
                                "name": "phpmyadmin-"+hostname,
                                "mountPath": "/usr/local/etc/php/conf.d/php-phpmyadmin.ini"
                            }
                        ],
                        "image": "phpmyadmin",
                        "ports": [
                            {
                                "name": "80tcp",
                                "expose": True,
                                "protocol": "TCP",
                                "containerPort": 80,
                                "hostPort": None,
                                "hostIP": None,
                                "_serviceType": "",
                                "_ipam": "dhcp"
                            },
                            {
                                "name": "443tcp",
                                "expose": True,
                                "protocol": "TCP",
                                "containerPort": 443,
                                "hostPort": None,
                                "hostIP": None,
                                "_serviceType": "",
                                "_ipam": "dhcp"
                            }
                        ],
                        "env": [
                            {
                                "name": "MYSQL_PASSWORD",
                                "valueFrom": {
                                    "secretKeyRef": {
                                        "key": "password",
                                        "name": hostname,
                                        "optional": False
                                    }
                                }
                            },
                            {
                                "name": "MYSQL_ROOT_PASSWORD",
                                "valueFrom": {
                                    "secretKeyRef": {
                                        "key": "password",
                                        "name": hostname,
                                        "optional": False
                                    }
                                }
                            },
                            {
                                "name": "MYSQL_USER",
                                "valueFrom": {
                                    "secretKeyRef": {
                                        "key": "username",
                                        "name": hostname,
                                        "optional": False
                                    }
                                }
                            },
                            {
                                "name": "PMA_HOST",
                                "value": "database-"+hostname
                            },
                            {
                                "name": "PMA_PASSWORD",
                                "valueFrom": {
                                    "secretKeyRef": {
                                        "key": "password",
                                        "name": hostname,
                                        "optional": False
                                    }
                                }
                            },
                            {
                                "name": "PMA_PORT",
                                "value": "3306"
                            }
                        ],
                        "envFrom": [],
                        "__active": True
                    }
                ],
                "initContainers": [],
                "imagePullSecrets": [],
                "volumes": [
                    {
                        "_type": "persistentVolumeClaim",
                        "persistentVolumeClaim": {
                            "claimName": "phpmyadmin-"+hostname
                        },
                        "name": "phpmyadmin-"+hostname,
                        "__newPvc": {
                            "type": "persistentvolumeclaim",
                            "metadata": {
                                "namespace": hostname
                            },
                            "spec": {
                                "accessModes": [],
                                "storageClassName": "",
                                "volumeName": "",
                                "resources": {
                                    "requests": {
                                        "storage": None
                                    }
                                }
                            }
                        }
                    }
                ],
                "affinity": {}
            },
            "metadata": {
                "labels": {
                    "component": "phpmyadmin-"+hostname,
                    "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-phpmyadmin"
                }
            }
        },
        "selector": {
            "matchLabels": {
                "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-phpmyadmin"
            }
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
    'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/apps.deployment/create',
    'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.status_code)
