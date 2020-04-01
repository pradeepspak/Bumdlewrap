k8s_namespaces = {
    "cert-manager": {
        "manifest": {
            "metadata": {"labels": {"certmanager.k8s.io/disable-validation": "true"}}
        }
    }
}

k8s_crd = {
    "certificaterequests.certmanager.k8s.io": {
        "manifest_file": "certificaterequests.certmanager.k8s.io.crd.yaml"
    },
    "certificates.certmanager.k8s.io": {
        "manifest_file": "certificates.certmanager.k8s.io.crd.yaml"
    },
    "challenges.certmanager.k8s.io": {
        "manifest_file": "challenges.certmanager.k8s.io.crd.yaml"
    },
    "clusterissuers.certmanager.k8s.io": {
        "manifest_file": "clusterissuers.certmanager.k8s.io.crd.yaml"
    },
    "issuers.certmanager.k8s.io": {
        "manifest_file": "issuers.certmanager.k8s.io.crd.yaml"
    },
    "orders.certmanager.k8s.io": {
        "manifest_file": "orders.certmanager.k8s.io.crd.yaml"
    },
}

k8s_clusterroles = {
    # Old bundle used 'certmanager-role', if this is found it can be removed in favour of what is below
    "certmanager-role": {"delete": True},
    "cert-manager-edit": {"manifest_file": "cert-manager-edit.clusterrole.yaml"},
    "cert-manager-view": {"manifest_file": "cert-manager-view.clusterrole.yaml"},
    "cert-manager-webhook-webhook-requester": {
        "manifest_file": "cert-manager-webhook.clusterrole.yaml"
    },
    "cert-manager-cainjector": {
        "manifest_file": "cert-manager-cainjector.clusterrole.yaml"
    },
    "cert-manager-controller-certificates": {
        "manifest_file": "cert-manager-controller-certificates.clusterrole.yaml"
    },
    "cert-manager-controller-challenges": {
        "manifest_file": "cert-manager-controller-challenges.clusterrole.yaml"
    },
    "cert-manager-controller-clusterissuers": {
        "manifest_file": "cert-manager-controller-clusterissuers.clusterrole.yaml"
    },
    "cert-manager-controller-ingress-shim": {
        "manifest_file": "cert-manager-controller-ingress-shim.clusterrole.yaml"
    },
    "cert-manager-controller-issuers": {
        "manifest_file": "cert-manager-controller-issuers.clusterrole.yaml"
    },
    "cert-manager-controller-orders": {
        "manifest_file": "cert-manager-controller-orders.clusterrole.yaml"
    },
    "cert-manager-leaderelection": {
        "manifest_file": "cert-manager-leaderelection.clusterrole.yaml"
    },
}
k8s_serviceaccounts = {
    # Old bundle used 'certmanager', if this is found it can be removed in favour of new serviceaccounts
    "cert-manager/certmanager": {"delete": True},
    "cert-manager/cert-manager": {
        "manifest": {"metadata": {"labels": {"app": "cert-manager"}}}
    },
    "cert-manager/cert-manager-cainjector": {
        "manifest": {"metadata": {"labels": {"app": "cainjector"}}}
    },
    "cert-manager/cert-manager-webhook": {
        "manifest": {"metadata": {"labels": {"app": "webhook"}}}
    },
}

k8s_deployments = {
    # Old bundle used 'certmanager' as the deployment name.
    # If this is found it can be removed in favour of cert-manager
    "cert-manager/certmanager": {"delete": True},
    "cert-manager/cert-manager": {"manifest_file": "cert-manager.deployment.yaml"},
    "cert-manager/cert-manager-cainjector": {
        "manifest_file": "cert-manager-cainjector.deployment.yaml"
    },
    "cert-manager/cert-manager-webhook": {
        "manifest_file": "cert-manager-webhook.deployment.yaml"
    },
}

k8s_services = {
    "cert-manager/cert-manager": {"manifest_file": "cert-manager.service.yaml"},
    "cert-manager/cert-manager-webhook": {
        "manifest_file": "cert-manager-webhook.service.yaml"
    },
}

k8s_rolebindings = {
    "kube-system/cert-manager-webhook-webhook-authentication-reader": {
        "manifest_file": "kube-system.cert-manager-webhook-webhook-authentication-reader.rolebinding.yaml"
    }
}

k8s_clusterrolebindings = {
    # Old bundle used 'certmanager-rolebinding', if this is found it can be removed in favour of what is below
    "certmanager-rolebinding": {"delete": True},
    "cert-manager-cainjector": {
        "manifest_file": "cert-manager-cainjector.clusterrolebinding.yaml"
    },
    "cert-manager-controller-certificates": {
        "manifest_file": "cert-manager-controller-certificates.clusterrolebinding.yaml"
    },
    "cert-manager-controller-challenges": {
        "manifest_file": "cert-manager-controller-challenges.clusterrolebinding.yaml"
    },
    "cert-manager-controller-clusterissuers": {
        "manifest_file": "cert-manager-controller-clusterissuers.clusterrolebinding.yaml"
    },
    "cert-manager-controller-ingress-shim": {
        "manifest_file": "cert-manager-controller-ingress-shim.clusterrolebinding.yaml"
    },
    "cert-manager-controller-issuers": {
        "manifest_file": "cert-manager-controller-issuers.clusterrolebinding.yaml"
    },
    "cert-manager-controller-orders": {
        "manifest_file": "cert-manager-controller-orders.clusterrolebinding.yaml"
    },
    "cert-manager-leaderelection": {
        "manifest_file": "cert-manager-leaderelection.clusterrolebinding.yaml"
    },
    "cert-manager-webhook-auth-delegator": {
        "manifest_file": "cert-manager-webhook-auth-delegator.clusterrolebinding.yaml"
    },
}

# cert-manager/letsencrypt was the old secret used by the cluster issuer letsencrypt
# Re-named to letsencrypt-account-key
k8s_secrets = {"cert-manager/letsencrypt": {"delete": True}}

k8s_raw = {
    "cert-manager/clusterissuers/letsencrypt-staging-http01": {
        "manifest_file": "letsencrypt-staging-clusterissuer.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "lego_email": node.metadata.get("ingress", {}).get(
                "lego_email", "ops+letsencrypt-default-bw@grandcentrix.net"
            )
        },
        "needs": ["k8s_crd:clusterissuers.certmanager.k8s.io"],
    },
    "cert-manager/clusterissuers/letsencrypt-http01": {
        "manifest_file": "letsencrypt-prod-clusterissuer.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "lego_email": node.metadata.get("ingress", {}).get(
                "lego_email", "ops+letsencrypt-default-bw@grandcentrix.net"
            )
        },
        "needs": ["k8s_crd:clusterissuers.certmanager.k8s.io"],
    },
    # The following is to ensure backwards compatiblity for old ingresses using
    # 'letsencrypt' clusterissuer. New should always use explicit letsencrypt-http01
    # This is a copy of letsencrypt-http01
    "cert-manager/clusterissuers/letsencrypt": {
        "manifest_file": "letsencrypt-prod-clusterissuer.yaml",
        "manifest_processor": "jinja2",
        "context": {
            "lego_email": node.metadata.get("ingress", {}).get(
                "lego_email", "ops+letsencrypt-default-bw@grandcentrix.net"
            )
        },
        "needs": ["k8s_crd:clusterissuers.certmanager.k8s.io"],
    },
}
