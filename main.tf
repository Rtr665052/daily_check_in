terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  project = var.project_name
}

module "dynamodb" {
  source     = "./modules/dynamodb"
  table_name = "${local.project}-responses"
}

module "lambda_iam" {
  source             = "./modules/lambda_iam"
  project_name       = local.project
  dynamodb_table_arn = module.dynamodb.table_arn
}

module "submit_form" {
  source = "./modules/lambda"

  function_name       = "${local.project}-submit-form"
  source_dir          = "${path.root}/lambda/submit_form"
  role_arn            = module.lambda_iam.role_arn
  runtime             = "python3.12"
  handler             = "app.lambda_handler"
  create_function_url = true

  environment_variables = {
    SENDER_EMAIL        = var.sender_email
    RECIPIENT_EMAIL     = var.recipient_email
    SCHEDULE_EXPRESSION = var.schedule_expression
    TIMEZONE            = var.timezone
    PROJECT_NAME        = var.project_name
    TABLE_NAME          = module.dynamodb.table_name
  }

  cors_allow_origins = var.cors_allow_origins
  cors_allow_methods = var.cors_allow_methods
  cors_allow_headers = var.cors_allow_headers
}

module "form_page" {
  source = "./modules/lambda"

  function_name       = "${local.project}-form-page"
  source_dir          = "${path.root}/lambda/form_page"
  role_arn            = module.lambda_iam.role_arn
  runtime             = "python3.12"
  handler             = "app.lambda_handler"
  create_function_url = true

  environment_variables = {
    PROJECT_NAME = var.project_name
    SUBMIT_URL   = module.submit_form.function_url
  }

  cors_allow_origins = var.cors_allow_origins
  cors_allow_methods = var.cors_allow_methods
  cors_allow_headers = var.cors_allow_headers
}

module "daily_email" {
  source = "./modules/lambda"

  function_name = "${local.project}-daily-email"
  source_dir    = "${path.root}/lambda/daily_email"
  role_arn      = module.lambda_iam.role_arn
  runtime       = "python3.12"
  handler       = "app.lambda_handler"

  environment_variables = {
    SENDER_EMAIL     = var.sender_email
    RECIPIENT_EMAIL  = var.recipient_email
    PROJECT_NAME     = var.project_name
    TIMEZONE         = var.timezone
    FORM_URL         = module.form_page.function_url
  }
}

module "scheduler_iam" {
  source            = "./modules/scheduler_iam"
  project_name      = local.project
  target_lambda_arn = module.daily_email.function_arn
}

module "scheduler" {
  source              = "./modules/scheduler"
  name                = "${local.project}-daily-email"
  schedule_expression = var.schedule_expression
  timezone            = var.timezone
  target_arn          = module.daily_email.function_arn
  role_arn            = module.scheduler_iam.role_arn
}
