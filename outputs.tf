output "form_url" {
  value = module.form_page.function_url
}

output "submit_url" {
  value = module.submit_form.function_url
}

output "table_name" {
  value = module.dynamodb.table_name
}