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

def clean_text(text: str) -> str:
    """Normalize fancy quotes and special chars to ASCII equivalents."""
    replacements = {
        '\u201c': '"', '\u201d': '"',  # curly double quotes
        '\u2018': "'", '\u2019': "'",  # curly single quotes
        '\u2013': '-', '\u2014': '-',  # en/em dash
        '\u00e9': 'e', '\u00e3': 'a', '\u00e7': 'c',  # accented (keep if needed)
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def extract_json(text: str):
    text = clean_text(text)
    
    # Strategy 1: ```json ... ``` fence
    fence = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if fence:
        try:
            return json.loads(fence.group(1))
        except:
            pass

    # Strategy 2: find outermost { } block (longest wins)
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

    # Strategy 3: strip control chars and retry
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
    'google': 'Google / Midia geral',
    'doe': 'Diario Oficial SP',
    'transparencia': 'Portal Transparencia / SIAFEM',
    'prefeituras': 'Sites de prefeituras',
    'licitacoes': 'BEC / ComprasNet',
    'regulacao': 'ANP / ARSESP / CETESB',
    'concessionarias': 'Comgas / Naturgy / NECTA',
    'associacoes': 'Abiogas / IBP / Associacoes',
    'noticias': 'Portais de noticias setoriais',
}

@app.post("/buscar")
async def buscar(req: SearchRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "Chave de API nao configurada no servidor."}

    source_labels = ", ".join([SOURCE_LABELS.get(s, s) for s in req.fontes])

    system_prompt = """Voce e um analista especializado em projetos de infraestrutura e energia do estado de Sao Paulo. Sua funcao e buscar e estruturar dados sobre projetos especificos solicitados pela SEMIL-SP, Subsecretaria de Energia e Mineracao.

REGRA CRITICA: Retorne APENAS um objeto JSON valido e nada mais. Sem texto antes, sem texto depois, sem markdown, sem blocos de codigo, sem aspas especiais. Apenas o JSON puro iniciando com { e terminando com }.

Use APENAS aspas duplas simples (") nos campos JSON. Nunca use aspas tipograficas ou curvadas.

Estrutura obrigatoria:
{"projeto":"string","municipio":"string","regiao_administrativa":"string","regiao_metropolitana":"string","tipo":"string","investimento_estado_reais":"string","investimento_outros_reais":"string","populacao_impactada":"string","beneficios_populacao":"string","situacao":"Em andamento ou Parado ou Previsto ou Concluido ou Desconhecido","data_inicio":"string","data_termino_previsto":"string","campo_funcional_semil":"string","produto_ppa":"string","politica_plano":"string","observacoes":"string","fontes_encontradas":["string"],"confianca_percentual":0}

Para campos sem informacao use "Nao localizado". Nao use caracteres especiais dentro dos valores de string que possam quebrar o JSON."""

    user_msg = f"""Busque informacoes sobre o projeto abaixo e retorne APENAS o JSON:

Projeto: {req.projeto}
{f'Municipio: {req.municipio}' if req.municipio else ''}
{f'Tipo: {req.tipo}' if req.tipo else ''}
{f'Contexto: {req.contexto}' if req.contexto else ''}
Fontes: {source_labels}"""

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

    raw_text = ""
    if "content" in data:
        for block in data["content"]:
            if block.get("type") == "text":
                raw_text += block.get("text", "")

    result = extract_json(raw_text)

    if not result:
        result = {
            "projeto": req.projeto,
            "municipio": req.municipio or "Nao localizado",
            "regiao_administrativa": "",
            "regiao_metropolitana": "",
            "tipo": req.tipo or "Nao localizado",
            "investimento_estado_reais": "Nao localizado",
            "investimento_outros_reais": "Nao localizado",
            "populacao_impactada": "Nao localizado",
            "beneficios_populacao": "Nao localizado",
            "situacao": "Desconhecido",
            "data_inicio": "Nao localizado",
            "data_termino_previsto": "Nao localizado",
            "campo_funcional_semil": "Nao localizado",
            "produto_ppa": "",
            "politica_plano": "",
            "observacoes": raw_text or "Nao foi possivel estruturar os dados.",
            "fontes_encontradas": req.fontes,
            "confianca_percentual": 10
        }

    return result
