# -*- coding: utf-8 -*-
"""(e) Métricas — `roteiro_estudo.md` 2.1(e) e 4.2; `protocolo/analise.md` §5.

Lê a trilha de decisões (`trilha_decisoes.csv`), os encerramentos (`encerramentos.json`) e a contagem
de achados fora do escopo (`fora_do_escopo.json`) e grava `metricas.json` (tudo, com denominadores) e
`metricas.md` (tabelas). Nada é recalculado por nível: chamada, execução, formato e agregado são
recortes da mesma lista de achados unificados pelos metadados (`analise.md` §2).

Uso:
    py analise/metricas.py --pasta <pasta da análise>   # depois de reatar_trilha.py

Convenções declaradas nas saídas:
- desvio-padrão amostral (n − 1); vazio com menos de duas execuções;
- moda da `severidade_ia` por defeito com empate resolvido pelo menor valor;
- kappa ponderado com pesos lineares, categorias 0 a 4;
- duplicação: os pontos de manifestação são os da IA, por achado unificado; quando o defeito tem mais de
  um ponto, recorrência e intrínseca saem juntas ("indeterminada").
"""
import argparse
import csv
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import chave_ordem_id, desvio_padrao_amostral, falhar, gravar_json, ler_json, media

FORMATOS = ["A", "B", "C"]
HEURISTICAS = [f"H{i}" for i in range(1, 11)]


