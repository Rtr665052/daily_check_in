variable "function_name" {
  type = string
}

variable "source_dir" {
  type = string
}

variable "role_arn" {
  type = string
}

variable "runtime" {
  type = string
}

variable "handler" {
  type = string
}

variable "create_function_url" {
  type    = bool
  default = false
}

variable "environment_variables" {
  type    = map(string)
  default = {}
}

variable "cors_allow_origins" {
  type    = list(string)
  default = ["*"]
}

variable "cors_allow_methods" {
  type    = list(string)
  default = ["GET", "POST"]
}

variable "cors_allow_headers" {
  type    = list(string)
  default = ["content-type"]
}