k8s_clusterrolebindings = {
    "kube-state-metrics": {
        "manifest_file": "cluster_role_binding.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_clusterroles = {
    "kube-state-metrics": {
        "manifest_file": "cluster_role.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_deployments = {
    "monitoring/kube-state-metrics": {
        "manifest_file": "deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_serviceaccounts = {
    "monitoring/kube-state-metrics": {
        "manifest_file": "service_account.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_services = {
    "monitoring/kube-state-metrics": {
        "manifest_file": "service.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_raw = {
    "kube-system/ServiceMonitor/kube-state-metrics": {
        "manifest_file": "service_monitor.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    }
}
