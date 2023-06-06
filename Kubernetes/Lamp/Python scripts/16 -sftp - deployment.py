import requests
import json

url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

hostname = "klant1"

payload = json.dumps({
    "type": "apps.deployment",
    "metadata": {
        "namespace": hostname,
        "annotations": {
            "deployment.kubernetes.io": "1"
        },
        "labels": {
            "component": "sftp-"+hostname,
            "workload.user.cattle.io/workloadselector": "apps.deployment-klant1-sftp-klant1"
        },
        "name": "sftp-"+hostname
    },
    "spec": {
        "replicas": 1,
        "template": {
            "spec": {
                "restartPolicy": "Always",
                "containers": [
                    {
                        "imagePullPolicy": "Always",
                        "name": "sftp-"+hostname,
                        "volumeMounts": [
                            {
                                "name": "webserver-"+hostname,
                                "mountPath": "/home/"+hostname
                            },
                            {
                                "name": "users-"+hostname,
                                "mountPath": "/etc/sftp"
                            }
                        ],
                        "__active": True,
                        "image": "atmoz/sftp:latest",
                        "ports": [
                            {
                                "name": "22tcp",
                                "expose": True,
                                "protocol": "TCP",
                                "containerPort": 22,
                                "hostPort": None,
                                "hostIP": None,
                                "_serviceType": "",
                                "_ipam": "dhcp"
                            }
                        ]
                    }
                ],
                "initContainers": [],
                "imagePullSecrets": [],
                "volumes": [
                    {
                        "_type": "persistentVolumeClaim",
                        "persistentVolumeClaim": {
                            "claimName": "webserver-"+hostname
                        },
                        "name": "webserver-"+hostname,
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
                    },
                    {
                        "_type": "configMap",
                        "configMap": {
                            "name": "sftp-user-config-"+hostname
                        },
                        "name": "users-"+hostname
                    }
                ],
                "affinity": {}
            },
            "metadata": {
                "labels": {
                    "component": "sftp-"+hostname,
                    "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-sftp-"+hostname
                }
            }
        },
        "selector": {
            "matchLabels": {
                "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-sftp-"+hostname
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
