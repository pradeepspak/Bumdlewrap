k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/riot": {
        "manifest_file": "riot-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env"),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("riot", {}).get("name", "riot"),
            "replicas": node.metadata.get("riot", {}).get("replicas", "1"),
            "registry_image": node.metadata.get("riot", {}).get(
                "registry_image", "riot"
            ),
            "registry_version": node.metadata.get("riot", {}).get(
                "registry_version", "master"
            ),
            "registry_host": node.metadata.get("global", {}).get("registry_host"),
            "keycloak_admin_user": node.metadata.get("riot", {}).get(
                "keycloak_admin_user", "riot_keycloak_admin"
            ),
            "keycloak_admin_pass": node.metadata.get("riot", {}).get(
                "keycloak_admin_pass"
            ),
            "keycloak_clientname": node.metadata.get("riot", {}).get(
                "keycloak_clientname", "riot"
            ),
            "keycloak_clientsecret": node.metadata.get("riot", {}).get(
                "keycloak_clientsecret"
            ),
            "keycloak_realm": node.metadata.get("riot", {}).get("keycloak_realm"),
            "keycloak_session_limit": node.metadata.get("riot", {}).get(
                "keycloak_session_limit", "2"
            ),
            # Must not have trailing slash on keycloak_url
            "keycloak_external_host": node.metadata.get("riot", {}).get(
                "keycloak_external_host",
                "https://auth." + node.metadata.get("global").get("domain_suffix"),
            ),
            "keycloak_internal_host": node.metadata.get("riot", {}).get(
                "keycloak_internal_host",
                "http://"
                + node.metadata.get("riot").get("keycloak_internal_host", "keycloak"),
            ),
            "postgres_db": node.metadata.get("riot", {}).get("postgres_db", "riot"),
            "postgres_user": node.metadata.get("riot", {}).get("postgres_user", "riot"),
            "postgres_pass": node.metadata.get("riot", {}).get("postgres_pass"),
            "postgres_host": node.metadata.get("global", {}).get(
                "postgres_host", "postgres"
            ),
            "riot_host": node.metadata.get("riot", {}).get(
                "riot_host", "riot." + node.metadata.get("global").get("domain_suffix")
            ),
            "riot_secret_key": node.metadata.get("riot", {}).get("riot_secret_key"),
            "mail_from": node.metadata.get("riot", {}).get(
                "mail_from", "riot@example.org"
            ),
            "mail_subject": node.metadata.get("riot", {}).get(
                "mail_subject", "RIOT-Email"
            ),
            "replace_os_vars": node.metadata.get("riot", {}).get(
                "replace_os_vars", "true"
            ),
            "redis_hostname": node.metadata.get("riot", {}).get(
                "redis_hostname", "redis"
            ),
            "redis_port": node.metadata.get("riot", {}).get("redis_port", "6379"),
            "mqtt_host": node.metadata.get("riot", {}).get("mqtt_host", "vernemq"),
            "mqtt_user": node.metadata.get("riot", {}).get("mqtt_user"),
            "mqtt_pass": node.metadata.get("riot", {}).get("mqtt_pass"),
            "mqtt_port": node.metadata.get("riot", {}).get("mqtt_port", "1883"),
            "sentry_dsn": node.metadata.get("riot", {}).get(
                "sentry_dsn", "http://localhost/0"
            ),
            "sentry_frontend_dsn": node.metadata.get("riot", {}).get(
                "sentry_frontend_dsn", "http://localhost/0"
            ),
            "env": node.metadata.get("global").get("env", "prod"),
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/riot": {
        "manifest_file": "riot-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "name": node.metadata.get("riot", {}).get("name", "riot"),
        },
    }
}


k8s_ingresses = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/riot": {
        "manifest_file": "riot-ingress.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "external_host": node.metadata.get("riot").get(
                "riot_host", "riot." + node.metadata.get("global").get("domain_suffix")
            ),
            "le_certificates": node.metadata.get("cluster", {}).get("letsencrypt"),
            "secrets_name": node.metadata.get("riot", {}).get("secrets_name"),
        },
    }
}

k8s_raw = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/ServiceMonitor/riot": {
        "manifest_file": "riot-servicemonitor.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "namespace": node.metadata.get("global", {}).get("namespace", "default")
        },
    }
}

k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/riot": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "riot"}},
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
                        "ports": [{"port": 8080, "protocol": "TCP"}],
                        "from": [
                            {
                                "namespaceSelector": {},
                                "podSelector": {
                                    "matchLabels": {"riot-int-api-access": "allow"}
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
                        "ports": [{"port": 1883, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "vernemq"}}}],
                    },
                    {
                        "ports": [{"port": 5432, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "postgres"}}}],
                    },
                    {
                        "ports": [{"port": 6379, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "redis"}}}],
                    },
                    {"ports": [{"port": 443, "protocol": "TCP"}]},
                    {"ports": [{"port": 53, "protocol": "UDP"}]},
                ],
            },
        }
    }
}
