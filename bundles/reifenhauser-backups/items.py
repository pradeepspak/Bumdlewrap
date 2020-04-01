k8s_cronjobs = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/backupjob-influxdb": {
        "manifest_file": "backup_job.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "backup_bucket": node.metadata.get("backups").get("backup_bucket"),
            "registry_image": node.metadata.get("backups", {}).get(
                "registry_image", "backup"
            ),
            "registry_version": node.metadata.get("backups", {}).get(
                "registry_version", "master"
            ),
            "registry_host": node.metadata.get("global", {}).get("registry_host"),
        },
    }
}

k8s_secrets = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/backup-bucket-credentials": {
        "manifest": {
            "data": {
                "credentials.json": str(
                    repo.vault.decrypt(
                        node.metadata.get("backups", {}).get("backup_credentials"),
                        key=node.metadata.get("global", {}).get("bw_key"),
                    )
                )
            }
        }
    }
}


k8s_networkpolicies = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/influx-backups": {
        "manifest": {
            "apiVersion": "extensions/v1beta1",
            "spec": {
                "podSelector": {"matchLabels": {"app": "influx-backup"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "ports": [
                            {"port": 53, "protocol": "UDP"},
                            {"port": 443, "protocol": "TCP"},
                        ]
                    },
                    {
                        "ports": [{"port": 8088, "protocol": "TCP"}],
                        "to": [{"podSelector": {"matchLabels": {"app": "influxdb"}}}],
                    },
                ],
            },
        }
    }
}
