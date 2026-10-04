# -*- coding: utf-8 -*-
"""(c) Página de revisão — `roteiro_estudo.md` 2.1(c), 2.4 e Fase 3.

Serve, só nesta máquina, uma página com os achados unificados pela IA: enunciado, uma leitura por
heurística (redação dos achados daquela heurística, com os cinco campos de um achado), as capturas dos
achados reunidos, os textos originais recolhidos e, para o pesquisador decidir, dois botões
(defeito ou falso positivo), a severidade 1 a 4 quando defeito e uma observação opcional. Cada
decisão grava `decisoes.json` na pasta cega, na hora. Nada sai da máquina.

Uso:
    py analise/revisar.py --pasta <pasta cega> [--porta 8765] [--sem-abrir]

A página não mostra id, formato, execução, severidade da IA nem a justificativa dessa severidade: o
cegamento do `analise.md` §2 vale até a reatação. As heurísticas aparecem no cabeçalho do cartão e como título de cada leitura. Recusa rodar se `mapa_chaves.json` estiver na pasta.
"""
import argparse
import html
import json
import os
import sys
import threading
import webbrowser
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import falhar, ler_json

PAGINA = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Revisão dos achados unificados</title>
<style>
:root{--bg:#f6f4ef;--card:#fff;--ink:#1f2a2e;--ink2:#4f5b60;--ink3:#7d888c;--line:#d9d4c8;--ok:#0F6E56;--ok-bg:#E1F5EE;--no:#993C1D;--no-bg:#FAECE7;--sel:#534AB7;--sel-bg:#EEEDFE}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,Segoe UI,Arial,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px 60px}
header{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:14px 0 10px;z-index:5}
h1{font-size:20px;margin:0 0 4px}.sub{color:var(--ink2);font-size:13px;display:flex;gap:18px;flex-wrap:wrap;align-items:center}
.bar{height:6px;background:var(--line);border-radius:3px;overflow:hidden;margin-top:8px}.bar i{display:block;height:100%;background:var(--ok);width:0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-top:14px}
.card.defeito{border-left:5px solid var(--ok)}.card.falso_positivo{border-left:5px solid var(--no)}.card.pendente{border-left:5px solid var(--line)}
.cab{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}.uid{font:600 13px ui-monospace,monospace;color:var(--ink3)}
.enun{font-size:16px;font-weight:600;margin:4px 0}.meta{color:var(--ink2);font-size:13px}.meta b{color:var(--ink)}
.dec{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:12px;padding-top:10px;border-top:1px dashed var(--line)}
button{font:500 14px system-ui,sans-serif;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:6px;padding:7px 14px;cursor:pointer}
button.on-def{background:var(--ok);border-color:var(--ok);color:#fff}button.on-fp{background:var(--no);border-color:var(--no);color:#fff}
.sev{display:none;gap:6px;align-items:center;margin-left:8px}.sev.show{display:inline-flex}.sev button{min-width:38px}.sev button.on{background:var(--sel);border-color:var(--sel);color:#fff}
.sev .lbl{font-size:13px;color:var(--ink2)}
textarea{width:100%;min-height:44px;margin-top:8px;font:14px system-ui,sans-serif;border:1px solid var(--line);border-radius:6px;padding:6px 8px;resize:vertical}
details{margin-top:10px}summary{cursor:pointer;color:var(--sel);font-size:14px}
.ach{border-top:1px solid var(--line);padding:10px 0}.ach p{margin:4px 0;font-size:14px}.red p{margin:8px 0;font-size:15px}.leit{border-top:1px solid var(--line);padding:8px 0 4px}.leit-t{font-size:13px;font-weight:600;color:var(--sel);text-transform:none;margin-bottom:2px}.k{color:var(--ink3);font-size:12px;text-transform:uppercase;letter-spacing:.05em}
.thumbs{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}.thumbs a img{max-height:130px;max-width:220px;border:1px solid var(--line);border-radius:4px;background:#fff}
.thumbs a.txt{font-size:12px;align-self:center;color:var(--sel)}
.salvo{font-size:12px;color:var(--ink3)}.salvo.err{color:var(--no);font-weight:600}
label.f{font-size:13px;display:inline-flex;gap:6px;align-items:center;cursor:pointer}
.legenda{font-size:12px;color:var(--ink3)}
</style></head><body><div class="wrap">
<header>
<h1>Revisão dos achados unificados</h1>
<div class="sub"><span id="prog"></span><label class="f"><input type="checkbox" id="so-pend"> só pendentes</label><span class="salvo" id="salvo"></span></div>
<div class="bar"><i id="barra"></i></div>
<div class="legenda">Cada cartão é um achado unificado: enunciado, elemento e pontos de manifestação à vista; as leituras (uma por heurística, no tamanho de um achado) e as capturas ficam recolhidas, assim como os achados originais. Decida: <b>Defeito</b> ou <b>Falso positivo</b> (o problema não se verifica no objeto); se defeito, a severidade de 1 a 4 (cosmético, menor, maior, catastrófico). Observação é opcional. Clique nas imagens para abrir a captura inteira; os textos originais ficam recolhidos ao fim do cartão.</div>
</header>
<div id="lista"></div>
</div>
<script id="dados" type="application/json">__DADOS__</script>
<script>
const D = JSON.parse(document.getElementById('dados').textContent);
let estado = {achados_unificados:{}, atualizado:null};
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const SEVS = {1:'1 cosmético',2:'2 menor',3:'3 maior',4:'4 catastrófico'};

function decisao(uid){ return estado.achados_unificados[uid] || {}; }
function classe(uid){ const d = decisao(uid); return d.classificacao || 'pendente'; }

function cardHTML(u){
  const d = decisao(u.unificado), cls = classe(u.unificado);
  const achados = u.achados.map(k => D.achados[k]).filter(Boolean);
  const L = u.leituras || [];
  const arquivos = achados.flatMap(a => a.arquivos || []);
  const campo = (rot, txt) => `<p><span class="k">${rot}</span><br>${esc(txt)}</p>`;
  const heur = L.length ? L.map(l => l.heuristica) : [...new Set(achados.map(a => (a.heuristica||'').split(' ')[0]).filter(Boolean))];
  const thumbs = `<div class="thumbs">${arquivos.map(f => f.toLowerCase().endsWith('.png') || f.toLowerCase().endsWith('.jpg')
      ? `<a href="evidencias_cegas/${encodeURIComponent(f)}" target="_blank" title="${esc(f)}"><img loading="lazy" src="evidencias_cegas/${encodeURIComponent(f)}" alt="${esc(f)}"></a>`
      : `<a class="txt" href="evidencias_cegas/${encodeURIComponent(f)}" target="_blank">${esc(f)}</a>`).join('')}</div>`;
  const leiturasHTML = L.length ? L.map((l, i) => `<div class="leit"><div class="leit-t">Leitura ${i+1} de ${L.length} · ${esc(l.nome_heuristica || l.heuristica)} · ${l.achados.length} achado${l.achados.length>1?'s':''}</div>
        ${campo('Localização', l.localizacao)}${campo('Descrição da falha', l.descricao_falha)}${campo('Justificativa da violação', l.justificativa_violacao)}${campo('Registro visual', l.registro_visual)}${campo('Sugestão de correção', l.sugestao_correcao)}</div>`).join('')
    : `<p class="meta"><b>Sem leituras</b> para este achado unificado; leia os achados originais.</p>`;
  return `<article class="card ${cls}" data-uid="${u.unificado}">
    <div class="cab"><span class="uid">${u.unificado}</span><span class="meta">${achados.length} achado${achados.length>1?'s':''}${heur.length ? ' · heurísticas: <b>' + esc(heur.join(', ')) + '</b>' : ''}</span></div>
    <div class="enun">${esc(u.enunciado)}</div>
    <div class="meta"><b>Elemento:</b> ${esc(u.elemento)}</div>
    ${u.pontos_manifestacao && u.pontos_manifestacao.length ? `<div class="meta"><b>Pontos de manifestação:</b> ${esc(u.pontos_manifestacao.join(' · '))}</div>` : ''}
    <details><summary>Ver ${L.length>1 ? 'as ' + L.length + ' leituras' : 'a leitura'} e as capturas</summary>
      ${thumbs}<div class="red">${leiturasHTML}</div>
    </details>
    <details><summary>Ver os ${achados.length} achado${achados.length>1?'s':''} ${achados.length>1?'originais':'original'}</summary>
      ${achados.map(a => `<div class="ach">
        <p><span class="k">Localização</span><br>${esc(a.localizacao)}</p>
        <p><span class="k">Descrição da falha</span><br>${esc(a.descricao_falha)}</p>
        <p><span class="k">Justificativa da violação</span><br>${esc(a.justificativa_violacao)}</p>
        <p><span class="k">Registro visual</span><br>${esc(a.registro_visual_cego || a.registro_visual)}</p>
        <p><span class="k">Sugestão de correção</span><br>${esc(a.sugestao_correcao)}</p>
      </div>`).join('')}
    </details>
    <div class="dec">
      <button data-acao="defeito" class="${cls==='defeito'?'on-def':''}">Defeito</button>
      <button data-acao="falso_positivo" class="${cls==='falso_positivo'?'on-fp':''}">Falso positivo</button>
      <span class="sev ${cls==='defeito'?'show':''}"><span class="lbl">Severidade:</span>${[1,2,3,4].map(n=>`<button data-sev="${n}" class="${d.severidade===n?'on':''}" title="${SEVS[n]}">${n}</button>`).join('')}</span>
      ${cls!=='pendente' ? '<button data-acao="limpar" title="voltar a pendente">Limpar</button>' : ''}
      <span class="salvo">${d.quando ? 'decidido em ' + new Date(d.quando).toLocaleString('pt-BR') : ''}</span>
    </div>
    <textarea data-obs placeholder="Observação (opcional)">${esc(d.observacao || '')}</textarea>
  </article>`;
}

function render(){
  const soPend = document.getElementById('so-pend').checked;
  const lista = document.getElementById('lista');
  lista.innerHTML = D.unificados.filter(u => !soPend || classe(u.unificado)==='pendente').map(cardHTML).join('') || '<p class="meta" style="margin-top:20px">Nada pendente.</p>';
  progresso();
}
function rerenderCard(uid){
  const antigo = document.querySelector(`.card[data-uid="${uid}"]`);
  if(!antigo) return;
  const u = D.unificados.find(x => x.unificado===uid);
  const abertos = [...antigo.querySelectorAll('details')].map(x => x.open);
  const tmp = document.createElement('div'); tmp.innerHTML = cardHTML(u);
  const novo = tmp.firstElementChild; [...novo.querySelectorAll('details')].forEach((x, i) => { x.open = !!abertos[i]; });
  antigo.replaceWith(novo); progresso();
}
function progresso(){
  const total = D.unificados.length;
  const dec = D.unificados.filter(u => classe(u.unificado)!=='pendente').length;
  const def = D.unificados.filter(u => classe(u.unificado)==='defeito').length;
  const semSev = D.unificados.filter(u => classe(u.unificado)==='defeito' && !decisao(u.unificado).severidade).length;
  document.getElementById('prog').textContent = `${dec} de ${total} decididos · ${def} defeitos · ${dec-def} falsos positivos` + (semSev ? ` · ${semSev} defeito(s) sem severidade` : '');
  document.getElementById('barra').style.width = (100*dec/total) + '%';
}
let gravando = null;
async function gravar(){
  estado.atualizado = new Date().toISOString();
  const el = document.getElementById('salvo');
  try{
    const r = await fetch('/decisoes', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(estado)});
    if(!r.ok) throw new Error(r.status);
    el.className='salvo'; el.textContent = 'gravado em decisoes.json às ' + new Date().toLocaleTimeString('pt-BR');
  }catch(e){ el.className='salvo err'; el.textContent = 'NÃO GRAVOU: ' + e + ' (o servidor está rodando?)'; }
}
function marcar(uid, patch){
  const d = Object.assign({classificacao:null, severidade:null, observacao:''}, decisao(uid), patch);
  if(d.classificacao !== 'defeito') d.severidade = null;
  if(patch.classificacao !== undefined || patch.severidade !== undefined) d.quando = new Date().toISOString();
  if(!d.classificacao){ delete estado.achados_unificados[uid]; } else { estado.achados_unificados[uid] = d; }
  gravar();
}
document.addEventListener('click', ev => {
  const card = ev.target.closest('.card'); if(!card) return;
  const uid = card.dataset.uid;
  const b = ev.target.closest('button'); if(!b) return;
  if(b.dataset.acao==='defeito' || b.dataset.acao==='falso_positivo'){ marcar(uid, {classificacao:b.dataset.acao}); rerenderCard(uid); }
  else if(b.dataset.acao==='limpar'){ marcar(uid, {classificacao:null}); rerenderCard(uid); }
  else if(b.dataset.sev){ marcar(uid, {severidade: parseInt(b.dataset.sev,10)}); rerenderCard(uid); }
});
document.addEventListener('input', ev => {
  const ta = ev.target.closest('textarea[data-obs]'); if(!ta) return;
  const uid = ta.closest('.card').dataset.uid;
  clearTimeout(gravando);
  gravando = setTimeout(() => {
    const d = decisao(uid);
    if(!d.classificacao && !ta.value.trim()) return;
    estado.achados_unificados[uid] = Object.assign({classificacao:null, severidade:null}, d, {observacao: ta.value});
    gravar();
  }, 500);
});
document.getElementById('so-pend').addEventListener('change', render);
fetch('/decisoes.json').then(r => r.ok ? r.json() : {}).then(j => { if(j && j.achados_unificados) estado = j; render(); }).catch(render);
</script></body></html>
"""


def montar_dados(pasta, permitir_sem_redacao=False):
    cegos = {a["chave"]: a for a in ler_json(pasta / "achados_cegos.json")}
    evid = ler_json(pasta / "achados_cegos_evidencias.json") if (pasta / "achados_cegos_evidencias.json").exists() else {}
    unif = ler_json(pasta / "unificacao_ia.json")["achados_unificados"]
    achados = {}
    for k, a in cegos.items():
        e = evid.get(k, {})
        achados[k] = {"heuristica": a.get("heuristica"), "localizacao": a.get("localizacao"),
                      "registro_visual": a.get("registro_visual"), "registro_visual_cego": e.get("registro_visual_cego"),
                      "descricao_falha": a.get("descricao_falha"), "justificativa_violacao": a.get("justificativa_violacao"),
                      "sugestao_correcao": a.get("sugestao_correcao"), "arquivos": e.get("arquivos", [])}
        # sem severidade, severidade_rotulo e justificativa_severidade: nada além do problema orienta a decisão
    unificados = sorted(unif, key=lambda u: u["unificado"])
    sem_redacao = [u["unificado"] for u in unificados if not u.get("leituras")]
    if sem_redacao and not permitir_sem_redacao:
        falhar(f"{len(sem_redacao)} achado(s) unificado(s) sem leituras (rode a redação em lotes ou use --sem-redacao): {', '.join(sem_redacao[:8])}")
    # o cartão leva enunciado, elemento, pontos de manifestação, leituras e capturas; a justificativa da fusão fica só no JSON
    return {"unificados": [{"unificado": u["unificado"], "enunciado": u["enunciado"], "achados": u["achados"], "elemento": u.get("elemento", ""), "pontos_manifestacao": u.get("pontos_manifestacao", []), "leituras": u.get("leituras") or []} for u in unificados],
            "achados": achados}


def gravar_atomico(caminho, texto):
    tmp = caminho.with_suffix(".tmp")
    tmp.write_text(texto, encoding="utf-8")
    os.replace(tmp, caminho)


def fazer_handler(pasta, pagina):
    decisoes = pasta / "decisoes.json"

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(pasta), **kw)

        def log_message(self, fmt, *args):  # silencia o log de cada imagem
            pass

        def _responder(self, corpo, tipo="application/json; charset=utf-8", status=200):
            dados = corpo.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(dados)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(dados)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                return self._responder(pagina, "text/html; charset=utf-8")
            if self.path == "/decisoes.json":
                if decisoes.exists():
                    return self._responder(decisoes.read_text(encoding="utf-8"))
                return self._responder('{"achados_unificados":{},"atualizado":null}')
            if self.path.startswith("/evidencias_cegas/"):
                return super().do_GET()
            return self._responder("não encontrado", "text/plain; charset=utf-8", 404)

        def do_POST(self):
            if self.path != "/decisoes":
                return self._responder("não encontrado", "text/plain; charset=utf-8", 404)
            n = int(self.headers.get("Content-Length", 0))
            bruto = self.rfile.read(n).decode("utf-8")
            try:
                obj = json.loads(bruto)
                assert isinstance(obj.get("achados_unificados"), dict)
            except Exception as e:  # noqa: BLE001
                return self._responder(f"JSON inválido: {e}", "text/plain; charset=utf-8", 400)
            obj["atualizado"] = datetime.now().isoformat(timespec="seconds")
            gravar_atomico(decisoes, json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
            return self._responder('{"ok":true}')

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pasta", required=True)
    ap.add_argument("--porta", type=int, default=8765)
    ap.add_argument("--sem-abrir", action="store_true", help="não abre o navegador")
    ap.add_argument("--sem-redacao", action="store_true", help="aceita achados unificados ainda sem redação unificada (mostra os originais)")
    args = ap.parse_args()
    pasta = Path(args.pasta).resolve()
    for nome in ("achados_cegos.json", "unificacao_ia.json"):
        if not (pasta / nome).exists():
            falhar(f"{pasta / nome} não existe")
    if (pasta / "mapa_chaves.json").exists():
        falhar("mapa_chaves.json está dentro da pasta cega: o cegamento foi quebrado; mova-o para a pasta fechada")

    dados = montar_dados(pasta, args.sem_redacao)
    pagina = PAGINA.replace("__DADOS__", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
    servidor = ThreadingHTTPServer(("127.0.0.1", args.porta), fazer_handler(pasta, pagina))
    url = f"http://127.0.0.1:{args.porta}/"
    print(f"Página de revisão em {url}\n{len(dados['unificados'])} achados unificados · {len(dados['achados'])} achados · "
          f"decisões em {pasta / 'decisoes.json'}\nCtrl+C encerra.")
    if not args.sem_abrir:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado. As decisões estão gravadas em decisoes.json.")


if __name__ == "__main__":
    main()