# ----------------------------------------------------------------------------- leitura
def ler_trilha(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    if not linhas:
        falhar(f"{caminho} vazio")
    for l in linhas:
        l["execucao"] = int(l["execucao"])
        l["severidade_ia"] = int(l["severidade_ia"]) if l["severidade_ia"] not in ("", None) else None
        l["severidade_pesquisador"] = int(l["severidade_pesquisador"]) if l.get("severidade_pesquisador") else None
        l["pontos"] = [p for p in (l.get("pontos_manifestacao") or "").split("|") if p]
    return linhas


def razao(num, den):
    return None if not den else num / den


def kappa_ponderado(pares, categorias):
    """Kappa com pesos lineares. pares: lista de (a, b). Devolve None sem dados ou sem variação."""
    if not pares:
        return None
    k = len(categorias)
    idx = {c: i for i, c in enumerate(categorias)}
    O = [[0.0] * k for _ in range(k)]
    for a, b in pares:
        O[idx[a]][idx[b]] += 1
    n = len(pares)
    lin = [sum(r) for r in O]
    col = [sum(O[i][j] for i in range(k)) for j in range(k)]
    num = den = 0.0
    for i in range(k):
        for j in range(k):
            w = abs(i - j) / (k - 1)
            num += w * O[i][j]
            den += w * lin[i] * col[j] / n
    return None if den == 0 else 1 - num / den


def moda_menor(valores):
    c = Counter(valores)
    top = max(c.values())
    return min(v for v, n in c.items() if n == top)


# ----------------------------------------------------------------------------- cálculo
def calcular(trilha, encerramentos, fora):
    U = defaultdict(list)  # achado unificado -> achados
    for l in trilha:
        U[l["achado_unificado"]].append(l)
    classe = {u: ls[0]["classificacao"] for u, ls in U.items()}
    D = {u for u, c in classe.items() if c == "defeito"}
    FE = sorted({(l["formato"], l["execucao"]) for l in trilha})
    formatos = [f for f in FORMATOS if any(fe[0] == f for fe in FE)]
    execs = {f: sorted(e for (ff, e) in FE if ff == f) for f in formatos}

    def A(f, e=None):
        return [l for l in trilha if l["formato"] == f and (e is None or l["execucao"] == e)]

    def U_de(f, e=None):
        return {l["achado_unificado"] for l in A(f, e)}

    def D_de(f, e=None):
        return U_de(f, e) & D

    enc = {(x["formato"], int(x["execucao"])): x for x in encerramentos}
    fora_f = (fora or {}).get("contagem_por_formato", {})
    fora_fe = (fora or {}).get("contagem_por_formato_execucao", {})

    R = {"denominadores": {
        "D": len(D), "achados_unificados": len(U), "falsos_positivos": len(U) - len(D),
        "nota": "D é o conjunto agregado: união dos defeitos das execuções analisadas; nunca é proporção dos problemas do objeto."},
        "por_execucao": {}, "por_formato": {}, "sobreposicao": {}, "severidade": {}, "conferencias": []}

    # --- por execução
    for f, e in FE:
        a = A(f, e)
        u_fe = U_de(f, e)
        d_fe = D_de(f, e)
        ach_def = [l for l in a if l["achado_unificado"] in D]
        p_def = razao(len(d_fe), len(u_fe))
        rec = razao(len(d_fe), len(D))
        f1 = None if p_def is None or rec is None or (p_def + rec) == 0 else 2 * p_def * rec / (p_def + rec)

        # duplicação: achado de referência = primeiro achado de (F,e) no defeito, na ordem do id
        dup = Counter()
        for d in d_fe:
            ls = sorted([l for l in a if l["achado_unificado"] == d], key=lambda l: chave_ordem_id(l["id"]))
            ref = ls[0]
            multi_pontos = len(U[d][0]["pontos"]) > 1
            for ex in ls[1:]:
                if ex["heuristica"] != ref["heuristica"]:
                    dup["atribuicao_multipla"] += 1
                elif multi_pontos:
                    dup["recorrencia_ou_intrinseca_indeterminada"] += 1
                else:
                    dup["intrinseca"] += 1
        ampla = sum(dup.values())

        x = enc.get((f, e), {})
        chamadas = x.get("chamadas", [])
        dur_soma = x.get("duracao_ms_soma") or sum(int(c.get("duracao_ms") or 0) for c in chamadas)
        tokens = x.get("tokens_total")
        horas = dur_soma / 3_600_000 if dur_soma else None
        R["por_execucao"][f"{f}/{e}"] = {
            "formato": f, "execucao": e,
            "achados": len(a), "achados_unificados": len(u_fe), "defeitos": len(d_fe), "falsos_positivos": len(u_fe) - len(d_fe),
            "achados_em_defeitos": len(ach_def), "achados_em_falsos_positivos": len(a) - len(ach_def),
            "severidade_ia_zero": sum(1 for l in a if l["severidade_ia"] == 0),
            "fora_do_escopo": fora_fe.get(f"{f}/{e}", 0),
            "precisao_defeito": p_def, "precisao_achado": razao(len(ach_def), len(a)),
            "taxa_fp_defeito": None if p_def is None else 1 - p_def,
            "taxa_fp_achado": None if not a else 1 - len(ach_def) / len(a),
            "recall": rec, "f1": f1,
            "duplicacao": {"excedentes": dict(dup), "ampla": ampla,
                           "taxas": {k: razao(v, len(a)) for k, v in dup.items()}, "taxa_ampla": razao(ampla, len(a))},
            "custo": {"tokens_total": tokens, "usos_ferramenta_total": x.get("usos_ferramenta_total"),
                      "duracao_ms_soma": dur_soma or None, "duracao_ms_max": x.get("duracao_ms_max"),
                      "duracao_total_s": x.get("duracao_total_s"), "duracao_avaliacao_s": x.get("duracao_avaliacao_s"),
                      "modo_execucao": x.get("modo_execucao") or (x.get("execucao") if isinstance(x.get("execucao"), str) else None),
                      "concorrencia_observada": x.get("concorrencia_observada"),
                      "chamadas": [{"chamada": c.get("chamada"), "duracao_ms": c.get("duracao_ms"), "tokens": c.get("tokens"),
                                    "usos_ferramenta": c.get("usos_ferramenta"), "achados": c.get("achados")} for c in chamadas],
                      "defeitos_por_hora": None if not horas else len(d_fe) / horas,
                      "defeitos_por_mil_tokens": None if not tokens else len(d_fe) / (tokens / 1000)},
        }
        if x:
            esperado = int(x.get("achados_total", 0)) - fora_fe.get(f"{f}/{e}", 0)
            R["conferencias"].append({"execucao": f"{f}/{e}", "achados_trilha": len(a), "achados_encerramento_menos_fora": esperado,
                                      "bate": esperado == len(a)})
        else:
            R["conferencias"].append({"execucao": f"{f}/{e}", "achados_trilha": len(a), "erro": "sem encerramento"})

    # --- por formato
    for f in formatos:
        pe = [R["por_execucao"][f"{f}/{e}"] for e in execs[f]]
        d_f = D_de(f)
        u_f = U_de(f)
        a_f = A(f)

        def agreg(chave):
            vals = [p[chave] for p in pe if p[chave] is not None]
            return {"valores": {str(p["execucao"]): p[chave] for p in pe}, "media": media(vals), "dp": desvio_padrao_amostral(vals)}

        cons = {}
        if 1 in execs[f] and len(execs[f]) > 1:
            d1 = D_de(f, 1)
            for e in execs[f]:
                if e != 1:
                    cons[str(e)] = razao(len(D_de(f, e) & d1), len(d1))
            vals = [v for v in cons.values() if v is not None]
            cons = {"valores": cons, "media": media(vals), "dp": desvio_padrao_amostral(vals), "denominador_D_F_1": len(d1)}
        else:
            cons = {"nota": "exige execução 1 e pelo menos outra"}

        heur_por_def = {d: {l["heuristica"] for l in a_f if l["achado_unificado"] == d} for d in d_f}
        multi = sum(1 for hs in heur_por_def.values() if len(hs) >= 2)
        dist_a = Counter(l["heuristica"] for l in a_f)
        dist_d = Counter(h for hs in heur_por_def.values() for h in hs)

        p_def_f = razao(len(d_f), len(u_f))
        rec_f = razao(len(d_f), len(D))
        f1_f = None if p_def_f is None or rec_f is None or (p_def_f + rec_f) == 0 else 2 * p_def_f * rec_f / (p_def_f + rec_f)
        ach_def_f = sum(1 for l in a_f if l["achado_unificado"] in D)

        sev_dist = Counter(l["severidade_ia"] for l in a_f)
        coincide = total_multi = 0
        for d in d_f:
            por_exec = defaultdict(list)
            for l in a_f:
                if l["achado_unificado"] == d:
                    por_exec[l["execucao"]].append(l["severidade_ia"])
            if len(por_exec) >= 2:
                total_multi += 1
                coincide += len({moda_menor(v) for v in por_exec.values()}) == 1
        pares_f = []
        for d in d_f:
            sev_p = U[d][0]["severidade_pesquisador"]
            ia = [l["severidade_ia"] for l in a_f if l["achado_unificado"] == d and l["severidade_ia"] is not None]
            if sev_p is not None and ia:
                pares_f.append((moda_menor(ia), sev_p))

        tokens_f = [p["custo"]["tokens_total"] for p in pe if p["custo"]["tokens_total"]]
        dpmt = [p["custo"]["defeitos_por_mil_tokens"] for p in pe if p["custo"]["defeitos_por_mil_tokens"] is not None]
        R["por_formato"][f] = {
            "execucoes": execs[f], "achados": len(a_f), "achados_por_execucao": agreg("achados"),
            "defeitos_uniao": len(d_f), "defeitos_por_execucao": agreg("defeitos"),
            "achados_unificados_uniao": len(u_f), "achados_em_defeitos": ach_def_f,
            "severidade_ia_zero": sum(1 for l in a_f if l["severidade_ia"] == 0), "fora_do_escopo": fora_f.get(f, 0),
            "precisao_defeito_uniao": p_def_f, "precisao_defeito_por_execucao": agreg("precisao_defeito"),
            "precisao_achado_uniao": razao(ach_def_f, len(a_f)), "precisao_achado_por_execucao": agreg("precisao_achado"),
            "recall_uniao": rec_f, "recall_por_execucao": agreg("recall"), "f1_uniao": f1_f, "f1_por_execucao": agreg("f1"),
            "consistencia_entre_execucoes": cons,
            "duplicacao_ampla_por_execucao": {str(p["execucao"]): p["duplicacao"]["ampla"] for p in pe},
            "duplicacao_por_causa_soma": dict(sum((Counter(p["duplicacao"]["excedentes"]) for p in pe), Counter())),
            "indice_atribuicao_multipla": razao(multi, len(d_f)), "defeitos_com_duas_ou_mais_heuristicas": multi,
            "heuristicas_por_defeito_media": media([len(hs) for hs in heur_por_def.values()]) if heur_por_def else None,
            "distribuicao_heuristica": {h: {"achados": dist_a.get(h, 0), "defeitos": dist_d.get(h, 0)} for h in HEURISTICAS},
            "severidade_ia_distribuicao": {str(k): v for k, v in sorted(sev_dist.items(), key=lambda kv: (kv[0] is None, kv[0]))},
            "consistencia_severidade": {"defeitos_em_mais_de_uma_execucao": total_multi, "coincidem": coincide,
                                        "proporcao": razao(coincide, total_multi)},
            "concordancia_ia_pesquisador": {"defeitos": len(pares_f),
                                            "exata": razao(sum(1 for a, b in pares_f if a == b), len(pares_f)),
                                            "kappa_linear": kappa_ponderado(pares_f, [0, 1, 2, 3, 4])},
            "custo": {"tokens_soma": sum(tokens_f) if tokens_f else None, "tokens_media": media(tokens_f), "tokens_dp": desvio_padrao_amostral(tokens_f),
                      "duracao_ms_soma_total": sum(p["custo"]["duracao_ms_soma"] or 0 for p in pe) or None,
                      "defeitos_por_hora_media": media([p["custo"]["defeitos_por_hora"] for p in pe if p["custo"]["defeitos_por_hora"] is not None]),
                      "defeitos_por_mil_tokens_media": media(dpmt), "defeitos_por_mil_tokens_dp": desvio_padrao_amostral(dpmt)},
        }

    # --- sobreposição entre formatos
    Ds = {f: D_de(f) for f in formatos}
    R["sobreposicao"] = {
        "exclusivos": {f: {"n": len(Ds[f] - set().union(*(Ds[g] for g in formatos if g != f))),
                           "defeitos": sorted(Ds[f] - set().union(*(Ds[g] for g in formatos if g != f)))} for f in formatos},
        "jaccard": {f"{f}∩{g}": {"intersecao": len(Ds[f] & Ds[g]), "uniao": len(Ds[f] | Ds[g]), "jaccard": razao(len(Ds[f] & Ds[g]), len(Ds[f] | Ds[g]))}
                    for f, g in combinations(formatos, 2)},
        "comuns_a_todos": len(set.intersection(*Ds.values())) if Ds else 0,
        "cobertura_por_defeito": {d: "".join(f if d in Ds[f] else "·" for f in formatos) for d in sorted(D)},
    }

    # --- severidade agregada (IA × pesquisador, moda global)
    pares = []
    for d in sorted(D):
        sev_p = U[d][0]["severidade_pesquisador"]
        ia = [l["severidade_ia"] for l in U[d] if l["severidade_ia"] is not None]
        if sev_p is not None and ia:
            pares.append((moda_menor(ia), sev_p))
    R["severidade"] = {
        "concordancia_ia_pesquisador_agregado": {"defeitos": len(pares), "exata": razao(sum(1 for a, b in pares if a == b), len(pares)),
                                                 "kappa_linear": kappa_ponderado(pares, [0, 1, 2, 3, 4]),
                                                 "distribuicao_diferenca": dict(Counter(a - b for a, b in pares))},
        "severidade_pesquisador_distribuicao": dict(Counter(str(U[d][0]["severidade_pesquisador"]) for d in D)),
        "nota": "moda da severidade_ia por defeito, empate resolvido pelo menor valor; kappa ponderado, categorias 0 a 4",
    }
    R["fora_do_escopo_por_formato"] = {f: fora_f.get(f, 0) for f in formatos}
    R["achados_unificados"] = {u: {"classificacao": classe[u], "severidade_pesquisador": ls[0]["severidade_pesquisador"],
                                   "n_achados": len(ls), "achados": sorted(l["id"] + f"/e{l['execucao']}" for l in ls),
                                   "heuristicas": sorted({l["heuristica"] for l in ls}, key=lambda h: int(h[1:])),
                                   "elemento": ls[0]["elemento"], "pontos_manifestacao": ls[0]["pontos"]} for u, ls in sorted(U.items())}
    return R


# ----------------------------------------------------------------------------- relatório
def fmt(x, casas=3, pct=False):
    if x is None:
        return "—"
    if isinstance(x, int):
        return f"{x:,}".replace(",", ".")
    if pct:
        return f"{100 * x:.1f}%".replace(".", ",")
    return f"{x:.{casas}f}".replace(".", ",")


def tabela(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---:" if i else "---" for i in range(len(cab))) + "|"]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


def md(R):
    fs = list(R["por_formato"].keys())
    pe = R["por_execucao"]
    pf = R["por_formato"]
    den = R["denominadores"]
    S = [f"# Métricas (`protocolo/analise.md` §5)", "",
         f"Conjunto agregado |D| = **{den['D']}** defeitos, de {den['achados_unificados']} achados unificados "
         f"({den['falsos_positivos']} falsos positivos). Recortes: {', '.join(pe.keys())}. Desvio-padrão amostral (n − 1).", ""]

    S += ["## Conferências", "", tabela(["Execução", "Achados na trilha", "Encerramento − fora do escopo", "Bate"],
                                        [[c["execucao"], c["achados_trilha"], c.get("achados_encerramento_menos_fora", "—"),
                                          "sim" if c.get("bate") else ("**não**" if "bate" in c else c.get("erro"))] for c in R["conferencias"]]), ""]

    S += ["## Volume (unidades: achados e defeitos)", "",
          tabela(["Execução", "Achados A(F,e)", "Achados unificados", "Defeitos D(F,e)", "Falsos positivos", "Nota 0", "Fora do escopo"],
                 [[k, v["achados"], v["achados_unificados"], v["defeitos"], v["falsos_positivos"], v["severidade_ia_zero"], v["fora_do_escopo"]] for k, v in pe.items()]), "",
          tabela(["Formato", "Achados A(F)", "média ± DP", "Defeitos D(F)", "média ± DP", "Nota 0", "Fora do escopo"],
                 [[f, pf[f]["achados"], f"{fmt(pf[f]['achados_por_execucao']['media'], 1)} ± {fmt(pf[f]['achados_por_execucao']['dp'], 1)}",
                   pf[f]["defeitos_uniao"], f"{fmt(pf[f]['defeitos_por_execucao']['media'], 1)} ± {fmt(pf[f]['defeitos_por_execucao']['dp'], 1)}",
                   pf[f]["severidade_ia_zero"], pf[f]["fora_do_escopo"]] for f in fs]), ""]

    S += ["## Precisão, recall e F1 (denominador do recall: |D| = " + str(den["D"]) + ")", "",
          tabela(["Execução", "Precisão por defeito", "Precisão por achado", "Taxa FP (defeito)", "Taxa FP (achado)", "Recall", "F1"],
                 [[k, fmt(v["precisao_defeito"], pct=True), fmt(v["precisao_achado"], pct=True), fmt(v["taxa_fp_defeito"], pct=True),
                   fmt(v["taxa_fp_achado"], pct=True), fmt(v["recall"], pct=True), fmt(v["f1"])] for k, v in pe.items()]), "",
          tabela(["Formato", "Precisão por defeito (união)", "média ± DP", "Precisão por achado (união)", "Recall (união)", "Recall média ± DP", "F1 (união)"],
                 [[f, fmt(pf[f]["precisao_defeito_uniao"], pct=True),
                   f"{fmt(pf[f]['precisao_defeito_por_execucao']['media'], pct=True)} ± {fmt(pf[f]['precisao_defeito_por_execucao']['dp'])}",
                   fmt(pf[f]["precisao_achado_uniao"], pct=True), fmt(pf[f]["recall_uniao"], pct=True),
                   f"{fmt(pf[f]['recall_por_execucao']['media'], pct=True)} ± {fmt(pf[f]['recall_por_execucao']['dp'])}", fmt(pf[f]["f1_uniao"])] for f in fs]), ""]

    S += ["## Consistência entre execuções: D(F,e) ∩ D(F,1) ÷ D(F,1)", "",
          tabela(["Formato", "e = 2", "e = 3", "média", "DP", "tamanho de D(F,1)"],
                 [[f, fmt(pf[f]["consistencia_entre_execucoes"].get("valores", {}).get("2"), pct=True),
                   fmt(pf[f]["consistencia_entre_execucoes"].get("valores", {}).get("3"), pct=True),
                   fmt(pf[f]["consistencia_entre_execucoes"].get("media"), pct=True), fmt(pf[f]["consistencia_entre_execucoes"].get("dp")),
                   pf[f]["consistencia_entre_execucoes"].get("denominador_D_F_1", "—")] for f in fs]), ""]

    causas = ["atribuicao_multipla", "intrinseca", "recorrencia_ou_intrinseca_indeterminada"]
    S += ["## Duplicação (excedentes de um mesmo defeito na mesma execução; taxas ÷ A(F,e))", "",
          tabela(["Execução", "Atribuição múltipla", "Intrínseca", "Recorrência ou intrínseca (indeterminada)", "Ampla", "Taxa ampla"],
                 [[k] + [v["duplicacao"]["excedentes"].get(c, 0) for c in causas] + [v["duplicacao"]["ampla"], fmt(v["duplicacao"]["taxa_ampla"], pct=True)] for k, v in pe.items()]), "",
          "Os pontos de manifestação são os da IA, por achado unificado; quando o defeito tem mais de um ponto, recorrência e intrínseca não se separam.", ""]

    S += ["## Atribuição heurística", "",
          tabela(["Formato", "Defeitos de D(F) com ≥ 2 heurísticas", "Índice de atribuição múltipla", "Heurísticas por defeito (média)"],
                 [[f, pf[f]["defeitos_com_duas_ou_mais_heuristicas"], fmt(pf[f]["indice_atribuicao_multipla"], pct=True),
                   fmt(pf[f]["heuristicas_por_defeito_media"], 2)] for f in fs]), "",
          tabela(["Heurística"] + [f"{f} achados" for f in fs] + [f"{f} defeitos" for f in fs],
                 [[h] + [pf[f]["distribuicao_heuristica"][h]["achados"] for f in fs] + [pf[f]["distribuicao_heuristica"][h]["defeitos"] for f in fs] for h in HEURISTICAS]), ""]

    so = R["sobreposicao"]
    S += ["## Sobreposição entre formatos", "",
          tabela(["Formato", "Defeitos exclusivos"], [[f, so["exclusivos"][f]["n"]] for f in fs]), "",
          tabela(["Par", "Interseção", "União", "Jaccard"], [[k, v["intersecao"], v["uniao"], fmt(v["jaccard"])] for k, v in so["jaccard"].items()]), "",
          f"Defeitos comuns a todos os formatos: **{so['comuns_a_todos']}**.", ""]

    sev = R["severidade"]["concordancia_ia_pesquisador_agregado"]
    S += ["## Severidade", "",
          tabela(["Formato"] + [f"nota {n}" for n in range(5)] + ["Consistência entre execuções (defeitos em ≥ 2 exec.)", "Concordância exata IA × pesquisador", "Kappa linear"],
                 [[f] + [pf[f]["severidade_ia_distribuicao"].get(str(n), 0) for n in range(5)]
                  + [f"{pf[f]['consistencia_severidade']['coincidem']} de {pf[f]['consistencia_severidade']['defeitos_em_mais_de_uma_execucao']} ({fmt(pf[f]['consistencia_severidade']['proporcao'], pct=True)})",
                     fmt(pf[f]["concordancia_ia_pesquisador"]["exata"], pct=True), fmt(pf[f]["concordancia_ia_pesquisador"]["kappa_linear"])] for f in fs]), "",
          f"Agregado (moda da severidade_ia por defeito × severidade_pesquisador, {sev['defeitos']} defeitos): concordância exata "
          f"{fmt(sev['exata'], pct=True)}, kappa linear {fmt(sev['kappa_linear'])}. "
          f"Distribuição de severidade_pesquisador: {R['severidade']['severidade_pesquisador_distribuicao']}.", ""]

    S += ["## Custo e eficiência", "",
          tabela(["Execução", "Modo", "Concorrência observada", "Tokens", "Usos de ferramenta", "Soma das chamadas (min)", "Chamada mais longa (min)", "Parede (min)", "Defeitos por hora", "Defeitos por mil tokens"],
                 [[k, v["custo"]["modo_execucao"] or "—", v["custo"]["concorrencia_observada"] or "—", fmt(v["custo"]["tokens_total"]), fmt(v["custo"]["usos_ferramenta_total"]),
                   fmt((v["custo"]["duracao_ms_soma"] or 0) / 60000, 1) if v["custo"]["duracao_ms_soma"] else "—",
                   fmt((v["custo"]["duracao_ms_max"] or 0) / 60000, 1) if v["custo"]["duracao_ms_max"] else "—",
                   fmt((v["custo"]["duracao_total_s"] or 0) / 60, 1) if v["custo"]["duracao_total_s"] else "—",
                   fmt(v["custo"]["defeitos_por_hora"], 1), fmt(v["custo"]["defeitos_por_mil_tokens"])] for k, v in pe.items()]), "",
          tabela(["Formato", "Tokens (soma)", "Tokens por execução (média ± DP)", "Defeitos por hora (média)", "Defeitos por mil tokens (média ± DP)"],
                 [[f, fmt(pf[f]["custo"]["tokens_soma"]),
                   f"{fmt(round(pf[f]['custo']['tokens_media']) if pf[f]['custo']['tokens_media'] is not None else None)} ± {fmt(round(pf[f]['custo']['tokens_dp']) if pf[f]['custo']['tokens_dp'] is not None else None)}",
                   fmt(pf[f]["custo"]["defeitos_por_hora_media"], 1), f"{fmt(pf[f]['custo']['defeitos_por_mil_tokens_media'])} ± {fmt(pf[f]['custo']['defeitos_por_mil_tokens_dp'])}"] for f in fs]), "",
          "Tempo de parede só é comparável entre formatos com a ressalva de `modo_execucao` e `concorrencia_observada`; "
          "defeitos por hora usa a soma das durações das chamadas (descritiva, porque em A e B cada chamada sofre contenção).", ""]

    S += ["## Contagens à parte", "",
          tabela(["Formato", "Achados fora do escopo", "Candidatos com nota 0 (dentro de A)"],
                 [[f, pf[f]["fora_do_escopo"], pf[f]["severidade_ia_zero"]] for f in fs]), ""]
    return "\n".join(S)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pasta", required=True, help="pasta da análise, depois da reatação")
    ap.add_argument("--trilha", help="padrão: <pasta>/trilha_decisoes.csv")
    ap.add_argument("--encerramentos", help="padrão: <pasta>/encerramentos.json (ou <pasta>-fechado/)")
    ap.add_argument("--fora-do-escopo", help="padrão: <pasta>/fora_do_escopo.json (ou <pasta>-fechado/)")
    args = ap.parse_args()
    pasta = Path(args.pasta).resolve()
    fechado = pasta.with_name(pasta.name + "-fechado")

    def achar(nome, explicito):
        if explicito:
            return Path(explicito)
        for base in (pasta, fechado):
            if (base / nome).exists():
                return base / nome
        return None

    trilha_p = achar("trilha_decisoes.csv", args.trilha)
    enc_p = achar("encerramentos.json", args.encerramentos)
    fora_p = achar("fora_do_escopo.json", args.fora_do_escopo)
    if not trilha_p or not trilha_p.exists():
        falhar("trilha_decisoes.csv não encontrada; rode reatar_trilha.py antes")
    if not enc_p or not enc_p.exists():
        falhar("encerramentos.json não encontrado")
    R = calcular(ler_trilha(trilha_p), ler_json(enc_p), ler_json(fora_p) if fora_p else None)
    R["fontes"] = {"trilha": str(trilha_p), "encerramentos": str(enc_p), "fora_do_escopo": str(fora_p) if fora_p else None}
    gravar_json(pasta / "metricas.json", R)
    (pasta / "metricas.md").write_text(md(R) + "\n", encoding="utf-8")
    print(md(R))
    print(f"\nGravados {pasta / 'metricas.json'} e {pasta / 'metricas.md'}")


if __name__ == "__main__":
    main()
