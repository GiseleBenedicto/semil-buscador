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
    replacements = {
        '\u201c': '"', '\u201d': '"',
        '\u2018': "'", '\u2019': "'",
        '\u2013': '-', '\u2014': '-',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def extract_json(text: str):
    text = clean_text(text)
    fence = re.search(r'```json\s*([\s\S]*?)\s*```', text)
    if fence:
        try:
            return json.loads(fence.group(1))
        except:
            pass
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
        return {"error": "Chave de API nao configurada."}

    source_labels = ", ".join([SOURCE_LABELS.get(s, s) for s in req.fontes])

    system_prompt = """Voce e um analista especializado em projetos de infraestrutura e energia do estado de Sao Paulo. Sua funcao e realizar pesquisa aprofundada sobre projetos especificos usando web search extensivo.

INSTRUCOES DE PESQUISA:
Pesquise obrigatoriamente nestas fontes, usando multiplas buscas:
- Governo SP: sp.gov.br, semil.sp.gov.br, desenvolvimentosp.com.br, agenciasp.sp.gov.br, fazenda.sp.gov.br
- Reguladores: anp.gov.br, arsesp.sp.gov.br, cetesb.sp.gov.br, aneel.gov.br
- Transparencia: transparencia.sp.gov.br, portaldatransparencia.gov.br, siafem
- Diario Oficial: imprensaoficial.com.br
- Empresas: comgas.com.br, naturgy.com.br, necta.com.br, orizon.com.br, sabesp.com.br, cpfl.com.br, enel.com.br
- Associacoes: abiogas.org.br, ibp.org.br, abegas.org.br, sindipeças
- Jornais e midia: valor.com.br, folha.com.br, estadao.com.br, g1.globo.com, canalenergia.com.br, epbr.com.br, portalr3.com.br, novacana.com.br, segs.com.br
- Licitacoes: bec.sp.gov.br, comprasnet.gov.br
- BNDES, bancos de fomento, fundos de investimento

REGRA CRITICA DE FORMATO:
Retorne APENAS JSON puro. Nenhum texto fora do JSON. Sem markdown. Sem blocos de codigo.
Use apenas aspas duplas simples ("). Nunca use aspas curvadas.

REGRA CRITICA DE CAMPOS VAZIOS:
Se nao encontrar informacao para um campo, deixe como string vazia "". NAO escreva "Nao localizado" nem "N/A".

ESTRUTURA OBRIGATORIA (retorne exatamente estes campos):
{
  "projeto": "nome completo do projeto/empreendimento",
  "municipio": "municipio(s) onde o projeto esta localizado",
  "regiao_administrativa": "regiao administrativa do estado de SP",
  "regiao_metropolitana": "regiao metropolitana se aplicavel",
  "tipo": "tipo do empreendimento (ex: planta de biometano, gasoduto, usina, etc)",
  "investimento_estado_reais": "valor investido pelo governo estadual em R$",
  "investimento_outros_reais": "valor investido por outras fontes (federal, privado) em R$",
  "populacao_impactada": "numero estimado de habitantes beneficiados",
  "beneficios_populacao": "descricao objetiva dos beneficios diretos a populacao",
  "situacao": "Em andamento ou Parado ou Previsto ou Concluido ou Desconhecido",
  "data_inicio": "data ou periodo de inicio (mes/ano)",
  "data_termino_previsto": "data ou periodo de conclusao prevista (mes/ano)",
  "campo_funcional_semil": "area tematica na SEMIL (ex: Energia, Mineracao, Gas Natural, Biocombustiveis)",
  "produto_ppa": "produto relacionado no PPA 2024-2027 do Estado de SP",
  "politica_plano": "politica publica, decreto ou plano estadual relacionado",
  "observacoes": "sintese factual das principais informacoes encontradas, sem repeticao dos campos acima",
  "fontes": [
    {"titulo": "nome do veiculo ou orgao", "url": "https://url-completa.com/pagina", "descricao": "o que foi encontrado nesta fonte"}
  ],
  "confianca_percentual": numero inteiro de 0 a 100
}"""

    user_msg = f"""Pesquise extensivamente sobre o seguinte projeto de infraestrutura ou energia no estado de Sao Paulo e retorne APENAS o JSON estruturado:

Projeto: {req.projeto}
{f'Municipio: {req.municipio}' if req.municipio else ''}
{f'Tipo: {req.tipo}' if req.tipo else ''}
{f'Contexto adicional: {req.contexto}' if req.contexto else ''}

Fontes prioritarias adicionais solicitadas: {source_labels}

Realize pelo menos 5 buscas diferentes antes de responder. Priorize dados oficiais e recentes (2023-2026)."""

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 6000,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_msg}]
    }

    async with httpx.AsyncClient(timeout=180.0) as client:
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

    # Debug log
    print("=== RAW RESPONSE ===")
    print(repr(raw_text[:500]))
    print("=== DATA KEYS ===")
    print(data.keys() if isinstance(data, dict) else type(data))
    if "error" in data:
        print("API ERROR:", data["error"])

    result = extract_json(raw_text)

    if not result:
        result = {
            "projeto": req.projeto,
            "municipio": req.municipio or "",
            "regiao_administrativa": "",
            "regiao_metropolitana": "",
            "tipo": req.tipo or "",
            "investimento_estado_reais": "",
            "investimento_outros_reais": "",
            "populacao_impactada": "",
            "beneficios_populacao": "",
            "situacao": "Desconhecido",
            "data_inicio": "",
            "data_termino_previsto": "",
            "campo_funcional_semil": "",
            "produto_ppa": "",
            "politica_plano": "",
            "observacoes": raw_text or "",
            "fontes": [],
            "confianca_percentual": 0
        }

    return result
