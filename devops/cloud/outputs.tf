output "sage_docs_bucket_name" {
  description = "Nome del bucket sage-docs"
  value       = google_storage_bucket.sage_docs.name
}

output "sage_docs_bucket_url" {
  description = "URL gs:// del bucket sage-docs"
  value       = google_storage_bucket.sage_docs.url
}
