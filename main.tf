terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.97.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = var.rgname
  location = var.rglocation
}

resource "azurerm_container_registry" "acr" {
  name                = "experience"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "basic"
  admin_enabled       = true
  tags = {
      Future_ready_talent="blogacr"
  }
}

module "web_app_container" {
  source = "innovationnorway/web-app-container/azurerm"

  name = var.waname

  resource_group_name = azurerm_resource_group.rg.name

  container_type = "docker"

  container_image = "experience.azurecr.io/flaskapp:v1"

  plan ={
    name = var.aspname
    sku_size = "B1"
    
  }
  docker_registry_username = "experience"
  docker_registry_url = "experience.azurecr.io/flaskapp:v1"
  docker_registry_password = azurerm_container_registry.acr.admin_password

}
