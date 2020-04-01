k8s_statefulsets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {
        "manifest_file": "rfh-keycloak-statefulset.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "registry_host": node.metadata.get("global", {}).get("registry_host"),
            "registry_image": node.metadata.get("keycloak", {}).get(
                "registry_image", "keycloak"
            ),
            "registry_version": node.metadata.get("keycloak", {}).get(
                "registry_version", "master"
            ),
            "name": node.metadata.get("keycloak", {}).get("name", "keycloak"),
            "replicas": node.metadata.get("keycloak", {}).get("replicas", "1"),
            "cluster_hoster": node.metadata.get("cluster", {}).get("hoster"),
            "keycloak_user": node.metadata.get("keycloak", {}).get(
                "keycloak_user", "keycloak"
            ),
            "keycloak_pass": node.metadata.get("keycloak", {}).get(
                "keycloak_pass", "keycloak_password"
            ),
            "postgres_host": node.metadata.get("global", {}).get(
                "postgres_host", "postgres"
            ),
            "postgres_user": node.metadata.get("keycloak", {}).get(
                "postgres_user", "keycloak"
            ),
            "postgres_pass": node.metadata.get("keycloak", {}).get(
                "postgres_pass", "keycloak"
            ),
            "postgres_db": node.metadata.get("keycloak", {}).get(
                "postgres_db", "keycloak"
            ),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container"
            ),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
            "keycloak_hostname": node.metadata.get("keycloak").get(
                "external_host",
                "auth." + node.metadata.get("global").get("domain_suffix"),
            ),
            "namespace": node.metadata.get("global", {}).get("namespace", "default"),
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {
        "manifest_file": "rfh-keycloak-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "internal_port": "8080",
            "service_port": "80",
            "name": "keycloak",
            "headless_or_not": "",
        },
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak-headless": {
        "manifest_file": "rfh-keycloak-headless-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "internal_port": "8080",
            "service_port": "80",
            "name": "keycloak",
            "headless_or_not": "clusterIP: None",
        },
    },
}

k8s_ingresses = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {
        "manifest_file": "rfh-keycloak-ingress.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "external_host": node.metadata.get("keycloak").get(
                "external_host",
                "auth." + node.metadata.get("global").get("domain_suffix"),
            ),
            "service_port": "80",
            "le_certificates": node.metadata.get("cluster", {}).get("letsencrypt"),
            "secrets_name": node.metadata.get("keycloak", {}).get("secrets_name"),
        },
    }
}

k8s_roles = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {
        "manifest": {
            "rules": [{"apiGroups": [""], "resources": ["pods"], "verbs": ["list"]}]
        }
    }
}

k8s_configmaps = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {"manifest_file": "rfh-keycloak-config-configmap.yaml"}
}
k8s_rolebindings = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {
        "manifest": {
            "roleRef": {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "Role",
                "name": "keycloak",
            },
            "subjects": [{"kind": "ServiceAccount", "name": "keycloak"}],
        }
    }
}


k8s_serviceaccounts = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {"manifest": {}}
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/keycloak": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "keycloak"}},
                "policyTypes": ["Ingress", "Egress"],
                "ingress": [
                    {"ports": [{"port": 8080, "protocol": "TCP"}]},
                    {
                        "ports": [{"port": 7600, "protocol": "TCP"}],
                        "from": [{"podSelector": {"matchLabels": {"app": "keycloak"}}}],
                    },
                ],
                "egress": [
                    {
                        "ports": [
                            {"port": 7600, "protocol": "TCP"},
                            {"port": 8080, "protocol": "TCP"},
                        ],
                        "to": [{"podSelector": {"matchLabels": {"app": "keycloak"}}}],
                    },
                    {"ports": [{"port": 53, "protocol": "UDP"}]},
                ],
            },
        }
    }
}
