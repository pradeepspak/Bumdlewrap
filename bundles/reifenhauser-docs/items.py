import glob
from pathlib import Path

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/docs": {"manifest_file": "docs_service.yaml"}
}

k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/docs": {
        "manifest_file": "docs_deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "registry_host": node.metadata.get("global", {}).get(
                "registry_host", "eu.gcr.io"
            ),
            "gatekeeper_image": node.metadata.get("docs", {}).get(
                "gatekeeper_image", "gcx-keycloak-gatekeeper"
            ),
            "gatekeeper_version": node.metadata.get("docs", {}).get(
                "gatekeeper_version", "2.3.0"
            ),
            "registry_image": node.metadata.get("docs", {}).get(
                "registry_image", "reifenhauser-docs"
            ),
            "registry_version": node.metadata.get("docs", {}).get(
                "registry_version", "latest"
            ),
        },
    }
}

k8s_configmaps = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/gatekeeper-config-docs": {
        "manifest_file": "gatekeeper_config.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "discovery_url": "https://auth."
            + node.metadata.get("global").get("domain_suffix")
            + "/auth/realms/"
            + node.metadata.get("docs").get("realm"),
            "client_id": node.metadata.get("docs").get("client_id", "docs"),
            "client_secret": repo.vault.decrypt(
                node.metadata.get("docs").get("client_secret"),
                key=node.metadata.get("global", {}).get("bw_key"),
            ),
            "redirection_url": "https://docs."
            + node.metadata.get("global").get("domain_suffix"),
        },
    }
}

k8s_ingresses = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/docs": {
        "manifest_file": "ingress.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "hostname": "docs." + node.metadata.get("global").get("domain_suffix")
        },
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/docs-ingress": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "docs"}},
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
                            {"port": 443, "protocol": "TCP"},
                            {"port": 53, "protocol": "UDP"},
                        ]
                    }
                ],
            },
        }
    }
}
