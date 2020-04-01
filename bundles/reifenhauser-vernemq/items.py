k8s_statefulsets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq": {
        "manifest_file": "reifenhauser-vernemq-statefulset.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env"),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("vernemq").get("name", "vernemq"),
            "replicas": node.metadata.get("vernemq").get("replicas", "1"),
            "registry_image": node.metadata.get("vernemq").get(
                "registry_image", "vernemq"
            ),
            "registry_version": node.metadata.get("vernemq").get(
                "registry_version", "master"
            ),
            "registry_host": node.metadata.get("global").get("registry_host"),
        },
    }
}

k8s_configmaps = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq-conf-local": {
        "manifest_file": "reifenhauser-vernemq-conf-local-configmap.yaml",
        "manifest_processor": "jinja2",
        "context": {"env": node.metadata.get("global", {}).get("env")},
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq-vmqacl": {
        "manifest_file": "reifenhauser-vernemq-vmqacl-configmap.yaml",
        "manifest_processor": "jinja2",
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq-advanced": {
        "manifest_file": "reifenhauser-vernemq-advanced-configmap.yaml",
        "manifest_processor": "jinja2",
    },
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq-headless": {
        "manifest_file": "reifenhauser-vernemq-service-headless.yaml"
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq": {
        "manifest_file": "reifenhauser-vernemq-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "name": node.metadata.get("vernemq").get("name", "vernemq"),
            "env": node.metadata.get("global", {}).get("env"),
        },
    },
}

k8s_raw = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/ServiceMonitor/vernemq": {
        "manifest_file": "reifenhauser-vernemq-servicemonitor.yaml"
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/PrometheusRule/vernemq": {
        "manifest_file": "reifenhauser-vernemq-alertmanager.yaml"
    },
}

k8s_serviceaccounts = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq": {"manifest": {}}
}

k8s_rolebindings = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/can-read-only-ops-on-pods": {
        "manifest": {
            "roleRef": {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "Role",
                "name": "list-get-watch-pods",
            },
            "subjects": [
                {"kind": "ServiceAccount", "name": "default"},
                {"kind": "ServiceAccount", "name": "vernemq"},
            ],
        }
    }
}

k8s_roles = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/list-get-watch-pods": {
        "manifest": {
            "rules": [
                {
                    "apiGroups": [""],
                    "resources": ["pods"],
                    "verbs": ["get", "list", "watch"],
                }
            ]
        }
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/vernemq": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "vernemq"}},
                "policyTypes": ["Ingress", "Egress"],
                "ingress": [
                    {
                        "ports": [
                            {"port": 1883, "protocol": "TCP"},
                            {"port": 4369, "protocol": "TCP"},
                            {"port": 8080, "protocol": "TCP"},
                            {"port": 8888, "protocol": "TCP"},
                            {"port": 9100, "protocol": "TCP"},
                            {"port": 9101, "protocol": "TCP"},
                            {"port": 9102, "protocol": "TCP"},
                            {"port": 9103, "protocol": "TCP"},
                            {"port": 9104, "protocol": "TCP"},
                            {"port": 9105, "protocol": "TCP"},
                            {"port": 9106, "protocol": "TCP"},
                            {"port": 9107, "protocol": "TCP"},
                            {"port": 9108, "protocol": "TCP"},
                            {"port": 9109, "protocol": "TCP"},
                            {"port": 9999, "protocol": "TCP"},
                            {"port": 44053, "protocol": "TCP"},
                        ],
                        "from": [{"podSelector": {"matchLabels": {"app": "vernemq"}}}],
                    },
                    {
                        "ports": [{"port": 1883, "protocol": "TCP"}],
                        "from": [{"namespaceSelector": {}}],
                    },
                    {
                        "ports": [{"port": 9999, "protocol": "TCP"}],
                        "from": [
                            {
                                "namespaceSelector": {
                                    "matchLabels": {"purpose": "monitoring"}
                                }
                            }
                        ],
                    },
                ],
                "egress": [
                    {
                        "ports": [
                            {"port": 1883, "protocol": "TCP"},
                            {"port": 4369, "protocol": "TCP"},
                            {"port": 8080, "protocol": "TCP"},
                            {"port": 8888, "protocol": "TCP"},
                            {"port": 9100, "protocol": "TCP"},
                            {"port": 9101, "protocol": "TCP"},
                            {"port": 9102, "protocol": "TCP"},
                            {"port": 9103, "protocol": "TCP"},
                            {"port": 9104, "protocol": "TCP"},
                            {"port": 9105, "protocol": "TCP"},
                            {"port": 9106, "protocol": "TCP"},
                            {"port": 9107, "protocol": "TCP"},
                            {"port": 9108, "protocol": "TCP"},
                            {"port": 9109, "protocol": "TCP"},
                            {"port": 9999, "protocol": "TCP"},
                            {"port": 44053, "protocol": "TCP"},
                        ],
                        "to": [{"podSelector": {"matchLabels": {"app": "vernemq"}}}],
                    },
                    {
                        "ports": [
                            {"port": 53, "protocol": "UDP"},
                            {"port": 443, "protocol": "TCP"},
                        ]
                    },
                ],
            },
        }
    }
}
