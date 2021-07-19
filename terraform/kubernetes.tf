provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
}

resource "kubernetes_deployment" "very-first-eks-deployment" {
  metadata {
    name = "precision-map-deployment"
    labels = {
      app = "precision-map"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "precision-map"
      }
    }

    template {
      metadata {
        labels = {
          app = "precision-map"
        }
      }

      spec {
        container {
          image = local.image_id
          name  = "precision-map"
          port {
            container_port = 5000
          }
          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }
        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_service" "very-first-eks-service" {
  metadata {
    name = "precision-map-service"
  }
  spec {
    selector = {
      app = "precision-map"
    }
    port {
      port        = 80
      target_port = 5000
    }

    type = "LoadBalancer"
  }
}
