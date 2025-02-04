module "environment_admin" {
  for_each = var.environments

  source      = "../modules/environment_admin"
  environment = each.value
}

data "snowflake_roles" "openlibrary_group" {
  pattern = "OPENLIBRARY_GROUP"
}