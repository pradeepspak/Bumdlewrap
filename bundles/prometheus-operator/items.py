import base64
import glob
import re
from pathlib import Path

data = {}
path_config = {}
main_path = "bundles/prometheus-operator/config/"
k8s_cluster_tag = node.name

# find all .json / .yaml files
for path in Path(main_path).rglob("*.[yj]*"):
    k8s_path = str(path.relative_to(main_path)).replace("/", ".")
    data[k8s_path] = base64.b64encode(
        path.read_text()
        .replace("${opsgenie_team}", node.metadata.get("opsgenie_team", "SRE"))
        .replace("${node_name}", k8s_cluster_tag)
        .encode("utf-8")
    ).decode("utf-8")
    path_config[k8s_path] = str(path.relative_to(main_path))


k8s_clusterrolebindings = {
    "prometheus-operator": {
        "manifest_file": "cluster_role_binding.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "prometheus-operator-crd-view": {
        "manifest_file": "cluster_role_binding_crd_view.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "prometheus-operator-crd-edit": {
        "manifest_file": "cluster_role_binding_crd_edit.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "prometheus": {
        "manifest_file": "prometheus_cluster_role_binding.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
}

k8s_clusterroles = {
    "prometheus-operator": {
        "manifest_file": "cluster_role.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "prometheus-operator-crd-view": {
        "manifest_file": "cluster_role_view.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "prometheus-operator-crd-edit": {
        "manifest_file": "cluster_role_edit.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "prometheus": {
        "manifest_file": "prometheus_cluster_role.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
}

k8s_deployments = {
    "monitoring/prometheus-operator": {
        "manifest_file": "deployment.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    }
}

k8s_serviceaccounts = {
    "monitoring/prometheus-operator": {
        "manifest_file": "service_account.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "monitoring/prometheus": {
        "manifest_file": "prometheus_service_account.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
}

k8s_raw = {
    "monitoring/Prometheus/k8s": {
        "manifest_file": "prometheus.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "storage_class": "default"
            if node.metadata.get("cluster", {}).get("hoster", "") == "AKS"
            else "standard",
            "retention": node.metadata.get("monitoring", {}).get("retention", "7d"),
        },
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
    "monitoring/ServiceMonitor/kube-apiserver": {
        "manifest_file": "kube_apiserver_monitor.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
    "monitoring/ServiceMonitor/kubelet": {
        "manifest_file": "kubelet_monitor.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
    "monitoring/ServiceMonitor/kube-controller-manager": {
        "manifest_file": "kube_controller_manager_monitor.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
    "monitoring/ServiceMonitor/kube-scheduler": {
        "manifest_file": "kube_scheduler_monitor.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
    "monitoring/ServiceMonitor/alertmanager": {
        "manifest_file": "alertmanager_monitor.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
    "monitoring/AlertManager/alertmanager": {
        "manifest_file": "alertmanager.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
    "monitoring/PrometheusRule/rules": {
        "manifest_file": "rules.yaml",
        "needs": ["k8s_deployment:monitoring/prometheus-operator"],
    },
}

k8s_crd = {
    "alertmanagers.monitoring.coreos.com": {
        "manifest_file": "alertmanager.crd.yaml",
        "manifest_processor": "jinja2",
        "needed_by": ["k8s_raw:"],
    },
    "prometheuses.monitoring.coreos.com": {
        "manifest_file": "prometheus.crd.yaml",
        "manifest_processor": "jinja2",
        "needed_by": ["k8s_raw:"],
    },
    "prometheusrules.monitoring.coreos.com": {
        "manifest_file": "prometheusrule.crd.yaml",
        "manifest_processor": "jinja2",
        "needed_by": ["k8s_raw:"],
    },
    "servicemonitors.monitoring.coreos.com": {
        "manifest_file": "servicemonitor.crd.yaml",
        "manifest_processor": "jinja2",
        "needed_by": ["k8s_raw:"],
    },
}

k8s_services = {
    "monitoring/prometheus": {
        "manifest_file": "prometheus_service.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "monitoring/alertmanager": {
        "manifest_file": "alertmanager_service.yaml",
        "manifest_processor": "jinja2",
    },
    "kube-system/kube-scheduler-prometheus-discovery": {
        "manifest_file": "kube_scheduler_service.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
    "kube-system/kube-controller-manager-prometheus-discovery": {
        "manifest_file": "kube_controller_manager_service.yaml",
        "manifest_processor": "jinja2",
        "context": {},
    },
}

k8s_secrets = {
    "monitoring/alertmanager-alertmanager": {"context": {}, "manifest": {"data": data}}
}
