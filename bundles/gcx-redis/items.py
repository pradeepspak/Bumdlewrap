k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/redis": {
        "manifest_file": "redis-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "replicas": node.metadata.get("redis", {}).get("replicas", "1"),
        },
    }
}

if node.has_bundle("gcp-regional-disk"):
    storage_class = "gcp-regional-disk"
else:
    storage_class = "standard"

k8s_pvc = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/redis": {
        "manifest_file": "redis-pvc.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "storage_size": node.metadata.get("redis", {}).get("storage_size", "1Gi"),
            "storage_class_name": storage_class,
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/redis": {"manifest_file": "redis-service.yaml", "manifest_processor": "jinja2"}
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/redis": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "redis"}},
                "policyTypes": ["Ingress"],
                "ingress": [{"ports": [{"port": 6379, "protocol": "TCP"}]}],
            },
        }
    }
}
