variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "daily-checkin"
}

variable "sender_email" {
  type = string
}

variable "recipient_email" {
  type = string
}

variable "schedule_expression" {
  type    = string
  default = "cron(0 8 * * ? *)"
}

variable "timezone" {
  type    = string
  default = "America/New_York"
}