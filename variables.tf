variable "rgname"{
    type=string
    description="Name of the resource group"
}

variable "rglocation" {
    type=string
    description="Location of the resource group"
  
}

variable "aspname"{
    type = string
    description = "Name of the app service plan"
}

variable "waname" {
    type = string
    description = "web app name"
  
}