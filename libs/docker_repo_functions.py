import json
import requests
import datetime


def get_current_image_tag(
    registry_prefix, project_id, image_name, password, user="_json_key"
):
    """
    registry_prefix:  the registry-FQDN like eu.gcr.io, gcr.io, docker.azure.XYZ, ...
    project_id:       the project_id in GKE
    image_name:       the name of the docker image
    password:         password to access private registry. In the case of GCR, this is the json
                      string containing the private-key for a service account.
    user (optional):  username to access registry. In the case of GCR, this is "_json_key"
    """
    # _json_key is used for Google Container Registry
    if user == "_json_key":
        url = "https://{registry}/v2/{project}/{repo}/tags/list".format(
            registry=registry_prefix, project=project_id, repo=image_name
        )
        response = requests.get(url, auth=(user, password))
        content = json.loads(response.text)
        time_stamp = 0
        latest_tag = ""
        for digest in content["manifest"].items():
            if int(digest[1]["timeUploadedMs"]) > time_stamp:
                time_stamp = int(digest[1]["timeUploadedMs"])
                latest_tag = digest[1]["tag"]
        try:
            image_tag = latest_tag[0]
        except IndexError:
            print(
                "Oops: No tags found for "
                + registry_prefix
                + "/"
                + project_id
                + "/"
                + image_name
            )
            print("Please ensure at least one tag is pushed and try again")
            exit(1)
    # Else if we're dealing with Azure CR
    elif "azurecr.io" in registry_prefix:
        url = "https://{registry}/acr/v1/{repo}/_manifests".format(
            registry=registry_prefix, repo=image_name
        )
        response = requests.get(url, auth=(user, password))
        content = json.loads(response.text)
        time_stamp = datetime.datetime.strptime("1970-01-01", "%Y-%m-%d")
        latest_tag = ""
        for manifest in content["manifests"]:
            manifest_timestamp = datetime.datetime.strptime(
                manifest["lastUpdateTime"][:-3], "%Y-%m-%dT%H:%M:%S.%f"
            )
            if manifest_timestamp > time_stamp:
                try:
                    latest_tag = manifest["tags"][0]
                    time_stamp = manifest_timestamp
                except KeyError:
                    # Sometimes the manifest may not have any tags associated.
                    continue
        if latest_tag == "":
            # We've scanned everything and found nothing
            print(
                "No tags found in ACR. Please ensure at least one tag is pushed and try again"
            )
            exit(1)
        image_tag = latest_tag
    # Future: Add additional registry logic
    else:
        print(
            "Error: Cannot understand the registry used for latest image calculation. Please use ACR or GCR"
        )
        exit(1)

    return image_tag
