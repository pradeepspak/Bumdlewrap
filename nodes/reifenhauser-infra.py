nodes["reifenhaeuser-stage-infra"] = {
    "os": "kubernetes",
    "kubectl_context": "gke_reifenhauser-stage_europe-west3-a_rfh-stage",
    "bundles": [
        "gcx-certmanager",
        "grafana",
        "prometheus-operator",
        "node-exporter",
        "kube-state-metrics",
        "gcx-ingress-nginx",
    ],
    "metadata": {
        "opsgenie_team": "Reifenhauser",
        "ops_domain": "staging.pure-iot.com",
        "ops_groups": ["[GHE] Reifenhaeuser Backend Developers"],
        "cluster": {
            "hoster": "GKE",
            "location": "europe-west3",
            "k8s_worker_spread_across_zones": "false",
        },
        "global": {
            "namespace": "stage",
            "bw_key": "reifenhauser-stage",
            "bw_password_container": "bw-managed-secrets",
            "env": "stage",
            "registry_host": "eu.gcr.io/reifenhauser-prod",
            "postgres_host": "postgres",
            "mailjet_api_key": "0bb4538ec0ff1a8506a3e41d894650a0",
            "mailjet_private_key": "mailjet_private_key",
            "domain_suffix": "staging.pure-iot.com",
            "cust-ns-suffix": "-stage",
        },
        "ingress": {
            "namespace": "cert-manager",
            "lego_email": "sean.mitchell@grandcentrix.net",
            "loadbalancer_ip": "35.246.233.124",
        },
    },
}

nodes["reifenhaeuser-prod-infra"] = {
    "os": "kubernetes",
    "kubectl_context": "gke_reifenhauser-prod_europe-west3-a_rfh-prod",
    "bundles": [
        "gcx-certmanager",
        "grafana",
        "prometheus-operator",
        "node-exporter",
        "kube-state-metrics",
        "gcx-ingress-nginx",
    ],
    "metadata": {
        "opsgenie_team": "Reifenhauser",
        "ops_domain": "pure-iot.com",
        "ops_groups": ["[GHE] Reifenhaeuser Backend Developers"],
        "cluster": {
            "hoster": "GKE",
            "location": "europe-west3",
            "k8s_worker_spread_across_zones": "true",
        },
        "global": {
            "namespace": "rfh-prod",
            "bw_key": "reifenhauser-prod",
            "bw_password_container": "bw-managed-secrets",
            "env": "prod",
            "registry_host": "eu.gcr.io/reifenhauser-prod",
            "postgres_host": "postgres",
            "mailjet_api_key": "0bb4538ec0ff1a8506a3e41d894650a0",
            "mailjet_private_key": "mailjet_private_key",
            "domain_suffix": "pure-iot.com",
        },
        "ingress": {
            "namespace": "cert-manager",
            "lego_email": "sean.mitchell@grandcentrix.net",
            "loadbalancer_ip": "35.246.247.70",
        },
    },
}
