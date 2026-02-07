terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 3.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

locals {
  namespace = "default"

  # Apply every YAML in /k8s except secret.yml
  manifest_files = [
    for f in fileset("${path.module}/k8s", "*.yml") : f
    if lower(f) != "secret.yml"
  ]
}

resource "kubernetes_manifest" "my_app" {
  for_each = toset(local.manifest_files)

  manifest = merge(
    yamldecode(file("${path.module}/k8s/${each.value}")),
    {
      metadata = merge(
        try(yamldecode(file("${path.module}/k8s/${each.value}")).metadata, {}),
        {
          namespace = local.namespace
        }
      )
    }
  )
}
