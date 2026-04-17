resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "person_id"
  range_key    = "submission_date"

  attribute {
    name = "person_id"
    type = "S"
  }

  attribute {
    name = "submission_date"
    type = "S"
  }
}