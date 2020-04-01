import glob
from pathlib import Path

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/tsdbviewer": {
        "manifest_file": "grafana_service.yaml",
        "manifest_processor": "mako",
    }
}

k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/tsdbviewer": {
        "manifest_file": "grafana_deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "registry_host": node.metadata.get("global", {}).get(
                "registry_host", "eu.gcr.io"
            ),
            "gatekeeper_image": node.metadata.get("tsdbviewer", {}).get(
                "gatekeeper_image", "gcx-keycloak-gatekeeper"
            ),
            "gatekeeper_version": node.metadata.get("tsdbviewer", {}).get(
                "gatekeeper_version", "2.3.0"
            ),
            "admin_password": repo.vault.password_for("tsdbviewer"),
        },
    }
}

k8s_configmaps = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/gatekeeper-config": {
        "manifest_file": "gatekeeper_config.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "discovery_url": "https://auth."
            + node.metadata.get("global").get("domain_suffix")
            + "/auth/realms/"
            + node.metadata.get("tsdbviewer").get("realm"),
            "client_id": node.metadata.get("tsdbviewer").get("client_id", "tsdbviewer"),
            "client_secret": repo.vault.decrypt(
                node.metadata.get("tsdbviewer").get("client_secret"),
                key=node.metadata.get("global", {}).get("bw_key"),
            ),
            "redirection_url": "https://tsdbviewer."
            + node.metadata.get("global").get("domain_suffix"),
        },
    }
}

k8s_ingresses = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/tsdbviewer": {
        "manifest_file": "ingress.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "hostname": "tsdbviewer."
            + node.metadata.get("global").get("domain_suffix"),
            "le_certificates": node.metadata.get("cluster", {}).get("letsencrypt"),
            "secrets_name": node.metadata.get("tsdbviewer", {}).get("secrets_name"),
        },
    }
}

if node.has_bundle("gcp-regional-disk"):
    storage_class = "gcp-regional-disk"
else:
    storage_class = "standard"

k8s_pvc = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/tsdbviewer": {
        "manifest_file": "grafana_pvc.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "storage_size": node.metadata.get("tsdbviewer", {}).get(
                "storage_size", "1Gi"
            ),
            "storage_class_name": storage_class,
        },
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/tsdbviewer": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "tsdbviewer"}},
                "policyTypes": ["Ingress", "Egress"],
                "ingress": [
                    {
                        "ports": [{"port": 80, "protocol": "TCP"}],
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
                "egress": [
                    {
                        "ports": [
                            {"port": 53, "protocol": "UDP"},
                            {"port": 443, "protocol": "TCP"},
                        ]
                    }
                ],
            },
        }
    }
}
