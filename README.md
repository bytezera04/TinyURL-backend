# 📝 TinyURL Backend

TinyURL Backend is an API that powers a URL shortening service. It allows creating shortened URLs and fetching statistics on the most clicked URLs.

## ✨ Features
- 🔗 Create shortened URLs
- 📊 Fetch statistics for the most clicked URLs
- ⚡ Built with **Python**, **FastAPI**, and **PostgreSQL**
- 🐧 Easy deployment on **Linux**

## 🌐 API Endpoints
# 📝 TinyURL Backend

TinyURL Backend is an API that powers a URL shortening service. It allows creating shortened URLs and fetching statistics on the most clicked URLs.

## ✨ Features
- 🔗 Create shortened URLs
- 📊 Fetch statistics for the most clicked URLs
- ⚡ Built with **Python**, **FastAPI**, and **PostgreSQL**

## 🌐 API Endpoints
- `POST /urls` – Create a new shortened URL
- `GET /urls/top` – Get the most clicked URLs
- `GET /urls/{short_id}` – Get redirect URL data

## 🌐 Frontend
Check out the frontend for this project here: [TinyURL Frontend](https://github.com/bytezera04/TinyURL-frontend)

## 🛠️ Tech Stack
- **Python** – Core language
- **FastAPI** – High-performance API framework
- **PostgreSQL** – Relational database for storing URLs and stats

## 🚀 Deployment
Can be deployed on Linux servers or cloud platforms supporting Python and PostgreSQL.

## 💻 Usage
1. Clone the repository  
   ```bash
   git clone https://github.com/bytezera04/TinyURL-backend.git
   ```  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the server  
   ```bash
   uvicorn main:app --reload
   ```  
4. Access the API at [http://localhost:8000](http://localhost:8000)

## 📄 License
This project is open source.
