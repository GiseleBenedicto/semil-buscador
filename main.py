import os
import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

class SearchRequest(BaseModel):
    projeto: str
    municipio: str = ""
    tipo: str = ""
    contexto: str = ""
    fontes: list[str] = []

def extract_json(text: str):
    # Strategy 1: ```json ... ``` fence
    fence = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if fence:
        try:
            return json.loads(fence.group(1))
        except:
            pass
    # Strategy 2: find outermost { } candidates, try longest first
    candidates = []
    depth = 0
    start = -1
    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start != -1:
                candidates.append(text[start:i+1])
                start = -1
    for c in sorted(candidates, key=len, reverse=True):
        try:
            return json.loads(c)
        except:
            pass
    # Strategy 3: strip control chars
    try:
        clean = re.sub(r'[\x00-\x1F\x7F]', ' ', text)
        clean = re.sub(r'```json|```', '', clean)
        m = re.search(r'\{[\s\S]*\}', clean)
        if m:
            return json.loads(m.group(0))
    except:
        pass
    return None

SOURCE_LABELS = {
    'google': 'Google / Mídia geral',
    'doe': 'Diário Oficial SP',
    'transparencia': 'Portal Transparência / SIAFEM',
    'prefeituras': 'Sites de prefeituras',
    'licitacoes': 'BEC / ComprasNet',
    'regulacao': 'ANP / ARSESP / CETESB',
    'concessionarias': 'Comgás / Naturgy / NECTA',
    'associacoes': 'Abiogás / IBP / Associações',
    'noticias': 'Portais de notícias setoriais',
}

@app.post("/buscar")
async def buscar(req: SearchRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "Chave de API não configurada no servidor."}

    source_labels = ", ".join([SOURCE_LABELS.get(s, s) for s in req.fontes])

    system_prompt = """Você é um analista especializado em projetos de infraestrutura e energia do estado de São Paulo, com acesso a múltiplas fontes de informação. Sua função é buscar e estruturar dados sobre projetos específicos solicitados pela Secretaria de Meio Ambiente, Infraestrutura e Logística (SEMIL-SP), especialmente sua Subsecretaria de Energia e Mineração.

Para cada projeto consultado, retorne EXCLUSIVAMENTE um objeto JSON válido (sem markdown, sem texto fora do JSON) com a seguinte estrutura:

{
  "projeto": "nome do projeto",
  "municipio": "município ou lista de municípios",
  "regiao_administrativa": "região administrativa do estado de SP ou vazia",
  "regiao_metropolitana": "região metropolitana ou vazia",
  "tipo": "tipo do empreendimento",
  "investimento_estado_reais": "valor em R$ ou vazio",
  "investimento_outros_reais": "valor em R$ ou vazio",
  "populacao_impactada": "número de habitantes ou vazio",
  "beneficios_populacao": "descrição dos benefícios",
  "situacao": "Em andamento | Parado | Previsto | Concluído | Desconhecido",
  "data_inicio": "mês/ano ou ano",
  "data_termino_previsto": "mês/ano ou ano",
  "campo_funcional_semil": "campo funcional relevante na SEMIL",
  "produto_ppa": "produto do PPA 2024-2027 relacionado ou vazio",
  "politica_plano": "política ou plano estadual relacionado",
  "observacoes": "síntese das informações encontradas, fontes consultadas, e grau de confiança dos dados (Alto/Médio/Baixo). Mencionar URLs ou publicações quando disponíveis.",
  "fontes_encontradas": ["lista de fontes onde informações foram localizadas"],
  "confianca_percentual": número entre 0 e 100
}

Priorize informações de: Diário Oficial do Estado de SP, ANP, ARSESP, CETESB, portais de transparência estadual, sites de concessionárias (Comgás, Naturgy, NECTA), Abiogás, IBP, e portais de notícias setoriais. Período de relevância: projetos iniciados após janeiro/2023 ou com previsão de conclusão após dezembro/2026.

Se não encontrar dados suficientes, preencha com "Não localizado" e explique nas observações."""

    user_msg = f"""Busque informações sobre o seguinte projeto/empreendimento de infraestrutura ou energia no estado de São Paulo:

Projeto: {req.projeto}
{f'Município: {req.municipio}' if req.municipio else ''}
{f'Tipo: {req.tipo}' if req.tipo else ''}
{f'Contexto adicional: {req.contexto}' if req.contexto else ''}

Fontes prioritárias solicitadas: {source_labels}

Retorne o JSON estruturado conforme orientado."""

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4000,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_msg}]
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "web-search-2025-03-05"
            },
            json=payload
        )
        data = response.json()

    # Extract text blocks
    raw_text = ""
    if "content" in data:
        for block in data["content"]:
            if block.get("type") == "text":
                raw_text += block.get("text", "")

    result = extract_json(raw_text)

    if not result:
        result = {
            "projeto": req.projeto,
            "municipio": req.municipio or "Não localizado",
            "regiao_administrativa": "",
            "regiao_metropolitana": "",
            "tipo": req.tipo or "Não localizado",
            "investimento_estado_reais": "Não localizado",
            "investimento_outros_reais": "Não localizado",
            "populacao_impactada": "Não localizado",
            "beneficios_populacao": "Não localizado",
            "situacao": "Desconhecido",
            "data_inicio": "Não localizado",
            "data_termino_previsto": "Não localizado",
            "campo_funcional_semil": "Não localizado",
            "produto_ppa": "",
            "politica_plano": "",
            "observacoes": raw_text or "Não foi possível estruturar os dados retornados.",
            "fontes_encontradas": req.fontes,
            "confianca_percentual": 10
        }

    return result
