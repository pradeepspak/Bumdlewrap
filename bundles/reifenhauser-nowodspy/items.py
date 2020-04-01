k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nowodspy": {
        "manifest_file": "nowodspy-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "prod"),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("nowodspy", {}).get("name", "nowodspy"),
            "replicas": node.metadata.get("nowodspy", {}).get("replicas", "2"),
            "registry_image": node.metadata.get("nowodspy", {}).get(
                "registry_image", "nowodspy"
            ),
            "registry_version": node.metadata.get("nowodspy", {}).get(
                "registry_version", "master"
            ),
            "registry_host": node.metadata.get("global", {}).get("registry_host"),
            "sentry_dsn": node.metadata.get("nowodspy", {}).get(
                "sentry_dsn", "http://localhost/0"
            ),
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nowodspy": {
        "manifest_file": "nowodspy-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "service_port": node.metadata.get("nowodspy", {}).get("service_port", "80"),
            "name": node.metadata.get("nowodspy", {}).get("name", "nowodspy"),
        },
    }
}
