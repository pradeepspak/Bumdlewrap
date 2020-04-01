gcx-certmanager
===============

This will provide letsencrypt certificates to your bundle'd project.

Use this to make https Just Work inside of Kubernetes.

How to use
==========

By default, this will use the lets-encrypt generate certificates, if you include one of the following annotations on your ingress:
```
certmanager.k8s.io/cluster-issuer: letsencrypt-http01
certmanager.k8s.io/cluster-issuer: letsencrypt-staging-http01
```

Include the following
```
        "ingress": {

        },
```

This will create a staging certificate, with ops Email as the certificate admin, and place everything in the cert-manager namespace.

It is recommended you override the email, so you will be notified about your expiring certificates should anything go wrong with renewals.

```
        "ingress": {
            "lego_email": "sean.mitchell@grandcentrix.net",
        },
```

Debugging
=========

Certificates should be created in the secret named in an ingress

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    certmanager.k8s.io/cluster-issuer: letsencrypt-staging-http01
    ingress.kubernetes.io/ssl-redirect: "true"
    kubernetes.io/ingress.class: nginx
    kubernetes.io/tls-acme: "true"
  name: seantest
spec:
  rules:
  - host: sean.example.com
    http:
      paths:
      - backend:
          serviceName: some-webapp
          servicePort: 80
        path: /
  tls:
  - hosts:
    - sean.example.com
    secretName: sean-ssl-cert
```

Logs are available from the certmanager pod runnin in the cert-manager namespace. Here is an example of a test certificate:

```
I1026 12:42:42.994343       1 controller.go:171] certificates controller: syncing item 'stage/sean-ssl-cert'
I1026 12:42:42.994475       1 sync.go:274] Preparing certificate stage/sean-ssl-cert with issuer
I1026 12:42:42.994705       1 logger.go:43] Calling GetOrder
I1026 12:42:43.252086       1 logger.go:73] Calling GetAuthorization
I1026 12:42:43.446138       1 logger.go:93] Calling HTTP01ChallengeResponse
I1026 12:42:43.446167       1 prepare.go:279] Cleaning up old/expired challenges for Certificate stage/sean-ssl-cert
I1026 12:42:43.446187       1 logger.go:68] Calling GetChallenge
I1026 12:42:53.647161       1 prepare.go:488] Accepting challenge for domain "sean.example.com"
I1026 12:42:53.647196       1 logger.go:63] Calling AcceptChallenge
I1026 12:42:54.432298       1 prepare.go:500] Waiting for authorization for domain "sean.example.com"
I1026 12:42:54.432323       1 logger.go:78] Calling WaitAuthorization
I1026 12:42:56.453421       1 prepare.go:510] Successfully authorized domain "sean.example.com"
I1026 12:42:56.453479       1 prepare.go:303] Cleaning up challenge for domain "sean.example.com" as part of Certificate stage/sean-ssl-cert
I1026 12:42:57.302075       1 ingress.go:49] Looking up Ingresses for selector certmanager.k8s.io/acme-http-domain=1643645074,certmanager.k8s.io/acme-http-token=835194346
I1026 12:42:57.513903       1 helpers.go:201] Found status change for Certificate "sean-ssl-cert" condition "ValidateFailed": "False" -> "False"; setting lastTransitionTime to 2018-10-26 12:42:57.513892227 +0000 UTC m=+603029.310947667
I1026 12:42:57.513940       1 sync.go:281] Issuing certificate...
I1026 12:42:57.514105       1 logger.go:43] Calling GetOrder
I1026 12:42:57.518454       1 controller.go:168] ingress-shim controller: syncing item 'stage/cm-acme-http-solver-ktn7m'
E1026 12:42:57.518477       1 controller.go:198] ingress 'stage/cm-acme-http-solver-ktn7m' in work queue no longer exists
I1026 12:42:57.518488       1 controller.go:182] ingress-shim controller: Finished processing work item "stage/cm-acme-http-solver-ktn7m"
I1026 12:42:57.899515       1 logger.go:58] Calling FinalizeOrder
I1026 12:42:59.361016       1 issue.go:196] successfully obtained certificate: cn="sean.example.com" altNames=[sean.example.com] url="https://acme-v02.api.letsencrypt.org/acme/order/44549255/138477170"
I1026 12:42:59.498353       1 sync.go:300] Certificate issued successfully
I1026 12:42:59.498396       1 helpers.go:201] Found status change for Certificate "sean-ssl-cert" condition "Ready": "False" -> "True"; setting lastTransitionTime to 2018-10-26 12:42:59.498391188 +0000 UTC m=+603031.295446528
I1026 12:42:59.500909       1 sync.go:206] Certificate stage/sean-ssl-cert scheduled for renewal in 1438 hours
I1026 12:42:59.604192       1 controller.go:185] certificates controller: Finished processing work item "stage/sean-ssl-cert"
```


