resource "snowflake_role_grants" "openlibrary" {
  for_each = data.snowflake_roles.openlibrary

  enable_multiple_grants = true

  role_name = each.value.roles[0].name
  roles     = each.key == "dev" ? data.snowflake_roles.openlibrary_group.roles[*].name : []
  users     = [snowflake_user.openlibrary.name]
}

resource "snowflake_role_grants" "openlibrary_group_db_reader" {
  count = length(data.snowflake_roles.openlibrary_group_db_reader["prod"].roles)

  enable_multiple_grants = true

  role_name = data.snowflake_roles.openlibrary_group_db_reader["prod"].roles[0].name
  roles     = data.snowflake_roles.openlibrary_group.roles[*].name
}