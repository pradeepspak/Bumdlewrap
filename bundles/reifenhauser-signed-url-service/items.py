k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/signed-url-service": {
        "manifest_file": "signed-url-service-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "prod"),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("signed_url_service", {}).get(
                "name", "signed-url-service"
            ),
            "replicas": node.metadata.get("signed_url_service", {}).get(
                "replicas", "2"
            ),
            "registry_image": node.metadata.get("signed_url_service", {}).get(
                "registry_image", "signed_url_service"
            ),
            "registry_version": node.metadata.get("signed_url_service", {}).get(
                "registry_version", "master"
            ),
            "registry_host": node.metadata.get("global", {}).get("registry_host"),
            "signed_url_service_host": node.metadata.get("signed_url_service", {}).get(
                "signed_url_service_host",
                "signed-url-service."
                + node.metadata.get("global").get("domain_suffix"),
            ),
            "signed_url_service_internal_port": node.metadata.get(
                "signed_url_service", {}
            ).get("signed_url_service_internal_port", "4000"),
            "signed_url_service_secret_key": node.metadata.get(
                "signed_url_service", {}
            ).get("signed_url_service_secret_key"),
            "replace_os_vars": node.metadata.get("signed_url_service", {}).get(
                "replace_os_vars", "true"
            ),
            "url_expire_time": node.metadata.get("signed_url_service", {}).get(
                "url_expire_time", "600"
            ),
            "mqtt_host": node.metadata.get("signed_url_service", {}).get(
                "mqtt_host", "vernemq"
            ),
            "mqtt_user": node.metadata.get("signed_url_service", {}).get("mqtt_user"),
            "mqtt_pass": node.metadata.get("signed_url_service", {}).get("mqtt_pass"),
            "mqtt_port": node.metadata.get("signed_url_service", {}).get(
                "mqtt_port", "1883"
            ),
            "bucket_nonwoven_grading_images": node.metadata.get(
                "signed_url_service", {}
            ).get("bucket_nonwoven_grading_images"),
            "bucket_condition_monitoring_wav": node.metadata.get(
                "signed_url_service", {}
            ).get("bucket_condition_monitoring_wav"),
            # Must not have trailing slash on riot internal api url
            "riot_internal_api_host": node.metadata.get("signed_url_service", {}).get(
                "riot_internal_api_host",
                "http://"
                + node.metadata.get("signed_url_service").get(
                    "riot_internal_api_host", "riot"
                )
                + ":"
                + node.metadata.get("riot", {}).get("riot_internal_api_port", "8080"),
            ),
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/signed-url-service": {
        "manifest_file": "signed-url-service-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "signed_url_service_internal_port": node.metadata.get(
                "signed_url_service", {}
            ).get("signed_url_service_internal_port", "4000"),
            "service_port": node.metadata.get("signed_url_service", {}).get(
                "service_port", "80"
            ),
            "name": node.metadata.get("signed_url_service", {}).get(
                "name", "signed-url-service"
            ),
        },
    }
}


k8s_ingresses = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/signed-url-service": {
        "manifest_file": "signed-url-service-ingress.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "external_host": node.metadata.get("signed_url_service").get(
                "signed_url_service_host",
                "signed-url-service."
                + node.metadata.get("global").get("domain_suffix"),
            ),
            "service_port": node.metadata.get("signed_url_service", {}).get(
                "service_port", "80"
            ),
            "le_certificates": node.metadata.get("cluster").get("letsencrypt"),
            "secrets_name": node.metadata.get("signed_url_service", {}).get(
                "secrets_name"
            ),
        },
    }
}

k8s_secrets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/gcp-credentials": {
        "manifest": {
            "data": {
                "credentials.json": str(
                    repo.vault.decrypt(
                        node.metadata.get("signed_url_service").get(
                            "credentials", "this-causes-a-fail-if-you-forget"
                        ),
                        key=node.metadata.get("global", {}).get("bw_key"),
                    )
                )
            }
        }
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/signed-url-service": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "signed-url-service"}},
                "policyTypes": ["Ingress", "Egress"],
                "ingress": [
                    {
                        "ports": [{"port": 4000, "protocol": "TCP"}],
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
                        "ports": [{"port": 1883, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "vernemq"}}}],
                    },
                    {
                        "ports": [
                            {"port": 53, "protocol": "UDP"},
                            {"port": 443, "protocol": "TCP"},
                        ]
                    },
                    {
                        "ports": [{"port": 8080, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "riot"}}}],
                    },
                ],
            },
        }
    }
}
