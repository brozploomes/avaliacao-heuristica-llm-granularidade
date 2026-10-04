# -*- coding: utf-8 -*-
"""(d) Reatação e trilha de decisões — `roteiro_estudo.md` 2.1(d) e 4.1; `analise.md` §2 passo 5 e §4.

Reatar é religar a origem: durante a revisão cada achado circulou só com a chave K###; aqui o mapa
`chave -> id` devolve a cada achado o id, o formato, a execução, a chamada e a severidade da IA. Junto com
as decisões do pesquisador (`decisoes.json`) e a saída da IA (`unificacao_ia.json`), isso vira
`trilha_decisoes.csv`: `;` como separador, campos livres entre aspas duplas (aspas internas duplicadas),
uma linha por achado, as 13 colunas do §4 na ordem declarada.

Só roda com a integridade limpa (validar_revisao.py). Como a reatação encerra o cegamento, copia o
conteúdo da pasta fechada para a pasta da análise (mapa, encerramentos, cabeçalhos, fora do escopo).

Uso:
    py analise/reatar_trilha.py --pasta <pasta cega> [--fechado <pasta>-fechado] [--nao-copiar]
"""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import COLUNAS_LIVRES, COLUNAS_TRILHA, falhar, ler_json
from validar_revisao import carregar, relatorio, validar

COPIAR = ["mapa_chaves.json", "encerramentos.json", "cabecalhos.json", "fora_do_escopo.json", "reuniao_relatorio.md"]


def campo_csv(valor, coluna):
    s = "" if valor is None else str(valor)
    if coluna in COLUNAS_LIVRES or any(ch in s for ch in ';"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pasta", required=True)
    ap.add_argument("--fechado", help="padrão: <pasta>-fechado")
    ap.add_argument("--nao-copiar", action="store_true", help="não copia a pasta fechada para a pasta da análise")
    args = ap.parse_args()
    pasta = Path(args.pasta).resolve()
    fechado = Path(args.fechado).resolve() if args.fechado else pasta.with_name(pasta.name + "-fechado")
    for p in (pasta / "achados_cegos.json", pasta / "unificacao_ia.json", pasta / "decisoes.json", fechado / "mapa_chaves.json"):
        if not p.exists():
            falhar(f"{p} não existe")

    cegos = ler_json(pasta / "achados_cegos.json")
    unif, dec = carregar(pasta)
    erros, avisos = validar(unif, dec)
    (pasta / "integridade.md").write_text(relatorio(erros, avisos, unif, dec) + "\n", encoding="utf-8")
    if erros:
        print(relatorio(erros, avisos, unif, dec))
        falhar("a revisão tem pendências; complete as decisões antes de reatar")

    mapa = ler_json(fechado / "mapa_chaves.json")["chaves"]
    por_chave = {}
    for u in unif:
        for k in u["achados"]:
            if k in por_chave:
                falhar(f"chave {k} em mais de um achado unificado ({por_chave[k]['unificado']} e {u['unificado']})")
            por_chave[k] = u
    sem_unificado = [a["chave"] for a in cegos if a["chave"] not in por_chave]
    if sem_unificado:
        falhar(f"{len(sem_unificado)} achado(s) cegos fora de qualquer achado unificado: {', '.join(sem_unificado)}")

    linhas, sem_id = [], []
    for a in sorted(cegos, key=lambda x: x["chave"]):
        k = a["chave"]
        m = mapa.get(k)
        if m is None:
            sem_id.append(k)
            continue
        u = por_chave[k]
        d = dec[u["unificado"]]
        defeito = d["classificacao"] == "defeito"
        linhas.append({
            "chave": k, "id": m["id"], "formato": m["formato"], "execucao": m["execucao"], "chamada": m["chamada"],
            "heuristica": m["heuristica"], "severidade_ia": m["severidade_ia"],
            "achado_unificado": u["unificado"], "classificacao": d["classificacao"],
            "severidade_pesquisador": d.get("severidade") if defeito else "",
            "elemento": u.get("elemento", ""), "pontos_manifestacao": "|".join(u.get("pontos_manifestacao", [])),
            "observacao": d.get("observacao") or "",
        })
    if sem_id:
        falhar(f"{len(sem_id)} chave(s) sem id no mapa: {', '.join(sem_id)}")

    destino = pasta / "trilha_decisoes.csv"
    with open(destino, "w", encoding="utf-8", newline="") as f:
        f.write(";".join(COLUNAS_TRILHA) + "\n")
        for l in linhas:
            f.write(";".join(campo_csv(l[c], c) for c in COLUNAS_TRILHA) + "\n")

    if not args.nao_copiar:
        for nome in COPIAR:
            if (fechado / nome).exists():
                shutil.copy2(fechado / nome, pasta / nome)

    n_def = sum(1 for u in unif if dec[u["unificado"]]["classificacao"] == "defeito")
    texto = ["# Reatação", "",
             f"- Linhas da trilha: {len(linhas)} · achados cegos: {len(cegos)} · confere: {'sim' if len(linhas) == len(cegos) else '**não**'}",
             f"- Colunas: {len(COLUNAS_TRILHA)} (as do §4)",
             f"- Achados unificados: {len(unif)} · defeitos (|D|): {n_def} · falsos positivos: {len(unif) - n_def}",
             f"- Pasta fechada copiada para a pasta da análise: {'não (--nao-copiar)' if args.nao_copiar else 'sim'}", ""]
    if avisos:
        texto += ["## Avisos da integridade", ""] + [f"- {a}" for a in avisos] + [""]
    (pasta / "reatacao.md").write_text("\n".join(texto) + "\n", encoding="utf-8")
    print("\n".join(texto))
    print(f"Gravado {destino}")


if __name__ == "__main__":
    main()
