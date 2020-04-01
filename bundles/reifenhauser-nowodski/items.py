k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nowodski": {
        "manifest_file": "nowodski-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "prod"),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("nowodski", {}).get("name", "nowodski"),
            "replicas": node.metadata.get("nowodski", {}).get("replicas", "2"),
            "registry_image": node.metadata.get("nowodski", {}).get(
                "registry_image", "nowodski"
            ),
            "registry_version": node.metadata.get("nowodski", {}).get(
                "registry_version", "master"
            ),
            "registry_host": node.metadata.get("global", {}).get("registry_host"),
            "keycloak_clientname": node.metadata.get("nowodski", {}).get(
                "keycloak_clientname", "nowodski"
            ),
            "keycloak_clientsecret": node.metadata.get("nowodski", {}).get(
                "keycloak_clientsecret"
            ),
            "keycloak_realm": node.metadata.get("nowodski", {}).get("keycloak_realm"),
            "keycloak_session_limit": node.metadata.get("nowodski", {}).get(
                "keycloak_session_limit", "2"
            ),
            # Must not have trailing slash on keycloak_url
            "keycloak_external_host": node.metadata.get("nowodski", {}).get(
                "keycloak_external_host",
                "https://auth." + node.metadata.get("global").get("domain_suffix"),
            ),
            "keycloak_internal_host": node.metadata.get("nowodski", {}).get(
                "keycloak_internal_host",
                "http://"
                + node.metadata.get("nowodski").get(
                    "keycloak_internal_host", "keycloak"
                ),
            ),
            "postgres_db": node.metadata.get("nowodski", {}).get(
                "postgres_db", "nowodski"
            ),
            "postgres_user": node.metadata.get("nowodski", {}).get(
                "postgres_user", "nowodski"
            ),
            "postgres_pass": node.metadata.get("nowodski", {}).get("postgres_pass"),
            "postgres_host": node.metadata.get("global", {}).get(
                "postgres_host", "postgres"
            ),
            "nowodski_host": node.metadata.get("nowodski", {}).get(
                "nowodski_host",
                "nonwovengrading." + node.metadata.get("global").get("domain_suffix"),
            ),
            "nowodski_internal_port": node.metadata.get("nowodski", {}).get(
                "nowodski_internal_port", "4000"
            ),
            "nowodski_secret_key": node.metadata.get("nowodski", {}).get(
                "nowodski_secret_key"
            ),
            "sentry_dsn": node.metadata.get("nowodski", {}).get(
                "sentry_dsn", "http://localhost/0"
            ),
            "sentry_frontend_dsn": node.metadata.get("nowodski", {}).get(
                "sentry_frontend_dsn", "http://localhost/0"
            ),
            "replace_os_vars": node.metadata.get("nowodski", {}).get(
                "replace_os_vars", "true"
            ),
            "redis_hostname": node.metadata.get("nowodski", {}).get(
                "redis_hostname", "redis"
            ),
            "gcp_bucket_name": node.metadata.get("nowodski", {}).get(
                "gcp_bucket_name", "nonwoven-grading-images-stage"
            ),
            "gcp_project": node.metadata.get("nowodski", {}).get(
                "gcp_project", "reifenhauser-stage"
            ),
            "gcp_pubsub_subscription": node.metadata.get("nowodski", {}).get(
                "gcp_pubsub_subscription", "image-uploaded"
            ),
            "redis_port": node.metadata.get("nowodski", {}).get("redis_port", "6379"),
            "mqtt_host": node.metadata.get("nowodski", {}).get("mqtt_host", "vernemq"),
            "mqtt_user": node.metadata.get("nowodski", {}).get("mqtt_user"),
            "mqtt_pass": node.metadata.get("nowodski", {}).get("mqtt_pass"),
            "mqtt_port": node.metadata.get("nowodski", {}).get("mqtt_port", "1883"),
            "mailjet_api_key": node.metadata.get("global", {}).get("mailjet_api_key"),
            "mailjet_private_key": node.metadata.get("global", {}).get(
                "mailjet_private_key"
            ),
            # Must not have trailing slash on riot internal api url
            "riot_internal_api_host": node.metadata.get("nowodski", {}).get(
                "riot_internal_api_host",
                "http://"
                + node.metadata.get("nowodski").get("riot_internal_api_host", "riot")
                + ":"
                + node.metadata.get("riot", {}).get("riot_internal_api_port", "8080"),
            ),
            "nowodspy_api_host": node.metadata.get("nowodski", {}).get(
                "nowodspy_api_host", "http://nowodspy"
            ),
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nowodski": {
        "manifest_file": "nowodski-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "nowodski_internal_port": node.metadata.get("nowodski", {}).get(
                "nowodski_internal_port", "4000"
            ),
            "service_port": node.metadata.get("nowodski", {}).get("service_port", "80"),
            "name": node.metadata.get("nowodski", {}).get("name", "nowodski"),
        },
    }
}


k8s_ingresses = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nowodski": {
        "manifest_file": "nowodski-ingress.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "external_host": node.metadata.get("nowodski").get(
                "nowodski_host",
                "nonwovengrading." + node.metadata.get("global").get("domain_suffix"),
            ),
            "service_port": node.metadata.get("nowodski", {}).get("service_port", "80"),
            "le_certificates": node.metadata.get("cluster", {}).get("letsencrypt"),
            "secrets_name": node.metadata.get("nowodski", {}).get("secrets_name"),
        },
    }
}


k8s_secrets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nowodski-gcp-credentials": {
        "manifest": {
            "data": {
                "pubsub-credentials.json": str(
                    repo.vault.decrypt(
                        node.metadata.get("nowodski").get(
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
    + "/ServiceMonitor/nowodski": {
        "manifest_file": "nowodski-servicemonitor.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "namespace": node.metadata.get("global", {}).get("namespace", "default")
        },
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/nowodski": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "nowodski"}},
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
                    },
                    {
                        "ports": [{"port": 9568, "protocol": "TCP"}],
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
                        "ports": [{"port": 8080, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "keycloak"}}}],
                    },
                    {
                        "ports": [{"port": 6379, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "redis"}}}],
                    },
                    {
                        "ports": [{"port": 1883, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "vernemq"}}}],
                    },
                    {
                        "ports": [
                            {"port": 443, "protocol": "TCP"},
                            {"port": 53, "protocol": "UDP"},
                        ]
                    },
                    {
                        "ports": [{"port": 80, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "nowodspy"}}}],
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
