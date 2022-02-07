import random
import string
import time
import sys
from os import getenv
from azure.common.client_factory import get_client_from_auth_file
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup,
                                                 Container,
                                                 ContainerGroupNetworkProtocol,
                                                 ContainerGroupRestartPolicy,
                                                 ContainerPort,
                                                 EnvironmentVariable,
                                                 IpAddress,
                                                 Port,
                                                 ResourceRequests,
                                                 ResourceRequirements,OperatingSystemTypes)



def main():
    azure_region = 'eastus'
    resource_group_name = 'Blog'
                                
    container_group_name = 'app'
    container_image_app = "microsoft/aci-helloworld"

    auth_file_path = getenv('AZURE_AUTH_LOCATION', None)
    if auth_file_path is not None:
        print("Authenticating with Azure using credentials in file at {0}"
              .format(auth_file_path))

        aciclient = get_client_from_auth_file(
            ContainerInstanceManagementClient)
        resclient = get_client_from_auth_file(ResourceManagementClient)
    else:
        print("\nFailed to authenticate to Azure. Have you set the"
              " AZURE_AUTH_LOCATION environment variable?\n")                                        

    print("Creating resource group '{0}'...".format(resource_group_name))
    resclient.resource_groups.create_or_update(resource_group_name,
                                               {'location': azure_region})
    resource_group = resclient.resource_groups.get(resource_group_name)

    # Demonstrate various container group operations
    create_container_group(aciclient, resource_group, container_group_name,
                           container_image_app)

    list_container_groups(aciclient, resource_group)
    print_container_group_details(aciclient,
                                  resource_group,
                                  multi_container_group_name)

def create_container_group(aci_client, resource_group,
                           container_group_name, container_image_name):

    print("Creating container group '{0}'...".format(container_group_name))

    container_resource_requests = ResourceRequests(memory_in_gb=1, cpu=1.0)
    container_resource_requirements = ResourceRequirements(
        requests=container_resource_requests)
    container = Container(name=container_group_name,
                          image=container_image_name,
                          resources=container_resource_requirements,
                          ports=[ContainerPort(port=80)])

    ports = [Port(protocol=ContainerGroupNetworkProtocol.tcp, port=80)]
    group_ip_address = IpAddress(ports=ports,
                                 dns_name_label=container_group_name,
                                 type="Public")
    group = ContainerGroup(location=resource_group.location,
                           containers=[container],
                           os_type=OperatingSystemTypes.linux,
                           ip_address=group_ip_address)

    aci_client.container_groups.create_or_update(resource_group.name,
                                                 container_group_name,
                                                 group)

    container_group = aci_client.container_groups.get(resource_group.name,
                                                      container_group_name)

    print("Once DNS has propagated, container group '{0}' will be reachable at"
          " http://{1}".format(container_group_name,
                               container_group.ip_address.fqdn))

def print_container_group_details(aci_client, resource_group, container_group_name):
    print("Getting container group details for container group '{0}'..."
          .format(container_group_name))

    container_group = aci_client.container_groups.get(resource_group.name,
                                                      container_group_name)
    print("------------------------")
    print("Name:   {0}".format(container_group.name))
    print("State:  {0}".format(container_group.provisioning_state))
    print("FQDN:   {0}".format(container_group.ip_address.fqdn))
    print("IP:     {0}".format(container_group.ip_address.ip))
    print("Region: {0}".format(container_group.location))
    print("Containers:")
    for container in container_group.containers:
        print("  Name:  {0}".format(container.name))
        print("  Image: {0}".format(container.image))
        print("  State: {0}".format(
            container.instance_view.current_state.state))
        print("  ----------")


if __name__ == "__main__":
    main()