import base64

# reifenhauser-customers
#
# This takes care of deploying all components which are customer specific (redis, reclis)


# The k8s_* must be defined before we can use them to concatenate
# it may be defined previously, but if not we must create it before attempting to update


try:
    k8s_namespaces
except NameError:
    k8s_namespaces = {}

try:
    k8s_deployments
except NameError:
    k8s_deployments = {}

try:
    k8s_pvc
except NameError:
    k8s_pvc = {}

try:
    k8s_services
except NameError:
    k8s_services = {}

try:
    k8s_ingresses
except NameError:
    k8s_ingresses = {}

try:
    k8s_secrets
except NameError:
    k8s_secrets = {}

try:
    k8s_configmaps
except NameError:
    k8s_configmaps = {}

try:
    k8s_raw
except NameError:
    k8s_raw = {}

try:
    k8s_serviceaccounts
except NameError:
    k8s_serviceaccounts = {}

try:
    k8s_networkpolicies
except NameError:
    k8s_networkpolicies = {}


def buildSecretsList(customer):
    allSecrets = {}
    for item, password in (
        node.metadata.get("customers").get(customer).get("passwords", {}).items()
    ):
        allSecrets[item] = base64.b64encode(
            str(
                repo.vault.decrypt(
                    password, key=node.metadata.get("global", {}).get("bw_key")
                )
            ).encode()
        ).decode("utf-8")
    return allSecrets


