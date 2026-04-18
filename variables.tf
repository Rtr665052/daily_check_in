variable "aws_region" {
  type = string
}

variable "project_name" {
  type = string
}

variable "sender_email" {
  type = string
}

variable "recipient_email" {
  type = string
}

variable "schedule_expression" {
  type = string
}

variable "timezone" {
  type = string
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