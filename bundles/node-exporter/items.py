k8s_namespaces = {
    "monitoring": {"manifest": {"metadata": {"labels": {"purpose": "monitoring"}}}}
}

k8s_daemonsets = {
    "kube-system/node-exporter": {
        "manifest_file": "daemon_set.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_serviceaccounts = {
    "kube-system/node-exporter": {
        "manifest_file": "service_account.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_services = {
    "kube-system/node-exporter": {
        "manifest_file": "service.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_raw = {
    "kube-system/ServiceMonitor/node-exporter": {
        "manifest_file": "service_monitor.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    }
}