for customer, config in node.metadata.get("customers", {}).items():
    print("Working on customer", customer)
    # Create a namespace
    namespace = customer + node.metadata.get("global", {}).get("cust-ns-suffix", "")

    k8s_namespaces.update(**{namespace: {}})
    # Create deployments:
    if node.metadata.get("global", {}).get("registry_secret"):
        k8s_secrets.update(
            {
                namespace
                + "/"
                + node.metadata.get("global", {}).get("registry_secret"): {
                    "manifest": {
                        "type": "kubernetes.io/dockerconfigjson",
                        "data": {
                            ".dockerconfigjson": str(
                                repo.vault.decrypt(
                                    node.metadata.get("passwords", {}).get("regcred"),
                                    node.metadata.get("global", {}).get("bw_key"),
                                )
                            )
                        },
                    }
                }
            }
        )
    if node.name == "reifenhaeuser-prod":
        k8s_secrets.update(
            {
                namespace
                + "/pure-iot-wildcard-certs": {
                    "manifest": {
                        "data": {
                            "tls.crt": str(
                                repo.vault.decrypt(
                                    node.metadata.get("base", {}).get("tls_crt"),
                                    key=node.metadata.get("global", {}).get("bw_key"),
                                )
                            ),
                            "tls.key": str(
                                repo.vault.decrypt(
                                    node.metadata.get("base", {}).get("tls_key"),
                                    key=node.metadata.get("global", {}).get("bw_key"),
                                )
                            ),
                        },
                        "metadata": {"name": "pure-iot-wildcard-certs"},
                        "type": "kubernetes.io/tls",
                    }
                }
            }
        )
    k8s_secrets.update(
        {
            namespace
            + "/"
            + node.metadata.get("global", {}).get("bw_password_container"): {
                "manifest": {"data": buildSecretsList(customer)}
            },
            namespace
            + "/alarmstats-ssh": {
                "manifest": {
                    "data": {
                        "id_rsa": str(
                            repo.vault.decrypt(
                                "gAAAAABctE6whLfsJMM3pl1-OuFZfcCvvpY2U57RG5UP-RLyVYKLqI8i7HKfwIkcPgFSBEGsl_fVrB8Xs3-N-uknE-vF35BGGgx0U4M0bJOFf9lDERW_PM3GqxFp75Hv8szYq-tW9396arGI7cwcTPLuCLgmLDVv0U6c7oNHFLCeBbXcKeYkolP_qrkceIB62CKvYkWpveRkA70NEU8gl96aTw4gqhGyw-yzLQtezlz4ZbYS-GVmpVkFl-J0oUc66jzFcSKlwyXp3bO41RcpMB-nQrcBA9RxWjTBbbLoo3HUtAuQ56YykZuhHArE0wWmnDqzfIl-gtWGndc5KksJjyz86fgz8ZpRB75e3XLChGPTjV_-3kgyqBlcTBORnOrxNV8RGo-MEdPT2PFhKZDBrgKkQuN_QjqFaXzl0dGBkIvoRG4UR_ldh2dlz5Qql-Zq5OimyzlvrgpRuf5PVWkE8irbDiFzUO94KGUU7isfAUx8xnUvCVi7SKjBhXtokE3W1w-yeFvJMFZBSzJORBtOejiqkj06qOW44tna6NgUJjSmjQuC7g-5oQwFSTI0BvY7ARNZ3RuL-boJr0CluEijju0vnP9waL4MsCqUNQsX2_gVh3RhllxZo45Gk95r5kXAHhohEhrLW3Sr3elG-3p4PqGk_UVYrGWu5E-FIzkCSx9yRMHeOSgwJSg87zHlxvskRQ3ZAskF3Yldm86ccr4wuvUSja06y6YhZK4UGTbx0lgZBbVrlFy5zT7P3ZNeNxLNryeIWmuyX8q6f0fR9HKLeCUzr33nE0Uv2ZdP35qjgyLOwNKad15xMiPXXhCNT7dvsVNb7MK8y15Fn5dTW05_fOUF2g6upnWyyA79I4TWIRvdY9iQhbE000o_eIa-S9S7yqnU-KwIwxR-dbvI7vucEzWOi1rDi8kVsl9KRUxgdXxCC0VllXQdWalZfZ9lVf_tdot-hSKGx-POGt7O5hfa80pux822eKWmgM4-NxUVGlhYYcU-QfP9jb5SGwxb1372HdTkfabDKJRfkGXz5T46EHni7oh-napS6YzlGd2W5tl-ME-N9DQcTjIVguNQzX2Pe9kl5z7lVmCZbb0VxmyBC_c9aSoDCzdZcHiWuac1HHynaPgV8u_bqq_H9lIVmSG7eXDQwP6zVAn85oK0JcMDLtnh4Ug7I6LKiQ8A_hjcvV5sMUD9j40m0-8k1eYixfBNDrsKj78lxsLsJOhF7eZF5mB9SRFyvNY8JwRYAkxi7OCnPFw2qrvfY1ecWVqVq5QHu51DQsMKDeLl-wiQwabEpS4t1pNEGGxMBJtZQjPUI9JRKhR04VSurOiL3xFRY2MGWIDc2TjZaoMLnvD9KTPhjKhWelxZZXoxqU-y_PcDTLRJItqRZLd3AQSiCWwmFmW6S_HJ3GrIxhxYNeybZZ_Wpy4hMeM5KKPnmRQ_7J27SzA6VXIz1zABqZhWLi6QIR1z9iGX3fP5GvdwT-NiR-hLhDMfrrI0artsrwEgMXs2hirHi2zLJK9NKo_YIYoXeRI4Kxf7ZVNHDFhzvUpkeMGw1ziqnAgUAU5IDDI3jO-pGmrJKAKSAHI2_WlObxBbilmm0mHWmQwYKptgYk-uScgyZguIFedlOysvuti6-067-SOPsy84aCKe5hn2IO_FMp7YWh2Yf7ELFJphkXzmiluUojIOj_3feFRMJJO5MkRBvXQQxTZ98DWjuL8orPuYANdpACGuRDYUQ2THp_iRH-3ijY1UOw1uEH8PBYrGdZ_kcKssH-557QVQHrsHsE3n8nqPjSFACL6xI8dAtI4fTIIP0nAmZWV_kHz5t6AjZDdAuGLQNSgWCJaZYzUBkOReVYnNyjCncgVTo4dHFlwn_5uI3l8ps8SSgK4cvRAz22l8VnQkSkCXyF_JdXgAYt8UMU6P_zO9BglDzD3i4To-NIVHfIAs0H731Mdg5r-QLd54eLMe5AtPZcoZbiy0marjrBL-r5sgmXVv9jdUpCf0eEV4KsBtBh76IzI5OBrgmFZMCzobG3CyIDLszR0xncFw6Q0yVfxJ5hY16N9G3lF136gfP3L_4BfZzIbVbBj9dQhv0PT8_MBunkhExSwe5HiT99-5QSsJ9_2lPaKYrGud4RYGHf1UHUyTZCSKMNlgOVQw6rO4K7mUbP88QnZb7QKtmwQhIB7Epp68FXDn2nIItB8I1S1eVeG1XWVh0TngPfuNkKtH0jpqyRwlymtiKjktqRdNVyI1pjJFLM7hvo4QsENb3ahCnNWhJl9pBH-LeOQJdUHqzdYtFYELNEEIkTNbTiYlXbTRhIyS7uPMijOlYwrrK-q7S5rKngEmaT5xdffSRMggKlj08DpLufAN44ZQzDlgmldB0bNl4uT8jjZEVyCaaIO4Gs_tteEiq7R8UFdZ566NeF0j_y99ilLMcHgUDH8gWKgXivh7PSgujowJmv1opjAhwzwRVEEzCztSwz3d9wyDiifSgrlCZKEav44X_sstKpxaFE5bnjDJwVQ0aD2-PXKkokM2dYOQOXs3QBCRat8GkT9OzP9K99ikgN2gG-KveBRM7YCeY2u0shh5n8713_XzLOCtkRi73V9L00nS1h8tVze1RhUde7wrAO1YeA4naY35AmxA0Obza0kgtMbjouKbFPp492ELe4E8EbPA8JL8Ed5_bDpV-sp6wx1CrRIc8i5BCrOzWqnnefOO7Tg7fUtZar1Lr1pvZ8yJ0vGD3mQ9dAPfeY7SyfwHna9qIiGQU3eSAlBhXQ1AYDteNxXlkmcwh3x7cYhbazU-JiiqoFQcr8N00LVjA6zUrIRWSdyL-ATCskS_ounods5XZgsd2w89mIKt-DkG9oigJOITUbH7Zstsh-DjzAr01EN0EuaNc-wCmwg7YtBly8L8piAhUEsbG8WTg1X0PVOexog3ex5YWA50_9q4jmyEEw9p3npNO3kBBp_4XITHtriTro9sIuRW9ji5ufmPMA4H06yGiiuw05eZVhvqLR-X0xRJsoACF6MEMJj8G55ky0GLUWfkwnZ40MLjAAK2PnjUtcvsYa8xW8VtPzydBX8OdOlvJI5QCk0RGSLpTNzqkELVQ6kfwf27WLRvZp7wXsW9JtajFQuta_xazTHTkQQ2ZgpRNwqhMmTaeafoUZrwcXsz5HoIwkhgBpWpPzdZXlDRNQE4clTWTeHkxfbXQ2_u340OcYKJj1t1mXkAbC7ILoEmCHkIbakXFbuGlFA1nmQFFn96GLOpSS-7AzhM5pmlUS4bTmiC7MqGyW1Q9XJBMMaVP4TTcUznMLY0BqG7rt2MnVdTAthOZQ-4N_DV32AaVsIoGoV7NDsKFVvix43e4Kbw4uOwqzV9Wj4qB7S1YhHB21BUBWGwzNxe4op13-Ng7KE-nQomzm2trqmPwBIwlAkru5KOYJ6kM02I04jgHc1VLS4wfU5wfgsSYk75D-BnO9US0Nh0fP_y2CdC2IE-PdaR6Tk8_LHnes-MX7qg0zhSXzZDhZxCNB2SvziidGOVomOxWXVapk8oc3EtlrFYTcfBTsbw4huOPWtJ0gQb-tIjgp-Nma-7rvY5Z7fscIqoWBltHuyZoNmyJW2WwYCZbyPuri4q3hLMvg-oF7cN8ZnxzR_MXYSkzOvKDq3gyMB2w13RYidbtV23NiYsiWbv370xS6s15sHtaEe7oe9VxdazttlmMMwcd0qoPjKG5_F4c4XkIGjwDBxkUqw8RrDoFKWFOvBITGeWgR4wvjHqUg4nwL48bbeBMUvxpj4gx8D6b9OCTK3Y8L4TwX3SmZeWAt1pMxJ-_02t4ySY75irDj982wJVTTWb0dDr3yWHN3BlpHM6pfeZzaY-FneS9gd_Ja5HxSw9ulm56uDKa4-LZJktJ3rpLtHkBZY-5IqAnezVR-uqwyV5qU8LVXJXT8VY4b_cObKjx3Sw8KU4BpUdhW1KO1sFi_LGGUMEByPwJwzHizXFMvCGLNos6hGDa_oX13z3Z-9KtespeTTEXuvaTkDr8-vVoFqEXfT1fedR8_ml2U1mE6Z3mc1NwyuYo0JY7EQEe51DatBxvk-kA25gEyn0bu61gvrYXiUWLgOk6kLyqB2cncz22JqsOd8UNPrw9lDxAYxZLpeZfUYV-oqmoeOP5fOYw5ge0bFoQX_-iplsW20RK56F0Qj4Lqx2OXmsJse4A5yAv3Bb5ZphSgwdaOsfPHC4rwfWFa60QPyCby2Z9ToAtiBeAY6orYfnJ9TBp8dol84ZLE8LQ5gQpJgfwZbkw3IQ0-PXkpYL1QvnwtQyZ_XQJbs0eC3xJy8E8FP9e8pFePEsAGxXQMasBo1AbL3alIgBBTNJYu_jt6VDBA5-gswcl5UAcJTjFrGGqA5DsolL6O9wIyOPLO49wYvgi4Zuth6TqjK65rFVMSkUYDgItrtKFMwuIGgoIwN1rKqxKY3CFxxetILkGw6vEoSdNF6sOH-EAbauaw1_lt7ElDRS6Jf9acCe3r2anDz3ras_z2QTxqJ3RxyJKj0lyR48bTeHZpzvKZj9JxJcMQVoeXrbMsciay-w0chuHtlpcD5cfiwaUU0RAkdPzE3Hc6jlA3bSQMZ-Nt29pIdR4KXEesZL4Bm9m72QBq4DfGJSlh2T_P5erTLAMwTIt47cEzHVdq06XBvuQ0t_qKuerDizfD7Ydt7QL_T4Zye743tt6N2dI-eh4MvebaDK3bKWQhB8835DZP0XVz6WHr1Y8NjM0mygKvmnNjbpLzKQiM8xUG71ir_3mx0WRxqXhoC0myxmXSmOgVgXPMrEdu0aRwsD1aowM547IpR2tCd-jtyHKHX7zcn6xanj_pmXubj-rO62wdORAOuqWX--ht1Y733QK-6-EdWx44BiYgCdHF3nAWnYAHk2zvJmG3M00T5GPc3FRt-0SBSJNQvFyatX26IZRTKUXSmWVwM3IcKkb6BCyejJr-_pjNCOFQ4IWGuf-iyIPP44qWqmG9G3Hh5wXg8H6EiBaaYbCP3ZLr097pPo7teyE2-oRbwp4tv7CHioarTEULddiwlU7VUUOeZt2-qs7saDuZadeTxKkJ-DdQ3ods2BLK9VYiZkj8HyxheQqPVlRsYyqqcgZVvNVwT_XX4qxLjz1DdSCtHEpuoIAO11a0iDxSQmt3sw6zjo3JmS5htrhOwaI0WqHpWDFxTuXxuhxIzfLd2QK-KIbFz6Ql3tYrPTOR3wwj3RD-ntn_p6gGCpikI1PRqrjGjmjlcUsS8cPLKGoSkWWBgNn3HBpw2lx_9iy6QtjyK_Q45Azmv122mGnVBzWBCun5-9CTDxctqW4VEpEIPsjywaoEVSBtrBcMJNodlG0zZlvOLB0wS9iVX5V3_lbvgINs_i1FpKGbe-64rFF7_BYVnGcoiTlyLOXPQHoyhC-H_qSmJY1ulaNWI2mSB029eNQsCVKkPInKnkykTQ3YwUU4UmSx1og185ZW_LAfIfUBTn4Crv9_SfeCLUD-Rte9HXw5vU7NwONJDlQgtd_oelS9XHPuWCF_btfioB4sRUaSZ_SmclT24miKOf7Eof9ZlB5aitCfmyjwAdkU_WfcQITYr1oRItUSzr7JMdx-34vaIfYW9MW7rf6WITFjcHNvM81qET4V_iwwFlPw3RfMST_kI5KNuyZGyB3muXZapoTd8_8U4w8G3lLDDvzFM7_Ff-AE3WHicxUj2bndcjMbefnPx3rUVXGbdmNXVyanc2PPkWbV3WZzOjjOGrrkrp7rzgEfHY2y4lc-jqUwSq3n-AhUZYp0JcyiH5_baPJ5w7uAoPJYMHIPtpw3bykR4GSMs9uyhNIaKNuhCGt9Qn5EsKUV_y_D-FPVNbn5kYe99I5tImDwSFjSH-UqDXCHbX4Xl4_Ku_b698dLshSH9LPiRDk8gdPjtUlsL42eS_1oAe7s3veVfxU5x5KKy9-WxTSPYCBDWj_vd9WmKV8wcG3LANgnSfQrpmp7D0jH6L1vj_9xHdQJ7b9NUyzMF2XdrCPDmYwAQrnYQMjok9qHo0AlEvscQMDr5445tgwgqWxNlnHDo4cRmppsGxltd4uZq-PfUn5Gx-SeILPwnNoekpIB18fzLBFexMg11nzhtx4ak6ZjZdKIUbEwmzwRGMOoAfCrYxuBsk3nWK_Rk8umk=",
                                key="reifenhauser-stage",
                            )
                        ),
                        "known_hosts": "Z2l0aHViLmdjeGkuZGUsMTg1Ljc5LjEyNC40IGVjZHNhLXNoYTItbmlzdHAyNTYgQUFBQUUyVmpaSE5oTFhOb1lUSXRibWx6ZEhBeU5UWUFBQUFJYm1semRIQXlOVFlBQUFCQkJGY3R6eG16aTBydVJ5aUg3WW83dGxOR0dZS2FqbHg0WTl6SWFyMGdwK2J6d1VoTVh2MGNYNzhHVlFBekE1M3FJd2VaTncwbTdqc21yYzcyS3kzcTZtQT0K",
                    }
                }
            },
        }
    )

    k8s_configmaps.update(
        **{
            namespace
            + "/alarmstats-config": {
                "manifest_file": "alarmstats-configmap.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "influx_host": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get(
                        "influx_host",
                        "influxdb." + node.metadata.get("global").get("namespace"),
                    ),
                    "influx_db": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get("influx_db", customer),
                    "influx_user": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get("influx_user", customer),
                    "influx_pass": str(
                        repo.vault.decrypt(
                            node.metadata.get("customers")
                            .get(customer)
                            .get("alarmstats", {})
                            .get("influx_pass"),
                            key=node.metadata.get("global", {}).get("bw_key"),
                        )
                    ),
                },
            }
        }
    )

    k8s_deployments.update(
        **{
            namespace
            + "/alarmstats": {
                "manifest_file": "alarmstats-deployment.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "env": node.metadata.get("global", {}).get("env", "stage"),
                    "customer": customer,
                    "bw_password_container": node.metadata.get("global", {}).get(
                        "bw_password_container"
                    ),
                    "registry_host": node.metadata.get("global", {}).get(
                        "registry_host"
                    ),
                    "registry_image": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get("registry_image", "prod/alarm_statistics_grafana"),
                    "registry_version": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get("registry_version", "latest"),
                    "replicas": node.metadata.get("customers")
                    .get(customer)
                    .get("redis")
                    .get("replicas", "1"),
                    "alarmstats_git_repository": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get(
                        "alarmstats_git_repository",
                        "git@github.gcxi.de:Reifenhaeuser/alarm_statistics.git",
                    ),
                    # Use the keycloak details from Reclis in order to facilitate SSO
                    # Discussion with Max Frigge
                    "keycloak_realm": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_realm", "master"),
                    "keycloak_external_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "keycloak_external_host",
                        "auth." + node.metadata.get("global").get("domain_suffix"),
                    ),
                    "gf_auth_generic_oauth_client_id": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_client_id", customer),
                    "keycloak_clientsecret": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_clientsecret"),
                    "gf_auth_generic_oauth_allowed_domains": node.metadata.get(
                        "global"
                    ).get("domain_suffix"),
                    "gf_security_secret_key": repo.vault.password_for(
                        customer + "-secret-key"
                    ),
                    "gf_security_admin_password": repo.vault.password_for(
                        customer + "-admin-pass"
                    ),
                    "gf_server_root_url": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get(
                        "external_host",
                        customer
                        + "-alarmstats."
                        + node.metadata.get("global").get("domain_suffix"),
                    ),
                },
            },
            namespace
            + "/redis": {
                "manifest_file": "redis-deployment.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "env": node.metadata.get("global", {}).get("env"),
                    "bw_password_container": node.metadata.get("global", {}).get(
                        "bw_password_container", "bw-managed-secrets"
                    ),
                    "customer": customer,
                    "replicas": node.metadata.get("customers")
                    .get(customer)
                    .get("redis")
                    .get("replicas", "1"),
                },
            },
            namespace
            + "/reclis": {
                "manifest_file": "reclis-deployment.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "env": node.metadata.get("global", {}).get("env", "dev"),
                    "name": "reclis-" + customer,
                    "customer": customer,
                    "bw_password_container": node.metadata.get("global", {}).get(
                        "bw_password_container"
                    ),
                    "registry_host": node.metadata.get("global", {}).get(
                        "registry_host"
                    ),
                    "registry_image": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("registry_image", "reclis"),
                    "registry_version": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("registry_version", "master"),
                    "external_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "external_host",
                        customer
                        + "."
                        + node.metadata.get("global").get("domain_suffix"),
                    ),
                    "internal_port": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("internal_port", "4000"),
                    "replicas": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("replicas", "1"),
                    "postgres_db": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("postgres_db", "reclis-" + customer),
                    "postgres_user": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("postgres_user", "reclis-" + customer),
                    "postgres_pass": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("postgres_pass", "hunter2"),
                    "postgres_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "postgres_host",
                        "postgres." + node.metadata.get("global").get("namespace"),
                    ),
                    "influx_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "influx_host",
                        "influxdb." + node.metadata.get("global").get("namespace"),
                    ),
                    "influx_db": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("influx_db", customer),
                    "alarm_statistics_db": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("alarm_statistics_db", customer + "_alarmstats"),
                    "influx_user": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("influx_user", customer),
                    "influx_pass": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("influx_pass"),
                    "keycloak_realm": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_realm", "master"),
                    "keycloak_session_limit": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_session_limit", "3"),
                    # Must not have trailing slash on keycloak_url
                    "keycloak_external_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "keycloak_external_host",
                        "https://auth."
                        + node.metadata.get("global").get("domain_suffix"),
                    ),
                    # Must call from external host so protocol/url is set correctly
                    # - see REFIOT-926. Can force hostname but not protocol
                    "keycloak_internal_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "keycloak_internal_host",
                        "https://auth."
                        + node.metadata.get("global").get("domain_suffix"),
                    ),
                    "keycloak_admin_username": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_admin_username", "admin-" + customer),
                    "keycloak_admin_password": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_admin_password", "hunter2"),
                    "keycloak_client_id": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_client_id", customer),
                    "keycloak_clientsecret": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("keycloak_clientsecret"),
                    "mqtt_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "mqtt_host",
                        "vernemq." + node.metadata.get("global").get("namespace"),
                    ),
                    "mqtt_user": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("mqtt_user"),
                    "mqtt_pass": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("mqtt_pass"),
                    "secret_key_base": repo.vault.password_for(
                        "reclis secret keybase " + customer
                    ),
                    "replace_os_vars": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("replace_os_vars", "true"),
                    "sentry_dsn": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("sentry_dsn", "http://localhost/0"),
                    "sentry_frontend_dsn": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("sentry_frontend_dsn", "http://localhost/0"),
                    "redis_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("redis_host", "redis"),
                    "redis_port": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("redis_port", "6379"),
                    "redis_password": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("redis_password", ""),
                    "registry_secret": node.metadata.get("global").get(
                        "registry_secret", ""
                    ),
                    "mailjet_api_key": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("mailjet_api_key"),
                    "mailjet_private_key": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("mailjet_private_key"),
                    "contact_form_recipient": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("contact_form_recipient", "info@reifenhauser-digital.com"),
                    # Must not have trailing slash on nowodski api url
                    "nowodski_api_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "nowodski_api_host",
                        "https://nonwovengrading."
                        + node.metadata.get("global", {}).get("domain_suffix", ""),
                    ),
                    "nowodski_service_token": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("nowodski_service_token"),
                    "env": node.metadata.get("global").get("env", "prod"),
                },
            },
        }
    )

    if node.has_bundle("gcp-regional-disk"):
        storage_class = "gcp-regional-disk"
    else:
        storage_class = "standard"

    k8s_pvc.update(
        **{
            namespace
            + "/redis": {
                "manifest_file": "redis-pvc.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "storage_size": node.metadata.get("customers")
                    .get(customer)
                    .get("redis", {})
                    .get("storage_size", "1Gi"),
                    # REFIOT-1286
                    # Google no longer supports <200Gi persistent disks. Existing disks are ok
                    # "storage_class_name": storage_class,
                },
            }
        }
    )
    k8s_services.update(
        **{
            namespace
            + "/redis": {
                "manifest_file": "redis-service.yaml",
                "manifest_processor": "jinja2",
                "context": {"customer": customer},
            },
            namespace
            + "/alarmstats": {
                "manifest_file": "alarmstats-service.yaml",
                "manifest_processor": "jinja2",
                "context": {"customer": customer},
            },
            namespace
            + "/reclis": {
                "manifest_file": "reclis-service.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "env": node.metadata.get("global", {}).get("env", "dev"),
                    "internal_port": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("internal_port", "4000"),
                    "service_port": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("service_port", "80"),
                    "reclis_customer": customer,
                },
            },
        }
    )
    k8s_ingresses.update(
        **{
            namespace
            + "/alarmstats-"
            + customer: {
                "manifest_file": "alarmstats-ingress.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "external_host": node.metadata.get("customers")
                    .get(customer)
                    .get("alarmstats", {})
                    .get(
                        "external_host",
                        customer
                        + "-alarmstats."
                        + node.metadata.get("global").get("domain_suffix"),
                    ),
                    "customer": customer,
                },
            },
            namespace
            + "/reclis-"
            + customer: {
                "manifest_file": "reclis-ingress.yaml",
                "manifest_processor": "jinja2",
                "context": {
                    "external_host": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get(
                        "external_host",
                        customer
                        + "."
                        + node.metadata.get("global").get("domain_suffix"),
                    ),
                    "customer": customer,
                    "service_port": node.metadata.get("customers")
                    .get(customer)
                    .get("reclis", {})
                    .get("service_port", "80"),
                    "le_certificates": node.metadata.get("cluster", {}).get(
                        "letsencrypt"
                    ),
                    "secrets_name": node.metadata.get("customers", {})
                    .get(customer)
                    .get("reclis", {})
                    .get("secrets_name"),
                },
            },
        }
    )
    k8s_raw.update(
        **{
            namespace
            + "/ServiceMonitor/reclis-"
            + customer: {
                "manifest_file": "reclis-servicemonitor.yaml",
                "manifest_processor": "jinja2",
                "context": {"namespace": namespace, "customer": customer},
            }
        }
    )

    k8s_serviceaccounts.update(**{namespace + "/reifenhauser-standard": {}})

    k8s_networkpolicies.update(
        **{
            namespace
            + "/default-deny-all": {
                "manifest": {
                    "apiVersion": "extensions/v1beta1",
                    "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]},
                }
            },
            namespace
            + "/allow-sentry": {
                "manifest": {
                    "apiVersion": "extensions/v1beta1",
                    "spec": {
                        "podSelector": {"matchLabels": {"sentry": "dus"}},
                        "policyTypes": ["Egress"],
                        "egress": [
                            {
                                "ports": [{"port": 443, "protocol": "TCP"}],
                                "to": [{"ipBlock": {"cidr": "185.79.127.14/32"}}],
                            }
                        ],
                    },
                }
            },
            namespace
            + "/allow-mailjet": {
                "manifest": {
                    "apiVersion": "extensions/v1beta1",
                    "spec": {
                        "podSelector": {"matchLabels": {"mail": "mailjet"}},
                        "policyTypes": ["Egress"],
                        "egress": [
                            {
                                "ports": [
                                    {"port": 25, "protocol": "TCP"},
                                    {"port": 465, "protocol": "TCP"},
                                    {"port": 587, "protocol": "TCP"},
                                    {"port": 443, "protocol": "TCP"},
                                ],
                                "to": [
                                    {"ipBlock": {"cidr": "104.199.96.85/32"}},
                                    {"ipBlock": {"cidr": "35.187.79.8/32"}},
                                ],
                            }
                        ],
                    },
                }
            },
            namespace
            + "/redis": {
                "manifest": {
                    "apiVersion": "extensions/v1beta1",
                    "spec": {
                        "podSelector": {"matchLabels": {"app": "redis"}},
                        "policyTypes": ["Ingress"],
                        "ingress": [
                            {
                                "ports": [{"port": 6379, "protocol": "TCP"}],
                                "from": [
                                    {"podSelector": {"matchLabels": {"app": "reclis"}}}
                                ],
                            }
                        ],
                    },
                }
            },
            namespace
            + "/allow-letsencrypt-certbot": {
                "manifest": {
                    "apiVersion": "extensions/v1beta1",
                    "spec": {
                        "podSelector": {
                            "matchLabels": {
                                "certmanager.k8s.io/acme-http01-solver": "true"
                            }
                        },
                        "policyTypes": ["Ingress"],
                        "ingress": [
                            {
                                "ports": [{"port": 8089, "protocol": "TCP"}],
                                "from": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {
                                            "matchLabels": {"app": "ingress-nginx"}
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                }
            },
            namespace
            + "/reclis": {
                "manifest": {
                    "apiVersion": "extensions/v1beta1",
                    "spec": {
                        "podSelector": {"matchLabels": {"app": "reclis"}},
                        "policyTypes": ["Egress", "Ingress"],
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
                            {"ports": [{"port": 53, "protocol": "UDP"}]},
                            {"ports": [{"port": 443, "protocol": "TCP"}]},
                            {
                                "ports": [{"port": 6379, "protocol": "TCP"}],
                                "to": [
                                    {"podSelector": {"matchLabels": {"app": "redis"}}}
                                ],
                            },
                            {
                                "ports": [{"port": 8086, "protocol": "TCP"}],
                                "to": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {
                                            "matchLabels": {"app": "influxdb"}
                                        },
                                    }
                                ],
                            },
                            {
                                "ports": [{"port": 1883, "protocol": "TCP"}],
                                "to": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {
                                            "matchLabels": {"app": "vernemq"}
                                        },
                                    }
                                ],
                            },
                            {
                                "ports": [{"port": 5432, "protocol": "TCP"}],
                                "to": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {
                                            "matchLabels": {"app": "postgres"}
                                        },
                                    }
                                ],
                            },
                            {
                                "ports": [{"port": 8080, "protocol": "TCP"}],
                                "to": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {"matchLabels": {"app": "riot"}},
                                    }
                                ],
                            },
                            {
                                "ports": [{"port": 8080, "protocol": "TCP"}],
                                "to": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {
                                            "matchLabels": {"app": "keycloak"}
                                        },
                                    }
                                ],
                            },
                        ],
                    },
                }
            },
            namespace
            + "/alarmstats": {
                "manifest": {
                    "apiVersion": "extensions/v1beta1",
                    "spec": {
                        "podSelector": {"matchLabels": {"app": "alarmstats"}},
                        "policyTypes": ["Ingress", "Egress"],
                        "ingress": [
                            {
                                "ports": [{"port": 3000, "protocol": "TCP"}],
                                "from": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {
                                            "matchLabels": {"app": "ingress-nginx"}
                                        },
                                    }
                                ],
                            }
                        ],
                        "egress": [
                            {
                                "ports": [
                                    {"port": 53, "protocol": "UDP"},
                                    {"port": 443, "protocol": "TCP"},
                                    {"port": 80, "protocol": "TCP"},
                                ]
                            },
                            {
                                "ports": [{"port": 22, "protocol": "TCP"}],
                                "to": [{"ipBlock": {"cidr": "185.79.124.4/32"}}],
                            },
                            {
                                "ports": [{"port": 8086, "protocol": "TCP"}],
                                "to": [
                                    {
                                        "namespaceSelector": {},
                                        "podSelector": {
                                            "matchLabels": {"app": "influxdb"}
                                        },
                                    }
                                ],
                            },
                        ],
                    },
                }
            },
        }
    )
