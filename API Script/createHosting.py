# imports of different modules

import requests
import json
import random
import base64
import time

# functions to create individual API calls towards the rancher instance

# create namespace

def create_namespace(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/namespaces"
    payload = json.dumps({
        "type": "namespace",
        "metadata": {
            "annotations": {
                "field.cattle.io/containerDefaultResourceLimit": "{}"
            },
            "name": hostname
        },
        "disableOpenApiValidation": False
        })
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
        'Origin': 'https://172.26.51.0',
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/namespace/create',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    return response.status_code


# convert string to base64_ascii encoded format to use in function create secrets
def plaintext_to_base64(string):
    encoded_bytes = base64.b64encode(string.encode("ascii"))
    coded_string_ascii = encoded_bytes.decode("ascii")
    return coded_string_ascii


# create secrets

def create_secrets(username, password, hostname):
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
    return response.status_code


"""

Functions to create a LAMP stack

"""

# create the persistent volume claim for the database of the lamp stack

def lamp_database_create_pvc(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/persistentvolumeclaims"

    payload = json.dumps({
        "type": "persistentvolumeclaim",
        "metadata": {
            "namespace": hostname,
            "labels": {
                "component": "database-"+hostname
            },
            "name": "database-"+hostname
        },
        "spec": {
            "accessModes": [
                "ReadWriteOnce"
            ],
            "storageClassName": "longhorn",
            "volumeName": "",
            "resources": {
                "requests": {
                    "storage": "2Gi"
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
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/persistentvolumeclaim/create',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.status_code


# create the service for the database of the lamp stack

def lamp_database_create_service(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/services"

    payload = json.dumps({
        "type": "service",
        "metadata": {
            "namespace": hostname,
            "labels": {
                "component": "database-"+hostname
            },
            "name": "database-"+hostname
        },
        "spec": {
            "ports": [
                {
                    "name": "database-"+hostname,
                    "port": 3306,
                    "protocol": "TCP",
                    "targetPort": 3306
                }
            ],
            "sessionAffinity": "None",
            "type": "ClusterIP",
            "selector": {
                "component": "database-"+hostname
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

    return response.status_code


# create the deployment for the database of the lamp stack

def lamp_database_create_deployment(hostname):
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

    return response.status_code


# create the persistent volume claim for phpmyadmin of the lamp stack

def lamp_phpmyadmin_create_pvc(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/persistentvolumeclaims"
    payload = json.dumps({
        "type": "persistentvolumeclaim",
        "metadata": {
            "namespace": hostname,
            "labels": {
                "component": "phpmyadmin-"+hostname
            },
            "name": "phpmyadmin-"+hostname
        },
        "spec": {
            "accessModes": [
                "ReadWriteOnce"
            ],
            "storageClassName": "longhorn",
            "volumeName": "",
            "resources": {
                "requests": {
                    "storage": "0.100Gi"
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
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/persistentvolumeclaim/create',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.status_code


# create the service for phpmyadmin of the lamp stack

def lamp_phpmyadmin_create_service(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/services"

    payload = json.dumps({
        "type": "service",
        "metadata": {
            "namespace": hostname,
            "labels": {
                "component": "phpmyadmin-"+hostname
            },
            "name": "phpmyadmin-"+hostname
        },
        "spec": {
            "ports": [
                {
                    "name": "http",
                    "port": 8080,
                    "protocol": "TCP",
                    "targetPort": 80
                },
                {
                    "name": "https",
                    "port": 8081,
                    "protocol": "TCP",
                    "targetPort": 443
                }
            ],
            "sessionAffinity": "None",
            "type": "ClusterIP",
            "selector": {
                "component": "phpmyadmin-"+hostname
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

    return response.status_code


# create the deployment for phpmyadmin of the lamp stack

def lamp_phpmyadmin_create_deployment(hostname):

    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

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

    return response.status_code


# create the ingress for phpmyadmin of the lamp stack

def lamp_phpmyadmin_create_ingress(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/networking.k8s.io.ingresses"

    payload = json.dumps({
        "type": "networking.k8s.io.ingress",
        "metadata": {
            "namespace": hostname,
            "annotations": {
                "kubernetes.io/ingress.class": "nginx",
                "cert-manager.io/cluster-issuer": "wp-prod-issuer"
            },
            "name": "phpmyadmin-"+hostname
        },
        "spec": {
            "rules": [
                {

                    "host": "phpmyadmin."+hostname+".motoyohosting.uk",
                    "http": {
                        "paths": [
                            {

                                "backend": {
                                    "service": {
                                        "port": {
                                            "number": 8080
                                        },
                                        "name": "phpmyadmin-"+hostname
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
                        "phpmyadmin."+hostname+".motoyohosting.uk"
                    ],
                    "secretName": "phpmyadmin-"+hostname+"-tls"
                }
            ]
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

    return response.status_code


# create the persistent volume for the webserver of the lamp stack

def lamp_webserver_create_pv(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/persistentvolumes"

    payload = json.dumps({
        "type": "persistentvolume",
        "metadata": {
            "name": "webserver-"+hostname
        },
        "spec": {
            "accessModes": [
                "ReadWriteMany"
            ],
            "capacity": {
                "storage": "2Gi"
            },
            "storageClassName": None,
            "hostPath": {
                "type": "",
                "path": "/mnt/"+hostname
            }
        },
        "accessModes": [
            "ReadWriteMany"
        ]
    })
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=b70cf6bccd7152f5c503aa94c4192f9a; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
        'Origin': 'https://172.26.51.0',
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/persistentvolume/create',
        'x-api-csrf': 'b70cf6bccd7152f5c503aa94c4192f9a'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.status_code


# create the persistent volume claim for the webserver of the lamp stack

def lamp_webserver_create_pvc(hostname):

    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/persistentvolumeclaims"

    payload = json.dumps({
        "type": "persistentvolumeclaim",
        "metadata": {
            "namespace": hostname,
            "name": "webserver-"+hostname
        },
        "spec": {
            "accessModes": [
                "ReadWriteMany"
            ],
            "storageClassName": "",
            "volumeName": "webserver-"+hostname,
            "resources": {
                "requests": {
                    "storage": "2Gi"
                }
            }
        },
        "accessModes": [
            "ReadWriteMany"
        ]
    })
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
        'Origin': 'https://172.26.51.0',
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/persistentvolumeclaim/create',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.status_code


# create the service for the webserver of the lamp stack

def lamp_webserver_create_service(hostname):

    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/services"

    payload = json.dumps({
        "type": "service",
        "metadata": {
            "namespace": hostname,
            "labels": {
                "component": "webserver-"+hostname
            },
            "name": "webserver-"+hostname
        },
        "spec": {
            "ports": [
                {
                    "name": "webserver-"+hostname,
                    "port": 80,
                    "protocol": "TCP",
                    "targetPort": 80
                }
            ],
            "sessionAffinity": "None",
            "type": "ClusterIP",
            "selector": {
                "component": "webserver-"+hostname
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

    return response.status_code


# create the deployment for the webserver of the lamp stack

def lamp_webserver_create_deployment(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

    payload = json.dumps({
        "type": "apps.deployment",
        "metadata": {
            "namespace": hostname,
            "annotations": {
                "deployment.kubernetes.io/revision": "1"
            },
            "labels": {
                "component": "webserver-"+hostname,
                "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-webserver-"+hostname
            },
            "name": "webserver-"+hostname
        },
        "spec": {
            "replicas": 1,
            "template": {
                "spec": {
                    "restartPolicy": "Always",
                    "containers": [
                        {
                            "imagePullPolicy": "Always",
                            "name": "php-apache",
                            "volumeMounts": [
                                {
                                    "name": "webserver-"+hostname,
                                    "mountPath": "/var/www"
                                }
                            ],
                            "image": "php:8.1.19-apache",
                            "ports": [
                                {
                                    "name": "webserver",
                                    "expose": True,
                                    "protocol": "TCP",
                                    "containerPort": 80,
                                    "hostPort": None,
                                    "hostIP": None,
                                    "_serviceType": "",
                                    "_ipam": "dhcp"
                                }
                            ],
                            "env": [
                                {
                                    "name": "APACHE_DOCUMENT_ROOT",
                                    "value": "/var/www/html"
                                },
                                {
                                    "name": "HOST_MACHINE_MYSQL_PORT",
                                    "value": "3306"
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
                        }
                    ],
                    "affinity": {}
                },
                "metadata": {
                    "labels": {
                        "component": "webserver-"+hostname,
                        "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-webserver-"+hostname
                    }
                }
            },
            "selector": {
                "matchLabels": {
                    "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-webserver-"+hostname
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

    return response.status_code


# create the ingress for the webserver of the lamp stack

def lamp_webserver_create_ingress(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/networking.k8s.io.ingresses"

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

    return response.status_code


# create the service for the sftp-server of the lamp stack, function return status_code and the nodePort that was created to reach the sftp instance
# because nog ingress can be used for ssh traffic.


def lamp_sftp_create_service(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/services"

    nodePort = random.randint(30001, 32767)

    payload = json.dumps({
        "type": "service",
        "metadata": {
            "namespace": hostname,
            "name": "sftp-"+hostname
        },
        "spec": {
            "ports": [
                {
                    "name": "sftp",
                    "port": 22,
                    "protocol": "TCP",
                    "targetPort": 22,
                    "nodePort": nodePort
                }
            ],
            "sessionAffinity": "None",
            "type": "NodePort",
            "selector": {
                "component": "sftp-"+hostname
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

    return [response.status_code, nodePort]


# create the configmap for the sftp-server of the lamp stack

def lamp_sftp_create_configmap(hostname, username, password):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/configmaps"

    payload = json.dumps({
        "type": "configmap",
        "metadata": {
            "namespace": hostname,
            "name": "sftp-user-config-"+hostname
        },
        "data": {
            "users.conf": username+":"+password+":1001:1001:/html"
        }
    })
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
        'Origin': 'https://172.26.51.0',
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/configmap/create',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.status_code


# create the deployment for the sftp-server of the lamp stack

def lamp_sftp_create_deployment(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

    payload = json.dumps({
        "type": "apps.deployment",
        "metadata": {
            "namespace": hostname,
            "annotations": {
                "deployment.kubernetes.io": "1"
            },
            "labels": {
                "component": "sftp-"+hostname,
                "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-sftp-"+hostname
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
                                    "mountPath": "/home/"+username    # was eerst de hostname
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

    return response.status_code


"""
Functions to create a wordpress instance

"""


# create the persistent volume claim for the database of the Wordpress instance

def wordpress_database_create_pvc(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/persistentvolumeclaims"

    payload = json.dumps({
        "type": "persistentvolumeclaim",
        "metadata": {
            "namespace": hostname,
            "name": "mysql-pv-claim-"+hostname
        },
        "spec": {
            "accessModes": [
                "ReadWriteOnce"
            ],
            "storageClassName": "longhorn",
            "volumeName": None,
            "resources": {
                "requests": {
                    "storage": "2Gi"
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
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/persistentvolumeclaim/create',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.status_code



# create the persistent volume claim for the webserver of the Wordpress instance

def wordpress_web_create_pvc(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/persistentvolumeclaims"

    payload = json.dumps({
        "type": "persistentvolumeclaim",
        "metadata": {
            "namespace": hostname,
            "name": "wordpress-pv-claim-"+hostname
        },
        "spec": {
            "accessModes": [
                "ReadWriteOnce"
            ],
            "storageClassName": "longhorn",
            "volumeName": None,
            "resources": {
                "requests": {
                    "storage": "2Gi"
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
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/persistentvolumeclaim/create',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.status_code


# create the service for the database of the Wordpress instance

def wordpress_db_create_service(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/services"

    payload = json.dumps({
        "type": "service",
        "metadata": {
            "namespace": hostname,
            "name": "mysql-wp-"+hostname
        },
        "spec": {
            "ports": [
                {
                    "port": 3306,
                    "protocol": "TCP",
                    "targetPort": 3306
                }
            ],
            "sessionAffinity": "None",
            "type": "ClusterIP",
            "selector": {
                "app": "wordpress",
                "tier": "mysql"
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

    return response.status_code


# create the deployment for the database of the Wordpress instance

def wordpress_db_create_deployment(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

    payload = json.dumps({
        "type": "apps.deployment",
        "metadata": {
            "namespace": hostname,
            "annotations": {
                "deployment.kubernetes.io/revision": "1"
            },
            "labels": {
                "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-mysql-wp-"+hostname
            },
            "name": "mysql-wp-"+hostname
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
                                    "name": "persistent-storage",
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
                                "claimName": "mysql-pv-claim-"+hostname
                            },
                            "name": "persistent-storage",
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
                        "app": "wordpress",
                        "tier": "mysql",
                        "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-mysql-wp-"+hostname
                    }
                }
            },
            "selector": {
                "matchLabels": {
                    "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-mysql-wp-"+hostname
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

    return response.status_code


# create the service for the webserver of the Wordpress instance

def wordpress_web_create_service(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/services"

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

    return response.status_code


# create the deployment for the webserver of the Wordpress instance

def wordpress_web_create_deployment(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/apps.deployments"

    payload = json.dumps({
        "type": "apps.deployment",
        "metadata": {
            "namespace": hostname,
            "annotations": {
                "deployment.kubernetes.io/revision": "1"
            },
            "labels": {
                "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-wordpress-"+hostname
            },
            "name": "wordpress-"+hostname
        },
        "spec": {
            "replicas": 1,
            "template": {
                "spec": {
                    "restartPolicy": "Always",
                    "containers": [
                        {
                            "imagePullPolicy": "Always",
                            "name": "wordpress",
                            "volumeMounts": [
                                {
                                    "name": "persistent-storage",
                                    "mountPath": "/var/www/html"
                                }
                            ],
                            "__active": True,
                            "image": "wordpress:php8.1-apache",
                            "ports": [
                                {
                                    "name": "wordpress",
                                    "expose": True,
                                    "protocol": "TCP",
                                    "containerPort": 80,
                                    "hostPort": None,
                                    "hostIP": None,
                                    "_serviceType": "",
                                    "_ipam": "dhcp"
                                }
                            ],
                            "env": [
                                {
                                    "name": "WORDPRESS_DB_HOST",
                                    "value": "mysql-wp-"+hostname+":3306"
                                },
                                {
                                    "name": "WORDPRESS_DB_PASSWORD",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "key": "password",
                                            "name": hostname,
                                            "optional": False
                                        }
                                    }
                                },
                                {
                                    "name": "WORDPRESS_DB_USER",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "key": "username",
                                            "name": hostname,
                                            "optional": False
                                        }
                                    }
                                },
                                {
                                    "name": "WORDPRESS_DB_NAME",
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
                                "claimName": "wordpress-pv-claim-"+hostname
                            },
                            "name": "persistent-storage",
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
                        "app": "wordpress",
                        "tier": "web",
                        "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-wordpress-"+hostname
                    }
                }
            },
            "selector": {
                "matchLabels": {
                    "workload.user.cattle.io/workloadselector": "apps.deployment-"+hostname+"-wordpress-"+hostname
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

    return response.status_code


# create the ingress for the webserver of the Wordpress instance

def wordpress_web_create_ingress(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/networking.k8s.io.ingresses"

    payload = json.dumps({
        "type": "networking.k8s.io.ingress",
        "metadata": {
            "namespace": hostname,
            "annotations": {
                "kubernetes.io/ingress.class": "nginx",
                "cert-manager.io/cluster-issuer": "wp-prod-issuer",
                "nginx.ingress.kubernetes.io/proxy-read-timeout": "360"
            },
            "name": "wordpress-"+hostname
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
                                        "name": "wordpress-"+hostname
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
                    "secretName": "wordpress-"+hostname+"-tls"
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

    return response.status_code


# delete namespace


def delete_namespace(hostname):
    url = "https://172.26.51.0/k8s/clusters/c-kmmv8/v1/namespaces/"+hostname

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-BE,en;q=0.9,nl-BE;q=0.8,nl;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': 'R_PCS=light; R_LOCALE=en-us; R_REDIRECTED=true; CSRF=2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw; R_SESS=token-j5pl8:2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw',
        'Origin': 'https://172.26.51.0',
        'Referer': 'https://172.26.51.0/dashboard/c/c-kmmv8/explorer/projectsnamespaces',
        'x-api-csrf': '2qm4zcdfgtwfhgpmlgsmbf9lrthkw9mr972vpmbv2wvgpsdrfdv6gw'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

    return response.status_code



"""
Program to create the deployments
"""

# variables obtained from the webinterface

username = input("Enter username: ")
password = input("Enter password: ")
hostname = input("Enter hostname: ")
type_deployment = input("Enter type of deployment (lamp or wordpress): ").lower()

creating_deployment = True

print("The installation of the deployment will take about 5 minutes, please don't refresh your page!!")

while creating_deployment:
    if type_deployment == "lamp":
        status_namespace = create_namespace(hostname)
        print("status_namespace", status_namespace)
        if status_namespace != 201:
            creating_deployment = False
        else:
            time.sleep(10)
            status_secrets = create_secrets(username, password, hostname)
            print("status_secrets", status_secrets)
            if status_secrets != 201:
                creating_deployment = False
            else:
                time.sleep(10)
                status_lamp_db_pvc = lamp_database_create_pvc(hostname)
                print("status_lamp_db_pvc", status_lamp_db_pvc)
                if status_lamp_db_pvc != 201:
                    creating_deployment = False
                else:
                    time.sleep(10)
                    status_lamp_db_service = lamp_database_create_service(hostname)
                    print("status_lamp_db_service", status_lamp_db_service)
                    if status_lamp_db_service != 201:
                        creating_deployment = False
                    else:
                        time.sleep(10)
                        status_lamp_db_deployment = lamp_database_create_deployment(hostname)
                        print("status_lamp_db_deployment", status_lamp_db_deployment)
                        if status_lamp_db_deployment != 201:
                            creating_deployment = False
                        else:
                            time.sleep(60)
                            status_lamp_php_pvc = lamp_phpmyadmin_create_pvc(hostname)
                            print("status_lamp_php_pvc", status_lamp_php_pvc)
                            if status_lamp_php_pvc != 201:
                                creating_deployment = False
                            else:
                                time.sleep(10)
                                status_lamp_php_service = lamp_phpmyadmin_create_service(hostname)
                                print("status_lamp_php_service", status_lamp_php_service)
                                if status_lamp_php_service != 201:
                                    creating_deployment = False
                                else:
                                    time.sleep(10)
                                    status_lamp_php_deployment = lamp_phpmyadmin_create_deployment(hostname)
                                    print("status_lamp_php_deployment", status_lamp_php_deployment)
                                    if status_lamp_php_deployment != 201:
                                        creating_deployment = False
                                    else:
                                        time.sleep(60)
                                        status_lamp_php_ingress = lamp_phpmyadmin_create_ingress(hostname)
                                        print("status_lamp_php_ingress", status_lamp_php_ingress)
                                        if status_lamp_php_ingress != 201:
                                            creating_deployment = False
                                        else:
                                            time.sleep(10)
                                            status_lamp_webserver_pv = lamp_webserver_create_pv(hostname)
                                            print("status_lamp_webserver_pv", status_lamp_webserver_pv)
                                            if status_lamp_webserver_pv != 201:
                                                creating_deployment = False
                                            else:
                                                time.sleep(10)
                                                status_lamp_webserver_pvc = lamp_webserver_create_pvc(hostname)
                                                print("status_lamp_webserver_pvc", status_lamp_webserver_pvc)
                                                if status_lamp_webserver_pvc != 201:
                                                    creating_deployment = False
                                                else:
                                                    time.sleep(10)
                                                    status_lamp_webserver_service = lamp_webserver_create_service(hostname)
                                                    print("status_lamp_webserver_service", status_lamp_webserver_service)
                                                    if status_lamp_webserver_service != 201:
                                                        creating_deployment = False
                                                    else:
                                                        time.sleep(10)
                                                        status_lamp_webserver_deployment = lamp_webserver_create_deployment(hostname)
                                                        print("status_lamp_webserver_deployment", status_lamp_webserver_deployment)
                                                        if status_lamp_webserver_deployment != 201:
                                                            creating_deployment = False
                                                        else:
                                                            time.sleep(60)
                                                            status_lamp_webserver_ingress = lamp_webserver_create_ingress(hostname)
                                                            print("status_lamp_webserver_ingress", status_lamp_webserver_ingress)
                                                            if status_lamp_webserver_ingress != 201:
                                                                creating_deployment = False
                                                            else:
                                                                time.sleep(60)
                                                                status_lamp_sftp_service = lamp_sftp_create_service(hostname)
                                                                print("status_lamp_sftp_service", status_lamp_sftp_service)
                                                                if status_lamp_sftp_service[0] != 201:
                                                                    creating_deployment = False
                                                                else:
                                                                    time.sleep(10)
                                                                    status_lamp_sftp_configmap = lamp_sftp_create_configmap(hostname, username, password)
                                                                    print("status_lamp_sftp_configmap", status_lamp_sftp_configmap)
                                                                    if status_lamp_sftp_configmap != 201:
                                                                        creating_deployment = False
                                                                    else:
                                                                        time.sleep(10)
                                                                        status_lamp_sftp_deployment = lamp_sftp_create_deployment(hostname)
                                                                        print("status_lamp_sftp_deployment", status_lamp_sftp_deployment)
                                                                        if status_lamp_sftp_configmap != 201:
                                                                            creating_deployment = False
                                                                        else:
                                                                            time.sleep(60)
                                                                            print("thank you for your patience!! \nYour new deployment is available @ \n"
                                                                                     "webpage --> https://www."+hostname+".motoyohosting.uk \n"
                                                                                        "sftp --> sftp://sftp."+hostname+".motoyohosting.uk  port: "+str(status_lamp_sftp_service[1]))
                                                                            exit(0)
    elif type_deployment == "wordpress":
        status_namespace = create_namespace(hostname)
        print("status_namespace", status_namespace)
        if status_namespace != 201:
            creating_deployment = False
        else:
            time.sleep(10)
            status_secrets = create_secrets(username, password, hostname)
            print("status_secrets", status_secrets)
            if status_secrets != 201:
                creating_deployment = False
            else:
                time.sleep(10)
                status_wordpress_db_pvc = wordpress_database_create_pvc(hostname)
                print("status_wordpress_db_pvc", status_wordpress_db_pvc)
                if status_wordpress_db_pvc != 201:
                    creating_deployment = False
                else:
                    time.sleep(10)
                    status_wordpress_db_service = wordpress_db_create_service(hostname)
                    print("status_wordpress_db_service", status_wordpress_db_service)
                    if status_wordpress_db_service != 201:
                        creating_deployment = False
                    else:
                        time.sleep(10)
                        status_wordpress_db_deployment = wordpress_db_create_deployment(hostname)
                        print("status_wordpress_db_deployment", status_wordpress_db_deployment)
                        if status_wordpress_db_deployment != 201:
                            creating_deployment = False
                        else:
                            time.sleep(60)
                            status_wordpress_web_pvc = wordpress_web_create_pvc(hostname)
                            print("status_wordpress_web_pvc", status_wordpress_web_pvc)
                            if status_wordpress_web_pvc != 201:
                                creating_deployment = False
                            else:
                                time.sleep(10)
                                status_wordpress_web_service = wordpress_web_create_service(hostname)
                                print("status_wordpress_web_service", status_wordpress_web_service)
                                if status_wordpress_web_service != 201:
                                    creating_deployment = False
                                else:
                                    time.sleep(10)
                                    status_wordpress_web_deployment = wordpress_web_create_deployment(hostname)
                                    print("status_wordpress_web_deployment", status_wordpress_web_deployment)
                                    if status_wordpress_web_deployment != 201:
                                        creating_deployment = False
                                    else:
                                        time.sleep(60)
                                        status_wordpress_web_ingress = wordpress_web_create_ingress(hostname)
                                        print("status_wordpress_web_ingress", status_wordpress_web_ingress)
                                        if status_wordpress_web_ingress != 201:
                                            creating_deployment = False
                                        else:
                                            time.sleep(60)
                                            print("thank you for your patience!! \nYour new deployment is available in 5 minutes @ \n"
                                                  "webpage --> https://www."+hostname+".motoyohosting.uk")
                                            exit(0)


time.sleep(60)
status_delete_namespace = delete_namespace(hostname)
time.sleep(60)
print("something went wrong, the hostname has been released. Please try again in 5 minutes")
#iets om de hostname uit de database te verwijderen
exit(0)

