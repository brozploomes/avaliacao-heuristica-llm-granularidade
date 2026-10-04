# -*- coding: utf-8 -*-
"""Integridade da revisão — `roteiro_estudo.md` 3.3.

Confere `decisoes.json` (gravado pela página de `revisar.py`) contra `unificacao_ia.json`, sem abrir o
mapa de chaves: todo achado unificado decidido; classificação no domínio; defeito com severidade 1 a 4;
falso positivo sem severidade; nenhum identificador desconhecido. Grava `integridade.md` na pasta e falha
(código 1) enquanto houver pendência.

Uso:
    py analise/validar_revisao.py --pasta <pasta cega>

`reatar_trilha.py` chama as mesmas funções antes de reatar: a trilha só é gerada com integridade limpa.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import DOMINIOS, SEVERIDADES_PESQUISADOR, falhar, ler_json


def carregar(pasta):
    unif = ler_json(pasta / "unificacao_ia.json")["achados_unificados"]
    dec_p = pasta / "decisoes.json"
    dec = ler_json(dec_p)["achados_unificados"] if dec_p.exists() else {}
    return unif, dec


def validar(unificados, decisoes):
    erros, avisos = [], []
    ids = [u["unificado"] for u in unificados]
    for uid in ids:
        d = decisoes.get(uid)
        if not d or not d.get("classificacao"):
            erros.append(f"{uid}: sem decisão")
            continue
        c = d["classificacao"]
        sev = d.get("severidade")
        if c not in DOMINIOS["classificacao"]:
            erros.append(f"{uid}: classificacao={c!r} fora do domínio")
        elif c == "defeito" and sev not in SEVERIDADES_PESQUISADOR:
            erros.append(f"{uid}: defeito sem severidade 1 a 4 (valor: {sev!r})")
        elif c == "falso_positivo" and sev not in (None, ""):
            erros.append(f"{uid}: falso positivo com severidade preenchida ({sev})")
    for uid in decisoes:
        if uid not in ids:
            avisos.append(f"{uid}: decisão para um identificador que não está em unificacao_ia.json; será ignorada")
    return erros, avisos


def relatorio(erros, avisos, unificados, decisoes):
    n_def = sum(1 for u in unificados if (decisoes.get(u["unificado"]) or {}).get("classificacao") == "defeito")
    n_fp = sum(1 for u in unificados if (decisoes.get(u["unificado"]) or {}).get("classificacao") == "falso_positivo")
    linhas = ["# Integridade da revisão", "",
              f"- Achados unificados: {len(unificados)} · decididos: {n_def + n_fp} · defeitos: {n_def} · falsos positivos: {n_fp}",
              f"- Erros: {len(erros)} · avisos: {len(avisos)}", ""]
    if erros:
        linhas += ["## Pendências (a reatação não roda)", ""] + [f"- {e}" for e in erros] + [""]
    if avisos:
        linhas += ["## Avisos", ""] + [f"- {a}" for a in avisos] + [""]
    if not erros:
        linhas += ["Sem pendência. O mapa de chaves pode ser aberto (passo 4.1).", ""]
    return "\n".join(linhas)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pasta", required=True)
    args = ap.parse_args()
    pasta = Path(args.pasta).resolve()
    if not (pasta / "unificacao_ia.json").exists():
        falhar(f"{pasta / 'unificacao_ia.json'} não existe")
    unif, dec = carregar(pasta)
    erros, avisos = validar(unif, dec)
    texto = relatorio(erros, avisos, unif, dec)
    (pasta / "integridade.md").write_text(texto + "\n", encoding="utf-8")
    print(texto)
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
