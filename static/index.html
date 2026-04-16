<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEMIL · Buscador de Projetos</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --ink: #0f1923;
    --paper: #f5f0e8;
    --sage: #3d6b4f;
    --sage-light: #e8f0eb;
    --amber: #c4822a;
    --amber-light: #fdf3e3;
    --mist: #8a9ba8;
    --line: #d8d0c0;
    --white: #ffffff;
    --red: #b94040;
    --red-light: #fdf0f0;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'DM Sans', sans-serif; background: var(--paper); color: var(--ink); min-height: 100vh; }
  header { background: var(--ink); padding: 18px 32px; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid var(--amber); }
  .logo { font-family: 'DM Serif Display', serif; font-size: 1.4rem; color: var(--paper); letter-spacing: 0.02em; }
  .logo span { color: var(--amber); }
  .badge { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--mist); letter-spacing: 0.1em; text-transform: uppercase; }
  .container { max-width: 1100px; margin: 0 auto; padding: 40px 24px; }
  .intro { margin-bottom: 36px; }
  .intro h1 { font-family: 'DM Serif Display', serif; font-size: 2rem; line-height: 1.2; color: var(--ink); margin-bottom: 8px; }
  .intro h1 em { color: var(--sage); font-style: italic; }
  .intro p { font-size: 0.9rem; color: var(--mist); max-width: 600px; line-height: 1.6; }
  .search-card { background: var(--white); border: 1px solid var(--line); border-radius: 8px; padding: 28px; margin-bottom: 32px; box-shadow: 0 2px 12px rgba(15,25,35,0.06); }
  .search-card h2 { font-family: 'DM Serif Display', serif; font-size: 1.1rem; margin-bottom: 20px; color: var(--ink); }
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
  .field { display: flex; flex-direction: column; gap: 6px; }
  .field label { font-family: 'DM Mono', monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--mist); }
  .field input, .field select { font-family: 'DM Sans', sans-serif; font-size: 0.9rem; padding: 10px 14px; border: 1.5px solid var(--line); border-radius: 6px; background: var(--paper); color: var(--ink); outline: none; transition: border-color 0.2s; }
  .field input:focus, .field select:focus { border-color: var(--sage); background: var(--white); }
  .sources-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px; margin-top: 6px; }
  .source-check { display: flex; align-items: center; gap: 8px; font-size: 0.82rem; cursor: pointer; padding: 6px 10px; border-radius: 4px; border: 1px solid var(--line); background: var(--paper); transition: all 0.15s; user-select: none; }
  .source-check:hover { border-color: var(--sage); background: var(--sage-light); }
  .source-check input { accent-color: var(--sage); cursor: pointer; }
  .source-check.checked { border-color: var(--sage); background: var(--sage-light); color: var(--sage); font-weight: 500; }
  .btn-search { width: 100%; padding: 14px; background: var(--sage); color: var(--white); border: none; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: background 0.2s, transform 0.1s; display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px; }
  .btn-search:hover { background: #2e5440; }
  .btn-search:active { transform: scale(0.99); }
  .btn-search:disabled { background: var(--mist); cursor: not-allowed; transform: none; }
  .loader { display: none; text-align: center; padding: 48px 24px; }
  .loader.active { display: block; }
  .loader-ring { width: 48px; height: 48px; border: 3px solid var(--line); border-top-color: var(--sage); border-radius: 50%; animation: spin 0.9s linear infinite; margin: 0 auto 16px; }
  @keyframes spin { to { transform: rotate(360deg); } }
  .loader-msg { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: var(--mist); letter-spacing: 0.06em; }
  .loader-step { font-size: 0.8rem; color: var(--mist); padding: 3px 0; opacity: 0; animation: fadeIn 0.4s forwards; }
  @keyframes fadeIn { to { opacity: 1; } }
  .results-section { display: none; }
  .results-section.active { display: block; }
  .results-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
  .results-header h2 { font-family: 'DM Serif Display', serif; font-size: 1.2rem; }
  .btn-export { padding: 8px 16px; background: var(--amber-light); color: var(--amber); border: 1.5px solid var(--amber); border-radius: 6px; font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.15s; }
  .btn-export:hover { background: var(--amber); color: white; }
  .result-card { background: var(--white); border: 1px solid var(--line); border-radius: 8px; margin-bottom: 20px; overflow: hidden; box-shadow: 0 2px 8px rgba(15,25,35,0.05); }
  .result-card-header { background: var(--ink); padding: 14px 20px; display: flex; align-items: center; justify-content: space-between; }
  .result-card-header h3 { font-family: 'DM Serif Display', serif; font-size: 1rem; color: var(--paper); }
  .status-badge { font-family: 'DM Mono', monospace; font-size: 0.65rem; padding: 4px 10px; border-radius: 20px; letter-spacing: 0.08em; text-transform: uppercase; }
  .status-em-andamento { background: #d4edda; color: #1a6630; }
  .status-parado { background: #f8d7da; color: #7a1c1c; }
  .status-previsto { background: #fff3cd; color: #7a5200; }
  .status-concluido { background: #d1ecf1; color: #0c5460; }
  .status-desconhecido { background: #e2e3e5; color: #383d41; }
  .fields-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0; }
  .field-item { padding: 14px 18px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }
  .field-label { font-family: 'DM Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--mist); margin-bottom: 4px; }
  .field-value { font-size: 0.85rem; color: var(--ink); line-height: 1.4; font-weight: 500; }
  .field-value.empty { color: var(--mist); font-style: italic; font-weight: 400; font-size: 0.8rem; }
  .field-value.found { color: var(--sage); }
  .sources-used { padding: 14px 18px; background: var(--sage-light); border-top: 1px solid var(--line); font-size: 0.78rem; color: var(--sage); }
  .sources-used strong { display: block; font-family: 'DM Mono', monospace; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
  .fontes-list { display: flex; flex-direction: column; gap: 4px; }
  .fonte-item { font-size: 0.8rem; line-height: 1.4; }
  .fonte-item a { color: var(--sage); text-decoration: underline; text-underline-offset: 2px; }
  .fonte-item a:hover { color: #2e5440; }
  .field-value.empty { color: var(--line); font-size: 0.8rem; }
  .confidence-bar { padding: 12px 18px; display: flex; align-items: center; gap: 12px; border-top: 1px solid var(--line); background: var(--paper); }
  .conf-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--mist); white-space: nowrap; }
  .bar-track { flex: 1; height: 6px; background: var(--line); border-radius: 3px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 3px; background: var(--sage); transition: width 0.8s ease; }
  .conf-pct { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: var(--sage); font-weight: 500; min-width: 36px; text-align: right; }
  .obs-block { padding: 14px 18px; border-top: 1px solid var(--line); background: var(--amber-light); }
  .obs-block .field-label { color: var(--amber); }
  .obs-block .field-value { font-size: 0.84rem; line-height: 1.6; }
  .error-msg { display: none; background: var(--red-light); border: 1px solid #e8c0c0; border-radius: 6px; padding: 14px 18px; color: var(--red); font-size: 0.85rem; margin-bottom: 20px; }
  .error-msg.active { display: block; }
  .empty-state { text-align: center; padding: 60px 24px; color: var(--mist); }
  .empty-icon { font-size: 3rem; margin-bottom: 12px; }
  .empty-state h3 { font-family: 'DM Serif Display', serif; font-size: 1.2rem; color: var(--ink); margin-bottom: 6px; }
  .empty-state p { font-size: 0.85rem; max-width: 400px; margin: 0 auto; }
  footer { margin-top: 60px; padding: 20px 32px; background: var(--ink); text-align: center; font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--mist); letter-spacing: 0.08em; text-transform: uppercase; }
  @media (max-width: 640px) { .form-grid { grid-template-columns: 1fr; } .fields-grid { grid-template-columns: 1fr 1fr; } header { flex-direction: column; gap: 8px; text-align: center; } }
</style>
</head>
<body>
<header>
  <div class="logo">SEMIL <span>·</span> Buscador de Projetos</div>
  <div class="badge">Subsecretaria de Energia e Mineração · SEM</div>
</header>
<div class="container">
  <div class="intro">
    <h1>Inteligência de <em>Projetos</em><br>de Infraestrutura</h1>
    <p>Busca automatizada em múltiplas fontes: Diário Oficial, portais de transparência, agências reguladoras, concessionárias, associações setoriais e mídia especializada. Projetos ativos entre 2023 e 2026+.</p>
  </div>
  <div class="search-card">
    <h2>Dados da Busca</h2>
    <div class="form-grid">
      <div class="field">
        <label>Nome do Projeto / Empreendimento *</label>
        <input type="text" id="projeto" placeholder="Ex: Alto Alegre, Gasoduto Paulínia-Guararema…" />
      </div>
      <div class="field">
        <label>Município (opcional)</label>
        <input type="text" id="municipio" placeholder="Ex: Araçatuba, São Paulo…" />
      </div>
    </div>
    <div class="form-grid">
      <div class="field">
        <label>Tipo de Projeto (opcional)</label>
        <select id="tipo">
          <option value="">— Todos —</option>
          <option value="biometano">Biometano / Biogás</option>
          <option value="gas natural">Gás Natural</option>
          <option value="petroleo">Petróleo</option>
          <option value="biocombustivel">Biocombustível</option>
          <option value="energia renovavel">Energia Renovável</option>
          <option value="infraestrutura logistica">Infraestrutura Logística</option>
          <option value="saneamento">Saneamento</option>
          <option value="outro">Outro</option>
        </select>
      </div>
      <div class="field">
        <label>Contexto adicional (opcional)</label>
        <input type="text" id="contexto" placeholder="Ex: concessão, licitação, ANP, ARSESP…" />
      </div>
    </div>
    <div class="field">
      <label>Fontes de Busca Prioritárias</label>
      <div class="sources-grid" id="sourcesGrid"></div>
    </div>
    <div id="errorMsg" class="error-msg"></div>
    <button class="btn-search" id="btnSearch" onclick="runSearch()">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      Buscar Informações do Projeto
    </button>
  </div>
  <div class="loader" id="loader">
    <div class="loader-ring"></div>
    <div class="loader-msg">CONSULTANDO FONTES</div>
    <div class="loader-steps" id="loaderSteps"></div>
  </div>
  <div class="results-section" id="resultsSection">
    <div class="results-header">
      <h2 id="resultsTitle">Resultados</h2>
      <button class="btn-export" onclick="exportCSV()">↓ Exportar CSV</button>
    </div>
    <div id="resultsContainer"></div>
  </div>
  <div class="empty-state" id="emptyState">
    <div class="empty-icon">🔍</div>
    <h3>Pronto para buscar</h3>
    <p>Preencha o nome do projeto acima e selecione as fontes desejadas.</p>
  </div>
</div>
<footer>SEMIL · Subsecretaria de Energia e Mineração · Ferramenta de Inteligência de Projetos</footer>
<script>
const SOURCES = [
  { id: 'google', label: 'Google / Mídia geral', default: true },
  { id: 'doe', label: 'Diário Oficial SP', default: true },
  { id: 'transparencia', label: 'Portal Transparência / SIAFEM', default: true },
  { id: 'prefeituras', label: 'Sites de prefeituras', default: true },
  { id: 'licitacoes', label: 'BEC / ComprasNet', default: true },
  { id: 'regulacao', label: 'ANP / ARSESP / CETESB', default: true },
  { id: 'concessionarias', label: 'Comgás / Naturgy / NECTA', default: true },
  { id: 'associacoes', label: 'Abiogás / IBP / Associações', default: true },
  { id: 'noticias', label: 'Portais de notícias setoriais', default: true },
];
const grid = document.getElementById('sourcesGrid');
SOURCES.forEach(s => {
  const label = document.createElement('label');
  label.className = 'source-check' + (s.default ? ' checked' : '');
  label.innerHTML = `<input type="checkbox" value="${s.id}" ${s.default ? 'checked' : ''} onchange="toggleCheck(this)"> ${s.label}`;
  grid.appendChild(label);
});
function toggleCheck(el) { el.parentElement.classList.toggle('checked', el.checked); }
function getSelectedSources() { return Array.from(document.querySelectorAll('#sourcesGrid input:checked')).map(el => el.value); }

let lastResult = null;

async function runSearch() {
  const projeto = document.getElementById('projeto').value.trim();
  const municipio = document.getElementById('municipio').value.trim();
  const tipo = document.getElementById('tipo').value;
  const contexto = document.getElementById('contexto').value.trim();
  const fontes = getSelectedSources();
  const errEl = document.getElementById('errorMsg');
  errEl.classList.remove('active');
  if (!projeto) { errEl.textContent = 'Por favor, informe o nome do projeto.'; errEl.classList.add('active'); return; }
  if (fontes.length === 0) { errEl.textContent = 'Selecione ao menos uma fonte.'; errEl.classList.add('active'); return; }

  document.getElementById('btnSearch').disabled = true;
  document.getElementById('loader').classList.add('active');
  document.getElementById('resultsSection').classList.remove('active');
  document.getElementById('emptyState').style.display = 'none';

  const steps = ['Formulando estratégia de busca...','Consultando Diário Oficial e portais regulatórios...','Buscando em portais de transparência...','Verificando sites setoriais e associações...','Consolidando e estruturando dados...'];
  const stepsEl = document.getElementById('loaderSteps');
  stepsEl.innerHTML = '';
  let si = 0;
  const stepInterval = setInterval(() => {
    if (si < steps.length) {
      const d = document.createElement('div');
      d.className = 'loader-step';
      d.textContent = '· ' + steps[si];
      stepsEl.appendChild(d);
      si++;
    }
  }, 2200);

  try {
    const response = await fetch('/buscar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projeto, municipio, tipo, contexto, fontes })
    });
    clearInterval(stepInterval);
    const result = await response.json();
    if (result.error) { throw new Error(result.error); }
    lastResult = result;
    renderResult(result);
  } catch(err) {
    clearInterval(stepInterval);
    errEl.textContent = 'Erro na busca: ' + err.message;
    errEl.classList.add('active');
    document.getElementById('emptyState').style.display = 'block';
  }
  document.getElementById('loader').classList.remove('active');
  document.getElementById('btnSearch').disabled = false;
}

function getStatusClass(s) {
  if (!s) return 'status-desconhecido';
  const l = s.toLowerCase();
  if (l.includes('andamento')) return 'status-em-andamento';
  if (l.includes('parado') || l.includes('suspenso')) return 'status-parado';
  if (l.includes('previsto') || l.includes('planejado')) return 'status-previsto';
  if (l.includes('conclu')) return 'status-concluido';
  return 'status-desconhecido';
}
function fv(val, cls='') {
  if (!val || val === '' || val === 'Nao localizado' || val === 'Não localizado' || val === 'vazio' || val === 'N/A') {
    return `<div class="field-value empty">—</div>`;
  }
  return `<div class="field-value ${cls}">${val}</div>`;
}

function renderFontes(fontes) {
  if (!fontes || fontes.length === 0) return '<span style="color:var(--mist)">Nenhuma fonte registrada</span>';
  if (typeof fontes[0] === 'string') {
    return fontes.map(f => `<span>${f}</span>`).join(' · ');
  }
  return fontes.map(f => {
    const url = f.url || '';
    const titulo = f.titulo || url;
    const desc = f.descricao ? ` — ${f.descricao}` : '';
    if (url) {
      return `<div class="fonte-item"><a href="${url}" target="_blank" rel="noopener">↗ ${titulo}</a>${desc}</div>`;
    }
    return `<div class="fonte-item"><strong>${titulo}</strong>${desc}</div>`;
  }).join('');
}
function renderResult(r) {
  const container = document.getElementById('resultsContainer');
  const conf = r.confianca_percentual || 0;
  const fontesHtml = renderFontes(r.fontes || r.fontes_encontradas);
  container.innerHTML = `
    <div class="result-card">
      <div class="result-card-header">
        <h3>${r.projeto || 'Projeto'}</h3>
        <span class="status-badge ${getStatusClass(r.situacao)}">${r.situacao || 'Desconhecido'}</span>
      </div>
      <div class="fields-grid">
        <div class="field-item"><div class="field-label">Município</div>${fv(r.municipio,'found')}</div>
        <div class="field-item"><div class="field-label">Região Administrativa</div>${fv(r.regiao_administrativa)}</div>
        <div class="field-item"><div class="field-label">Região Metropolitana</div>${fv(r.regiao_metropolitana)}</div>
        <div class="field-item"><div class="field-label">Tipo</div>${fv(r.tipo)}</div>
        <div class="field-item"><div class="field-label">Investimento Estado (R$)</div>${fv(r.investimento_estado_reais)}</div>
        <div class="field-item"><div class="field-label">Investimento Outros (R$)</div>${fv(r.investimento_outros_reais)}</div>
        <div class="field-item"><div class="field-label">População Impactada</div>${fv(r.populacao_impactada)}</div>
        <div class="field-item"><div class="field-label">Benefícios à População</div>${fv(r.beneficios_populacao)}</div>
        <div class="field-item"><div class="field-label">Início</div>${fv(r.data_inicio)}</div>
        <div class="field-item"><div class="field-label">Término Previsto</div>${fv(r.data_termino_previsto)}</div>
        <div class="field-item"><div class="field-label">Campo Funcional SEMIL</div>${fv(r.campo_funcional_semil)}</div>
        <div class="field-item"><div class="field-label">Produto PPA 2024–2027</div>${fv(r.produto_ppa)}</div>
        <div class="field-item"><div class="field-label">Política / Plano</div>${fv(r.politica_plano)}</div>
      </div>
      ${r.observacoes ? `<div class="obs-block"><div class="field-label">Observações e Fontes</div><div class="field-value">${r.observacoes}</div></div>` : ''}
      <div class="confidence-bar">
        <span class="conf-label">Confiança dos Dados</span>
        <div class="bar-track"><div class="bar-fill" style="width:${conf}%"></div></div>
        <span class="conf-pct">${conf}%</span>
      </div>
      <div class="sources-used"><strong>Fontes consultadas:</strong><div class="fontes-list">${fontesHtml}</div></div>
    </div>`;
  document.getElementById('resultsSection').classList.add('active');
  document.getElementById('resultsTitle').textContent = `Resultado · ${r.projeto || 'Projeto'}`;
  container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function exportCSV() {
  if (!lastResult) return;
  const r = lastResult;
  const headers = ['Projeto','Município','Região Administrativa','Região Metropolitana','Tipo','Investimento Estado (R$)','Investimento Outros (R$)','População Impactada','Benefícios','Situação','Início','Término','Campo Funcional SEMIL','Produto PPA','Política/Plano','Observações','Confiança (%)'];
  const values = [r.projeto,r.municipio,r.regiao_administrativa,r.regiao_metropolitana,r.tipo,r.investimento_estado_reais,r.investimento_outros_reais,r.populacao_impactada,r.beneficios_populacao,r.situacao,r.data_inicio,r.data_termino_previsto,r.campo_funcional_semil,r.produto_ppa,r.politica_plano,r.observacoes,r.confianca_percentual].map(v=>`"${String(v||'').replace(/"/g,'""')}"`);
  const csv = headers.join(';')+'\n'+values.join(';');
  const blob = new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8;'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href=url; a.download=`SEMIL_${(r.projeto||'projeto').replace(/\s+/g,'_')}_${new Date().toISOString().slice(0,10)}.csv`;
  a.click(); URL.revokeObjectURL(url);
}
document.getElementById('projeto').addEventListener('keydown', e => { if(e.key==='Enter') runSearch(); });
</script>
</body>
</html>
