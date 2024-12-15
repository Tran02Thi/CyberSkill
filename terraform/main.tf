
terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "2.15.0" 
    }
  }
}


provider "docker" {
  host = "tcp://localhost:2375"
}

# Tạo một network cho MinIO container
resource "docker_network" "backend" {
  name = "minio_network"
}

# Định nghĩa MinIO container
resource "docker_container" "minio" {
  name  = "minio"
  image = "minio/minio:latest"
  ports {
    internal = 9000
    external = 9000
  }
  ports {
    internal = 9001
    external = 9001
  }
  networks_advanced {
    name = docker_network.backend.name
  }
  env = [
    "MINIO_ACCESS_KEY=admin",
    "MINIO_SECRET_KEY=admin123"
  ]
  command = ["server", "/data", "--console-address", ":9001"]
}