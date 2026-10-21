# Su GCP l'equivalente di ECR è Artifact Registry
resource "google_artifact_registry_repository" "main" {
  project       = var.project_id
  location      = var.region
  repository_id = var.resource_prefix
  description   = "Repository Docker per ${var.resource_prefix}"
  format        = "DOCKER"

  depends_on = [google_project_service.apis]
}
