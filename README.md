# 🧾 StudelyDesk – Helpdesk Ticketing System with Docker & AKS

**StudelyDesk** is a lightweight helpdesk and ticketing web application built with **Flask**. It enables users to easily submit support requests while providing administrators with a streamlined interface to manage and resolve tickets efficiently.

The application is containerized using **Docker**, ensuring consistency across development and production environments. For scalability and cloud-native orchestration, it is deployed on **Azure Kubernetes Service (AKS)**, allowing it to handle growing workloads seamlessly.

---

## 🚀 Features

- User-friendly submission and tracking of helpdesk tickets  
- Admin dashboard to view, update, and resolve tickets  
- RESTful API design for easy integration and extension  
- Fully containerized for portability with Docker  
- Scalable, reliable deployment using Kubernetes on AKS  

---

## 🛠️ Tech Stack

- **Backend:** Python 3 with Flask framework  
- **Frontend:** HTML and CSS with Bootstrap for responsive design  
- **Database:** SQLite (used for demonstration and simplicity)  
- **Containerization:** Docker for creating reproducible application images  
- **Orchestration:** Kubernetes deployed via Azure Kubernetes Service (AKS)  
- **Tools:** Azure CLI and kubectl for managing cloud resources and Kubernetes clusters

---

## ⚙️ CI/CD – Continuous Integration & Deployment

Deployment is automated using **GitHub Actions**, which builds, tags, and pushes the Docker image to **Azure Container Registry (ACR)**, then updates the app on **Azure Kubernetes Service (AKS)** using `kubectl`.

This ensures:
- reliable, hands-off deployments  
- continuous delivery of updates  
- consistency between code, container image, and production

---

## 🐘 Migration from SQLite to PostgreSQL

To prepare the application for production-level use, the database has been migrated from SQLite to **PostgreSQL**.

### Why PostgreSQL?

- Better handling of concurrent users and multiple connections  
- Native support for distributed systems like Kubernetes  
- Compatibility with managed cloud services (e.g. Azure Database for PostgreSQL)  
- Richer data types and improved performance for larger datasets

---
