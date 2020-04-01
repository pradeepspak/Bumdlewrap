# k8s_namespaces = {
# node.metadata.get("ingress", {}).get("namespace", "ingress-nginx"): {}
# }

k8s_daemonsets = {
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/default-http-backend": {"manifest_file": "default-http-backend.yaml"},
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/nginx-ingress-controller": {
        "manifest_file": "nginx-ingress-controller.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "hosting_environment": node.metadata.get("cluster", {}).get("hoster", {}),
            "default_backend_service": node.metadata.get("ingress", {}).get(
                "default_backend_service", "default-http-backend"
            ),
            "k8s_worker_spread_across_zones": node.metadata.get("cluster", {}).get(
                "k8s_worker_spread_across_zones", "false"
            ),
        },
    },
}

k8s_services = {
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/default-http-backend": {"manifest_file": "default-http-backend-svc.yaml"},
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/nginx-prometheus-export": {"manifest_file": "ingress-nginx-svc-monitor.yaml"},
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/ingress-nginx": {
        "manifest_file": "ingress-nginx-svc-lb.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "loadbalancer_ip": node.metadata.get("ingress", {}).get(
                "loadbalancer_ip", {}
            )
        },
    },
}
k8s_configmaps = {
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/nginx-configuration": {"manifest_file": "nginx-configuration.yaml"},
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/tcp-services": {"manifest_file": "tcp-services.yaml"},
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/udp-services": {"manifest_file": "udp-services.yaml"},
}


k8s_clusterrolebindings = {
    "nginx-ingress-clusterrole-nisa-binding": {
        "manifest_file": "nginx-crb.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "namespace": node.metadata.get("ingress", {}).get(
                "namespace", "ingress-nginx"
            )
        },
    }
}

k8s_clusterroles = {
    "nginx-ingress-clusterrole": {"manifest_file": "nginx-ingress-cr.yaml"}
}

k8s_serviceaccounts = {
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/nginx-ingress-serviceaccount": {}
}

k8s_raw = {
    node.metadata.get("ingress", {}).get("namespace", "ingress-nginx")
    + "/ServiceMonitor/ingress-nginx": {
        "manifest_file": "nginx_monitor.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "namespace": node.metadata.get("ingress", {}).get(
                "namespace", "ingress-nginx"
            )
        },
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    }
}
