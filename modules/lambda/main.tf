resource "null_resource" "artifacts_dir" {
  provisioner "local-exec" {
    command = "mkdir -p ${path.root}/.terraform-artifacts"
  }
}

data "archive_file" "this" {
  depends_on  = [null_resource.artifacts_dir]
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.root}/.terraform-artifacts/${var.function_name}.zip"
}

resource "aws_lambda_function" "this" {
  function_name    = var.function_name
  role             = var.role_arn
  runtime          = var.runtime
  handler          = var.handler
  filename         = data.archive_file.this.output_path
  source_code_hash = data.archive_file.this.output_base64sha256

  environment {
    variables = var.environment_variables
  }
}

resource "aws_lambda_function_url" "this" {
  count = var.create_function_url ? 1 : 0

  function_name      = aws_lambda_function.this.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = var.cors_allow_origins
    allow_methods = var.cors_allow_methods
    allow_headers = var.cors_allow_headers
  }
}