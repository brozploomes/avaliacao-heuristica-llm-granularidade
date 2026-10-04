# -*- coding: utf-8 -*-
"""(b) Unificação cega por IA e redação unificada: monta os prompts e valida as saídas.
`roteiro_estudo.md` 2.1(b) e 2.3; `protocolo/unificacao.md`.

Os textos dos prompts são os de `protocolo/unificacao.md` ("## Texto do prompt" e "### Texto do prompt
da redação"), extraídos em tempo de execução para que não exista uma segunda cópia a divergir. As chamadas
do modelo são feitas pela skill `/unificar` (na conversa de revisão, raiz do MBA).

Uso:
    py analise/unificar_prompt.py montar           --pasta <pasta cega>            # grava prompt_unificacao.md
    py analise/unificar_prompt.py validar          --pasta <pasta cega>            # lê unificacao_ia_bruto.md, grava unificacao_ia.json
    py analise/unificar_prompt.py montar-redacao   --pasta <pasta cega> [--lote 8] # grava redacao_lote_NN.md, um por lote (leituras por heurística)
    py analise/unificar_prompt.py validar-redacao  --pasta <pasta cega>            # lê redacao_lote_NN_bruto.md, grava as leituras em unificacao_ia.json

Conferências (roteiro 2.3): a saída parseia; todo K### em exatamente um achado unificado; nenhum campo
obrigatório vazio; toda leitura (achado unificado × heurística) com os cinco campos e tamanho de achado. Falha (código 1) se alguma reprovar; nada é corrigido
à mão.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import RAIZ_INSTRUMENTO, RE_UNIFICADO, codigo_heuristica, falhar, gravar_json, ler_json

PROTOCOLO = RAIZ_INSTRUMENTO / "protocolo" / "unificacao.md"
CAMPOS_REDACAO = ["localizacao", "descricao_falha", "justificativa_violacao", "registro_visual", "sugestao_correcao"]
CAMPOS_ORIGINAIS = ["localizacao", "registro_visual", "descricao_falha", "justificativa_violacao", "sugestao_correcao"]
# campos que vão ao prompt da unificação: os que definem a identidade do problema
# (`protocolo/unificacao.md`, "Preparação da entrada", item 4). Heurística e severidade ficam fora
# porque o próprio protocolo as declara fora dos critérios de fusão; registro_visual e
# justificativa_violacao, porque a coleta real não caberia no contexto do modelo com eles — ensaio de
# 24/09/2026 sobre 100 achados: concordância 0,999 e 44 de 48 grupos idênticos ao conjunto completo.
CAMPOS_UNIFICACAO = ["chave", "localizacao", "descricao_falha", "sugestao_correcao"]


def secao_prompt(titulo):
    """Devolve o texto em blockquote da seção `titulo` (## ou ###) do protocolo."""
    linhas = PROTOCOLO.read_text(encoding="utf-8").splitlines()
    dentro, saida = False, []
    for ln in linhas:
        if re.match(r"^#{2,3} ", ln):
            if dentro:
                break
            dentro = ln.strip().lstrip("#").strip() == titulo
            continue
        if dentro:
            saida.append(re.sub(r"^> ?", "", ln))
    texto = "\n".join(saida).strip()
    if not texto:
        falhar(f"não achei a seção '{titulo}' em {PROTOCOLO}")
    return texto


def extrair_json(texto):
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", texto, re.S)
    bruto = m.group(1) if m else texto[texto.find("{"): texto.rfind("}") + 1]
    if not bruto.strip():
        falhar("não há objeto JSON na saída bruta")
    try:
        return json.loads(bruto)
    except json.JSONDecodeError as e:
        falhar(f"a saída bruta não parseia como JSON: {e}")


# ----------------------------------------------------------------------------- unificação
def montar(pasta, _args):
    cegos = ler_json(pasta / "achados_cegos.json")
    corpo = "[\n" + ",\n".join(json.dumps({c: a[c] for c in CAMPOS_UNIFICACAO if c in a}, ensure_ascii=False)
                               for a in cegos) + "\n]"
    prompt = (secao_prompt("Texto do prompt")
              + f"\n\n---\n\nSão {len(cegos)} achados. Responda **somente** com o JSON pedido, sem texto antes ou depois, "
              "sem cercas de código. Não use ferramenta alguma: tudo de que você precisa está abaixo.\n\n"
              "## Achados\n\n" + corpo + "\n")
    destino = pasta / "prompt_unificacao.md"
    destino.write_text(prompt, encoding="utf-8")
    print(f"Prompt gravado em {destino}\nAchados: {len(cegos)} · caracteres: {len(prompt)} · tokens (estimativa ~chars/3): {len(prompt) // 3}")


def validar(pasta, _args):
    cegos = ler_json(pasta / "achados_cegos.json")
    chaves = [a["chave"] for a in cegos]
    conjunto = set(chaves)
    saida = extrair_json((pasta / "unificacao_ia_bruto.md").read_text(encoding="utf-8"))

    erros, avisos = [], []
    lista = saida.get("achados_unificados")
    if lista is None and isinstance(saida.get("grupos"), list):
        avisos.append("a saída usa a chave antiga `grupos`; lida como `achados_unificados`")
        lista = saida["grupos"]
    if not isinstance(lista, list) or not lista:
        erros.append("`achados_unificados` ausente ou vazio")
        lista = []
    if "pares_limitrofes" in saida:
        avisos.append("a saída trouxe `pares_limitrofes`, que o protocolo não pede; ignorados")

    ocorrencias, ids, normalizados = Counter(), Counter(), []
    for n, u in enumerate(lista, 1):
        uid = str(u.get("unificado") or u.get("grupo") or "").strip()
        if not RE_UNIFICADO.match(uid):
            avisos.append(f"achado unificado {n}: identificador {uid!r} fora do padrão U###; renumerado")
            uid = f"U{n:03d}"
        ids[uid] += 1
        ach = u.get("achados")
        if not isinstance(ach, list) or not ach:
            erros.append(f"{uid}: `achados` ausente ou vazio")
            ach = []
        ach = [str(k).strip() for k in ach]
        for k in ach:
            ocorrencias[k] += 1
            if k not in conjunto:
                erros.append(f"{uid}: chave desconhecida {k}")
        for campo in ("enunciado", "elemento", "justificativa"):
            if not str(u.get(campo, "")).strip():
                erros.append(f"{uid}: campo `{campo}` vazio")
        pontos = u.get("pontos_manifestacao")
        if isinstance(pontos, str):
            pontos = [p.strip() for p in pontos.split("|") if p.strip()]
        if not isinstance(pontos, list):
            pontos = []
        if not pontos:
            avisos.append(f"{uid}: `pontos_manifestacao` vazio")
        normalizados.append({"unificado": uid, "achados": sorted(ach), "enunciado": str(u.get("enunciado", "")).strip(),
                             "elemento": str(u.get("elemento", "")).strip(), "pontos_manifestacao": [str(p) for p in pontos],
                             "justificativa": str(u.get("justificativa", "")).strip()})
    for uid, c in ids.items():
        if c > 1:
            erros.append(f"identificador repetido: {uid} ({c} vezes)")
    faltam = [k for k in chaves if ocorrencias[k] == 0]
    repetidas = [k for k, c in ocorrencias.items() if c > 1 and k in conjunto]
    if faltam:
        erros.append(f"{len(faltam)} chave(s) em nenhum achado unificado: {', '.join(faltam)}")
    if repetidas:
        erros.append(f"{len(repetidas)} chave(s) em mais de um achado unificado: {', '.join(sorted(repetidas))}")

    tamanhos = Counter(len(u["achados"]) for u in normalizados)
    resumo = ["# Conferência da unificação por IA", "",
              f"- Achados cegos: {len(chaves)} · achados unificados: {len(normalizados)}",
              f"- Achados unificados de um só achado: {tamanhos.get(1, 0)} · maior: {max(tamanhos) if tamanhos else 0} achados",
              f"- Erros: {len(erros)} · avisos: {len(avisos)}", ""]
    if erros:
        resumo += ["## Erros (a saída não é aceita)", ""] + [f"- {e}" for e in erros] + [""]
    if avisos:
        resumo += ["## Avisos", ""] + [f"- {a}" for a in avisos] + [""]
    (pasta / "unificacao_conferencia.md").write_text("\n".join(resumo) + "\n", encoding="utf-8")
    print("\n".join(resumo))
    if erros:
        sys.exit(1)
    # preserva leituras já gravadas, se o arquivo existir
    anteriores = {}
    if (pasta / "unificacao_ia.json").exists():
        anteriores = {u["unificado"]: u.get("leituras") for u in ler_json(pasta / "unificacao_ia.json")["achados_unificados"]}
    for u in normalizados:
        if anteriores.get(u["unificado"]):
            u["leituras"] = anteriores[u["unificado"]]
    gravar_json(pasta / "unificacao_ia.json", {"achados_unificados": normalizados})
    print(f"Gravado {pasta / 'unificacao_ia.json'}")


# ----------------------------------------------------------------------------- redação unificada (leituras)
def _leituras_de(u, cegos):
    """Pares (heurística, [chaves]) de um achado unificado, na ordem H1..H10, pelo campo do avaliador."""
    from collections import defaultdict
    por_h = defaultdict(list)
    for k in u["achados"]:
        if k in cegos:
            por_h[codigo_heuristica(cegos[k]["heuristica"])].append(k)
    return sorted(por_h.items(), key=lambda kv: int(kv[0][1:]))


def montar_redacao(pasta, args):
    cegos = {a["chave"]: a for a in ler_json(pasta / "achados_cegos.json")}
    unif = sorted(ler_json(pasta / "unificacao_ia.json")["achados_unificados"], key=lambda u: u["unificado"])
    if args.so_faltantes:
        unif = [u for u in unif if len(u.get("leituras") or []) < len(_leituras_de(u, cegos))]
    if not unif:
        print("Nada a redigir.")
        return
    texto_prompt = secao_prompt("Texto do prompt da redação")
    lotes = [unif[i:i + args.lote] for i in range(0, len(unif), args.lote)]
    total_leituras = 0
    for n, lote in enumerate(lotes, 1):
        blocos = []
        for u in lote:
            grupos = []
            for h, chaves in _leituras_de(u, cegos):
                grupos.append({"heuristica": h, "nome": cegos[chaves[0]]["heuristica"],
                               "achados": [{"chave": k, **{c: cegos[k].get(c) for c in CAMPOS_ORIGINAIS}} for k in chaves]})
                total_leituras += 1
            blocos.append(json.dumps({"unificado": u["unificado"], "enunciado": u["enunciado"], "por_heuristica": grupos},
                                     ensure_ascii=False, indent=1))
        n_leit = sum(len(_leituras_de(u, cegos)) for u in lote)
        prompt = (texto_prompt
                  + f"\n\n---\n\nEste lote tem {len(lote)} achados unificados ({lote[0]['unificado']} a {lote[-1]['unificado']}), "
                  f"em {n_leit} pares achado unificado × heurística: responda com exatamente {n_leit} objetos em `redacoes`. "
                  "Responda **somente** com o JSON pedido, sem texto antes ou depois, sem cercas de código. "
                  "Não use ferramenta alguma: tudo de que você precisa está abaixo.\n\n## Achados unificados\n\n"
                  + "\n\n".join(blocos) + "\n")
        destino = pasta / f"redacao_lote_{n:02d}.md"
        destino.write_text(prompt, encoding="utf-8")
        print(f"{destino.name}: {len(lote)} achados unificados · {n_leit} leituras · {sum(len(u['achados']) for u in lote)} achados · "
              f"{len(prompt)} caracteres (~{len(prompt) // 3} tokens)")
    print(f"{len(lotes)} lote(s), {total_leituras} leituras, gravados em {pasta}")


def validar_redacao(pasta, _args):
    cegos = {a["chave"]: a for a in ler_json(pasta / "achados_cegos.json")}
    unif_doc = ler_json(pasta / "unificacao_ia.json")
    unif = {u["unificado"]: u for u in unif_doc["achados_unificados"]}
    esperados = {(uid, h): chaves for uid, u in unif.items() for h, chaves in _leituras_de(u, cegos)}
    # rodada 1: redacao_lote_NN_bruto.md; rodadas seguintes: redacao_lote_NN_bruto_r2.md, _r3.md, …
    # Um par redigido de novo numa rodada posterior substitui o da anterior; repetição só é erro dentro do mesmo arquivo.
    def ordem(caminho):
        m = re.fullmatch(r"redacao_lote_(\d+)_bruto(?:_r(\d+))?\.md", caminho.name)
        return (int(m.group(2) or 1), int(m.group(1))) if m else (99, 0)
    brutos = sorted(pasta.glob("redacao_lote_*_bruto*.md"), key=ordem)
    if not brutos:
        falhar("nenhum redacao_lote_NN_bruto.md na pasta")
    erros, avisos, novas = [], [], {}
    vistos = Counter()
    substituidos = 0
    for b in brutos:
        saida = extrair_json(b.read_text(encoding="utf-8"))
        lista = saida.get("redacoes")
        if not isinstance(lista, list):
            erros.append(f"{b.name}: `redacoes` ausente")
            continue
        vistos_neste = Counter()
        for r in lista:
            uid = str(r.get("unificado", "")).strip()
            h = str(r.get("heuristica", "")).strip().upper()
            par = (uid, h)
            if par not in esperados:
                erros.append(f"{b.name}: par desconhecido {uid} × {h}")
                continue
            vistos_neste[par] += 1
            if vistos_neste[par] > 1:
                erros.append(f"{b.name}: {uid} × {h} redigido {vistos_neste[par]} vezes no mesmo arquivo")
                continue
            if par in novas or any(e.startswith(f"{uid} × {h}:") for e in erros):
                substituidos += 1
            # a rodada posterior substitui o veredito anterior do par
            erros[:] = [e for e in erros if not e.startswith(f"{uid} × {h}:")]
            avisos[:] = [w for w in avisos if not w.startswith(f"{uid} × {h}:")]
            vistos[par] = 1
            faltando = [c for c in CAMPOS_REDACAO if not str(r.get(c, "")).strip()]
            if faltando:
                erros.append(f"{uid} × {h}: campo(s) vazio(s): {', '.join(faltando)}")
                continue
            leitura = {c: str(r.get(c, "")).strip() for c in CAMPOS_REDACAO}
            tam = sum(len(v) for v in leitura.values())
            maior = max(sum(len(str(cegos[k].get(c) or "")) for c in CAMPOS_REDACAO) for k in esperados[par])
            if tam > 1.5 * maior:
                erros.append(f"{uid} × {h}: leitura com {tam} caracteres, maior que 1,5 vez o maior achado que representa ({maior}); não é tamanho de achado")
                vistos[par] = 0
                continue
            elif tam > maior:
                avisos.append(f"{uid} × {h}: leitura ({tam} caracteres) um pouco maior que o maior achado ({maior})")
            if "—" in " ".join(leitura.values()):
                avisos.append(f"{uid} × {h}: a leitura usa travessão")
            novas[par] = {"heuristica": h, "nome_heuristica": cegos[esperados[par][0]]["heuristica"], "achados": esperados[par], **leitura}
    sem = [f"{u} × {h}" for (u, h) in esperados if (u, h) not in vistos]
    if sem:
        erros.append(f"{len(sem)} par(es) sem leitura: {', '.join(sem)}")

    resumo = ["# Conferência das leituras (redação unificada por heurística)", "",
              f"- Arquivos lidos: {len(brutos)} · achados unificados: {len(unif)} · pares esperados: {len(esperados)} · leituras aceitas: {len(novas)}"
              + (f" · pares refeitos em rodada posterior: {substituidos}" if substituidos else ""),
              f"- Erros: {len(erros)} · avisos: {len(avisos)}", ""]
    if erros:
        resumo += ["## Erros (as leituras do par com erro não são aceitas)", ""] + [f"- {e}" for e in erros] + [""]
    if avisos:
        resumo += ["## Avisos", ""] + [f"- {a}" for a in avisos] + [""]
    (pasta / "redacao_conferencia.md").write_text("\n".join(resumo) + "\n", encoding="utf-8")
    print("\n".join(resumo))
    if erros:
        sys.exit(1)
    for u in unif.values():
        u.pop("redacao", None)
        u["leituras"] = [novas[(u["unificado"], h)] for h, _ in _leituras_de(u, cegos)]
    gravar_json(pasta / "unificacao_ia.json", {"achados_unificados": sorted(unif.values(), key=lambda u: u["unificado"])})
    print(f"Leituras gravadas em {pasta / 'unificacao_ia.json'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("acao", choices=["montar", "validar", "montar-redacao", "validar-redacao"])
    ap.add_argument("--pasta", required=True, help="pasta cega da análise (com achados_cegos.json)")
    ap.add_argument("--lote", type=int, default=8, help="achados unificados por lote da redação (padrão 8)")
    ap.add_argument("--so-faltantes", action="store_true", help="montar-redacao: só os achados unificados com leituras faltando")
    args = ap.parse_args()
    pasta = Path(args.pasta).resolve()
    if not (pasta / "achados_cegos.json").exists():
        falhar(f"{pasta} não tem achados_cegos.json; rode reunir_cegar.py antes")
    if (pasta / "mapa_chaves.json").exists():
        falhar("mapa_chaves.json está dentro da pasta cega: o cegamento foi quebrado; mova-o para a pasta fechada")
    {"montar": montar, "validar": validar, "montar-redacao": montar_redacao, "validar-redacao": validar_redacao}[args.acao](pasta, args)


if __name__ == "__main__":
    main()
