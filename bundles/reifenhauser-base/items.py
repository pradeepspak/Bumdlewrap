import base64

# Ensure the namespace exists
k8s_namespaces = {node.metadata.get("global", {}).get("namespace", "default"): {}}

k8s_networkpolicies = {
    # A blank ingress/egress will ensure all traffic in the namespace is blocked, unless
    # it is explicitly allowed via another rule
    node.metadata.get("global", {}).get("namespace", "default")
    + "/default-deny-all": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]},
        }
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/allow-sentry": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"sentry": "dus"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "ports": [
                            {"port": 443, "protocol": "TCP"},
                            {"port": 53, "protocol": "UDP"},
                        ],
                        "to": [{"ipBlock": {"cidr": "185.79.127.14/32"}}],
                    }
                ],
            },
        }
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/allow-certmanager-solver": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {
                    "matchLabels": {"certmanager.k8s.io/acme-http01-solver": "true"}
                },
                "policyTypes": ["Ingress"],
                "ingress": [
                    {
                        "ports": [{"port": 8089, "protocol": "TCP"}],
                        "from": [
                            {
                                "namespaceSelector": {},
                                "podSelector": {
                                    "matchLabels": {"app": "ingress-nginx"}
                                },
                            }
                        ],
                    }
                ],
            },
        }
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/allow-mailjet": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"mail": "mailjet"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "ports": [
                            {"port": 25, "protocol": "TCP"},
                            {"port": 465, "protocol": "TCP"},
                            {"port": 587, "protocol": "TCP"},
                            {"port": 443, "protocol": "TCP"},
                            {"port": 53, "protocol": "UDP"},
                        ],
                        "to": [
                            {"ipBlock": {"cidr": "104.199.96.85/32"}},
                            {"ipBlock": {"cidr": "35.187.79.8/32"}},
                        ],
                    }
                ],
            },
        }
    },
}


def buildSecretsList():
    allSecrets = {}
    for item, password in node.metadata.get("passwords", {}).items():
        allSecrets[item] = base64.b64encode(
            str(
                repo.vault.decrypt(
                    password, key=node.metadata.get("global", {}).get("bw_key")
                )
            ).encode()
        ).decode("utf-8")
    return allSecrets


if node.name == "reifenhaeuser-prod":
    k8s_secrets = {
        node.metadata.get("global", {}).get("namespace", "default")
        + "/"
        + node.metadata.get("global", {}).get("bw_password_container"): {
            "manifest": {"data": buildSecretsList()}
        },
        "rfh-prod/pure-iot-wildcard-certs": {
            "manifest": {
                "data": {
                    "tls.crt": str(
                        repo.vault.decrypt(
                            node.metadata.get("base", {}).get("tls_crt"),
                            key=node.metadata.get("global", {}).get("bw_key"),
                        )
                    ),
                    "tls.key": str(
                        repo.vault.decrypt(
                            node.metadata.get("base", {}).get("tls_key"),
                            key=node.metadata.get("global", {}).get("bw_key"),
                        )
                    ),
                },
                "metadata": {"name": "pure-iot-wildcard-certs"},
                "type": "kubernetes.io/tls",
            }
        },
    }
else:
    k8s_secrets = {
        node.metadata.get("global", {}).get("namespace", "default")
        + "/"
        + node.metadata.get("global", {}).get("bw_password_container"): {
            "manifest": {"data": buildSecretsList()}
        }
    }


if node.metadata.get("global", {}).get("registry_secret"):
    k8s_secrets.update(
        {
            node.metadata.get("global", {}).get("namespace", "default")
            + "/"
            + node.metadata.get("global", {}).get("registry_secret"): {
                "manifest": {
                    "type": "kubernetes.io/dockerconfigjson",
                    "data": {
                        ".dockerconfigjson": str(
                            repo.vault.decrypt(
                                node.metadata.get("passwords", {}).get("regcred"),
                                node.metadata.get("global", {}).get("bw_key"),
                            )
                        )
                    },
                }
            }
        }
    )


k8s_serviceaccounts = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/reifenhauser-standard": {}
}

domain_suffix = node.metadata.get("global").get("domain_suffix")
keycloak_user = node.metadata.get("keycloak").get("keycloak_user", "keycloak")
keycloak_pass_secret = node.metadata.get("global").get("bw_password_container")
keycloak_pass_key = node.metadata.get("keycloak").get("keycloak_pass")

print("\n")
print("***********************************************")
print("***********************************************")
print("**      Reifenhauser Base Configuration      **")
print("***********************************************")
print("***********************************************")
print("** Configured with following parameters:       ")
print("  * Base URL: " + domain_suffix)
print("  * Visit: http://riot." + domain_suffix + "/")
print("  * Keycloak: http://auth." + domain_suffix + "/")
print("    user: " + keycloak_user)
print("    password: Run the following command:")
print(
    "        kubectl get secret "
    + keycloak_pass_secret
    + " -o jsonpath='{.data."
    + keycloak_pass_key
    + "}' | base64 --decode; echo "
)
print("***********************************************")
