k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/influxdb": {
        "manifest_file": "reifenhauser-influxdb-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("influxdb", {}).get("name", "influxdb"),
            "replicas": node.metadata.get("influxdb", {}).get("replicas", "1"),
            "registry_image": node.metadata.get("influxdb", {}).get(
                "registry_image", "influxdb"
            ),
            "registry_version": node.metadata.get("influxdb", {}).get(
                "registry_version", "1.7.6"
            ),
            "influx_db": node.metadata.get("influxdb", {}).get("influx_db"),
            "influx_user": node.metadata.get("influxdb", {}).get(
                "influx_user", "standard_user"
            ),
            "influx_password": node.metadata.get("influxdb", {}).get("influx_password"),
            "influx_admin_user": node.metadata.get("influxdb", {}).get(
                "influx_admin_user", "admin"
            ),
            "influx_admin_password": node.metadata.get("influxdb", {}).get(
                "influx_admin_password"
            ),
        },
    }
}

k8s_configmaps = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/influxdb": {
        "manifest_file": "reifenhauser-influxdb-config-configmap.yaml",
        "manifest_processor": "jinja2",
        #'context': {
        # },
    }
}

if node.has_bundle("gcp-regional-disk"):
    storage_class = "gcp-regional-disk"
else:
    storage_class = "standard"

k8s_pvc = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/influxdb": {
        "manifest_file": "reifenhauser-influxdb-pvc.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "storage_size": node.metadata.get("influxdb", {}).get(
                "storage_size", "32Gi"
            ),
            "storage_class_name": storage_class,
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/influxdb": {
        "manifest_file": "reifenhauser-influxdb-service.yaml",
        "manifest_processor": "jinja2",
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/influxdb": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "influxdb"}},
                "policyTypes": ["Ingress"],
                "ingress": [
                    {
                        "ports": [{"port": 8086, "protocol": "TCP"}],
                        "from": [
                            {
                                "namespaceSelector": {},
                                "podSelector": {"matchLabels": {"tsdbconn": "true"}},
                            }
                        ],
                    },
                    {
                        "ports": [{"port": 8088, "protocol": "TCP"}],
                        "from": [
                            {"podSelector": {"matchLabels": {"app": "influx-backup"}}}
                        ],
                    },
                ],
            },
        }
    }
}
