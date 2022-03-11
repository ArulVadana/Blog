output "acr-login-server" {
    value = azurerm_container_registry.acr.login_server
    description="Displays the login server"
  
}
 output "acr-admin-user" {
     value = azurerm_container_registry.acr.admin_username
     description = "admin username of acr"
   
 }

 