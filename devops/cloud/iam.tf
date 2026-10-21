# Nota: account_id deve essere lungo 6-30 caratteri
resource "google_service_account" "main" {
  project      = var.project_id
  account_id   = var.resource_prefix
  display_name = var.resource_prefix
  description  = "Service account per il servizio Cloud Run ${var.resource_prefix}"

  depends_on = [google_project_service.apis]
}

# Permesso di chiamare Vertex AI (Gemini)
resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.main.email}"
}
