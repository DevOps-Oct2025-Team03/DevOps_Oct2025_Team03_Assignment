resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "app-secrets"
    namespace = "default"
  }

  # Keep plaintext here — provider will handle the right encoding/storage
  data = {
    SECRET_KEY   = "replace_me"
    DATABASE_URL = "postgresql://postgres:postgres@db:5432/appdb"
  }

  type = "Opaque"
}
