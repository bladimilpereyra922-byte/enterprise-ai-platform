# 🏢 Plataforma de IA Empresarial

## 📌 Descripción
Sistema empresarial con microservicios, inteligencia artificial, ERP y multimedia.  
**Portafolio profesional** de Bladimil Pereyra - Systems Architect.

---

## 🏗️ Arquitectura

| Módulo | Tecnología | Función |
|--------|------------|---------|
| **ERP Connector** | FastAPI + PostgreSQL | Gestión de productos + Conexión SAP |
| **AI Expert** | LangChain + Ollama | Text-to-SQL y RAG con IA local |
| **Media Service** | Node.js + Express | TMDB (películas) + Spotify (música) |
| **Workflow Engine** | n8n | Automatización de procesos |
| **Dashboard** | Next.js + Tailwind | Interfaz unificada |

---

## 🚀 Tecnologías

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes)

---

## 📦 Servicios

| Servicio | URL |
|----------|-----|
| **Dashboard** | http://localhost:3000 |
| **ERP API** | http://localhost:8000 |
| **AI Expert** | http://localhost:8001 |
| **Media Service** | http://localhost:8002 |
| **n8n** | http://localhost:5678 |

---

## 🔧 Cómo ejecutar

```bash
# Clonar el repositorio
git clone https://github.com/bladimilpereyra922-byte/enterprise-ai-platform.git

# Levantar todos los servicios con Docker
docker-compose up -d

# Acceder al dashboard
# http://localhost:3000
