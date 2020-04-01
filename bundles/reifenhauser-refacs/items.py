k8s_deployments = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/refacs": {
        "manifest_file": "refacs-deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "bw_password_container": node.metadata.get("global", {}).get(
                "bw_password_container", "bw-managed-secrets"
            ),
            "name": node.metadata.get("refacs", {}).get("name"),
            "replicas": node.metadata.get("refacs", {}).get("replicas"),
            "registry_host": node.metadata.get("global", {}).get(
                "registry_host", "rfhregistry.azurecr.io"
            ),
            "registry_image": node.metadata.get("refacs", {}).get("registry_image"),
            "registry_version": node.metadata.get("refacs", {}).get("registry_version"),
            "refacs_host": node.metadata.get("refacs", {}).get("refacs_host"),
            "refacs_tmp": node.metadata.get("refacs", {}).get("refacs_tmp"),
            "mssql_db": node.metadata.get("refacs", {}).get("mssql_db"),
            "mssql_host": node.metadata.get("refacs", {}).get("mssql_host"),
            "mssql_user": node.metadata.get("refacs", {}).get("mssql_user"),
            "mssql_pass": node.metadata.get("refacs", {}).get("mssql_pass"),
            "sqllite_db": node.metadata.get("refacs", {}).get("sqllite_db"),
            "api_key": node.metadata.get("refacs", {}).get("api_key"),
            "secret_key": node.metadata.get("refacs", {}).get("secret_key"),
            "replace_os_vars": node.metadata.get("refacs", {}).get("replace_os_vars"),
            "sentry_url": node.metadata.get("refacs", {}).get("sentry_url"),
            "registry_secret": node.metadata.get("global", {}).get("registry_secret"),
        },
    }
}

k8s_services = {
    node.metadata.get("global", {}).get("namespace", "default")
    + "/refacs": {
        "manifest_file": "refacs-service.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "env": node.metadata.get("global", {}).get("env", "dev"),
            "name": node.metadata.get("refacs", {}).get("name"),
            "name": "refacs",
            "service_port": node.metadata.get("refacs", {}).get("service_port"),
            "internal_port": node.metadata.get("refacs", {}).get("internal_port"),
        },
    }
}
# Todo: I don't think a PV is necessary; Removed from deployment
# k8s_pvc = {
#  node.metadata.get('global', {}).get('namespace', 'default')+'/refacs': {
#    'manifest_file': 'refacs-pvc.yaml',
#    'manifest_processor': 'jinja2',
#    'context': {
#      'storageclass': 'volume.beta.kubernetes.io/storage-class: default',
#      'access_mode': 'ReadWriteOnce',
#      'size': '8Gi',
#      },
#    },
# }
