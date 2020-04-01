k8s_daemonsets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nginx-mqtt": {
        "manifest_file": "nginx-mqtt-daemonset.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env"),
            "app": node.metadata.get("mqtt-ingress", {}).get("app", "nginx-mqtt"),
        },
    }
}

k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nginx-mqtt": {"delete": True}
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nginx-mqtt": {
        "manifest_file": "nginx-mqtt-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "app": node.metadata.get("mqtt-ingress", {}).get("app", "nginx-mqtt"),
            "loadbalancer_ip": node.metadata.get("mqtt-ingress", {}).get(
                "loadbalancer_ip", {}
            ),
        },
    }
}

k8s_configmaps = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nginx-conf": {
        "manifest_file": "nginx-conf.yaml",
        "manifest_processor": "jinja2",
    },
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nginx-stream-conf-d": {
        "manifest_file": "nginx-stream-conf.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "mqtt_server": node.metadata.get("mqtt-ingress", {}).get(
                "mqtt_server", "vernemq"
            ),
            "mqtt_port": node.metadata.get("mqtt-ingress", {}).get("mqtt_port", "1883"),
        },
    },
}

k8s_secrets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/rfh-nginx-certs": {
        "manifest_file": "nginx-ssl-certs.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "ca_chain": str(
                repo.vault.decrypt(
                    node.metadata.get("mqtt-ingress").get("ca_chain"),
                    key=node.metadata.get("global").get("bw_key"),
                )
            ),
            "cert": str(
                repo.vault.decrypt(
                    node.metadata.get("mqtt-ingress").get("cert"),
                    key=node.metadata.get("global").get("bw_key"),
                )
            ),
            "key": str(
                repo.vault.decrypt(
                    node.metadata.get("mqtt-ingress").get("key"),
                    key=node.metadata.get("global").get("bw_key"),
                )
            ),
        },
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/mqtt-ingress": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "nginx-mqtt"}},
                "policyTypes": ["Ingress", "Egress"],
                "ingress": [
                    {
                        "ports": [
                            {"port": 8883, "protocol": "TCP"},
                            {"port": 443, "protocol": "TCP"},
                        ]
                    }
                ],
                "egress": [
                    {
                        "ports": [{"port": 1883, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "vernemq"}}}],
                    },
                    {"ports": [{"port": 53, "protocol": "UDP"}]},
                ],
            },
        }
    }
}
