resource "aws_iam_role" "this" {
  name = "${var.project_name}-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = "sts:AssumeRole"
      Principal = {
        Service = "scheduler.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "invoke" {
  name = "${var.project_name}-scheduler-invoke"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "lambda:InvokeFunction"
      Resource = var.target_lambda_arn
    }]
  })
}

resource "aws_iam_role_policy_attachment" "invoke" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.invoke.arn
}