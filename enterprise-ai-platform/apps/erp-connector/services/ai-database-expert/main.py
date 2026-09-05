from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os
import httpx
import json

# ===== CONFIGURACIÓN =====
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secure_password_123@localhost:5432/enterprise")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

app = FastAPI(title="AI Database Expert", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== SCHEMAS =====
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    results: list
    explanation: str

# ===== ENDPOINT PRINCIPAL =====
@app.post("/api/ai/text-to-sql", response_model=QueryResponse)
async def text_to_sql(request: QueryRequest):
    """Convierte lenguaje natural a SQL usando Ollama"""
    
    prompt = f"""
    Eres un experto en SQL. Convierte esta pregunta a SQL:
    "{request.question}"
    
    La base de datos tiene una tabla 'products' con:
    - id (integer)
    - name (varchar)
    - sku (varchar)
    - price (float)
    - stock (integer)
    - category (varchar)
    - created_at (timestamp)
    
    Devuelve SOLO la consulta SQL, sin explicación.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_HOST}/api/generate",
                json={
                    "model": "qwen2.5-coder:7b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise HTTPException(500, "Error en Ollama")
            
            sql = response.json().get("response", "").strip()
            sql = sql.replace("```sql", "").replace("```", "").strip()
            
            # Ejecutar SQL en la base de datos
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                result = conn.execute(text(sql))
                rows = [dict(row._mapping) for row in result]
                
            return QueryResponse(
                sql=sql,
                results=rows,
                explanation=f"Consulta generada y ejecutada correctamente. {len(rows)} resultados."
            )
            
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.get("/api/ai/health")
def health_check():
    return {"status": "operational", "service": "AI Expert"}
