k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/reflow": {
        "manifest_file": "reflow-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "prod"),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("reflow", {}).get("name", "reflow"),
            "replicas": node.metadata.get("reflow", {}).get("replicas", "2"),
            "registry_image": node.metadata.get("reflow", {}).get(
                "registry_image", "reflow"
            ),
            "registry_version": node.metadata.get("reflow", {}).get(
                "registry_version", "master"
            ),
            "registry_host": node.metadata.get("global", {}).get("registry_host"),
            "sentry_dsn": node.metadata.get("reflow", {}).get(
                "sentry_dsn", "http://localhost/0"
            ),
            "replace_os_vars": node.metadata.get("reflow", {}).get(
                "replace_os_vars", "true"
            ),
            "mqtt_host": node.metadata.get("reflow", {}).get("mqtt_host", "vernemq"),
            "mqtt_user": node.metadata.get("reflow", {}).get("mqtt_user"),
            "mqtt_pass": node.metadata.get("reflow", {}).get("mqtt_pass"),
            "mqtt_port": node.metadata.get("reflow", {}).get("mqtt_port", "1883"),
            "port": node.metadata.get("reflow", {}).get("port", "4000"),
            "riot_internal_api_host": node.metadata.get("reflow", {}).get(
                "riot_internal_api_host",
                "http://"
                + node.metadata.get("reflow").get("riot_internal_api_host", "riot")
                + ":"
                + node.metadata.get("riot", {}).get("riot_internal_api_port", "8080"),
            ),
            "gcp_project": node.metadata.get("reflow").get(
                "gcp_project", "reifenhauser-stage"
            ),
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/reflow": {
        "manifest_file": "reflow-service.yaml",
        "manifest_processor": "jinja2",
        "context": {"env": node.metadata.get("global", {}).get("env", "prod")},
    }
}

k8s_secrets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/reflow-gcp-credentials": {
        "manifest": {
            "data": {
                "reflow-credentials.json": str(
                    repo.vault.decrypt(
                        node.metadata.get("reflow").get(
                            "gcp_credentials", "this-causes-a-fail-if-you-forget"
                        ),
                        key=node.metadata.get("global", {}).get("bw_key"),
                    )
                )
            }
        }
    }
}

k8s_raw = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/ServiceMonitor/reflow": {
        "manifest_file": "reflow-servicemonitor.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "namespace": node.metadata.get("global", {}).get("namespace", "default")
        },
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/reflow": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "reflow"}},
                "policyTypes": ["Ingress", "Egress"],
                "ingress": [
                    {
                        "ports": [{"port": 9568, "protocol": "TCP"}],
                        "from": [
                            {
                                "namespaceSelector": {
                                    "matchLabels": {"purpose": "monitoring"}
                                }
                            }
                        ],
                    }
                ],
                "egress": [
                    {
                        "ports": [{"port": 1883, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "vernemq"}}}],
                    },
                    {
                        "ports": [{"port": 8080, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "riot"}}}],
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
