import requests
import json


# variables to assign before deploying
hostname = "klant1"




url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

payload = json.dumps({
    "type": "apps.deployment",
    "metadata": {
        "namespace": hostname,
        "labels": {
            "component": "database-"+hostname,
            "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-database"
        },
        "name": "database-"+hostname
    },
    "spec": {
        "replicas": 1,
        "template": {
            "spec": {
                "restartPolicy": "Always",
                "containers": [
                    {
                        "imagePullPolicy": "Always",
                        "name": "mysql",
                        "volumeMounts": [
                            {
                                "name": "database-"+hostname,
                                "mountPath": "/var/lib/mysql"
                            }
                        ],
                        "__active": True,
                        "image": "mysql:latest",
                        "ports": [
                            {
                                "name": "mysql",
                                "expose": True,
                                "protocol": "TCP",
                                "containerPort": 3306,
                                "hostPort": None,
                                "hostIP": None,
                                "_serviceType": "",
                                "_ipam": "dhcp"
                            }
                        ],
                        "env": [
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
                                "name": "MYSQL_DATABASE",
                                "valueFrom": {
                                    "secretKeyRef": {
                                        "key": "username",
                                        "name": hostname,
                                        "optional": False
                                    }
                                }
                            }
                        ],
                        "envFrom": []
                    }
                ],
                "initContainers": [],
                "imagePullSecrets": [],
                "volumes": [
                    {
                        "_type": "persistentVolumeClaim",
                        "persistentVolumeClaim": {
                            "claimName": "database-"+hostname
                        },
                        "name": "database-"+hostname,
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
                    "component": "database-"+hostname,
                    "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-database"
                }
            }
        },
        "selector": {
            "matchLabels": {
                "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-database"
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
