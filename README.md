## 🚀 Rodando o Backend (Django) com Docker

### ✅ Pré-requisitos

Você precisa ter o **Docker** e **Docker Compose** instalados em sua máquina.

Caso esteja no **Windows (WSL2)**, recomendamos seguir esse guia de instalação:

👉 [Guia Rápido WSL2 + Docker (codeedu)](https://github.com/codeedu/wsl2-docker-quickstart)

---

### ⚙️ Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/seu-backend.git

copie o .env.example para .env

```bash
cp .env.example .env

e suba o projeto

```bash
docker compose up -d --build

A documentação Swagger estará disponível após o backend subir em:

```bash
http://localhost:8000/swagger/