# -*- coding: utf-8 -*-
"""(a) Reunião e cegamento dos achados — `roteiro_estudo.md` 2.1(a) e 2.2; `protocolo/analise.md` §2 passos 1-2.

Lê os JSONL das execuções, exclui os achados com `fora_do_escopo = true` (contados à parte), embaralha
com semente declarada, atribui a chave substituta K001…, remove id, formato, execução, chamada e os
nomes de arquivo do `registro_visual`, copia as evidências renomeadas pela chave e guarda o mapa
`chave -> id` numa pasta separada, que ninguém abre até a reatação.

Uso:
    py analise/reunir_cegar.py --coleta . --semente 20260921 --saida "../entregas/analise-2026-09-21"
    py analise/reunir_cegar.py --manifesto analise/fontes/ensaio_paralelo_2026-09-13.json --semente 20260913 --saida <pasta>

Saídas:
    <saida>/achados_cegos.json             só os campos de `unificacao.md` (entrada da IA)
    <saida>/achados_cegos_evidencias.json  chave -> registro_visual com nomes cegos e lista de arquivos (entrada da planilha)
    <saida>/semente.txt
    <saida>/evidencias_cegas/K###.*
    <saida>/reuniao.md                     só totais, nada por formato
    <saida>-fechado/mapa_chaves.json       chave -> id, formato, execucao, chamada, severidade_ia, heuristica
    <saida>-fechado/encerramentos.json     custo e tempo por (formato, execução), para as métricas
    <saida>-fechado/cabecalhos.json
    <saida>-fechado/fora_do_escopo.json    os achados excluídos, na íntegra, e a contagem por formato
    <saida>-fechado/reuniao_relatorio.md   conferências, com detalhe por formato
"""
import argparse
import random
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import (CAMPOS_CEGOS_IA, RAIZ_INSTRUMENTO, RE_ARQUIVO_EVIDENCIA, RE_ID, chamada_do_id,
                   codigo_heuristica, falhar, formatar_chave, gravar_json, largura_chaves, ler_json,
                   ler_jsonl, partes_id)

ARQUIVOS_EXCLUIDOS = (".achado.md",)  # carrega id, formato e chamada no cabeçalho

# nome de arquivo de evidência: o id, um sufixo opcional de letra, e o ponto. O sufixo de letra
# apareceu na coleta de 21 a 23/09/2026 (`A-H5-003b.1.png`, `B-G2-009b.snapshot.txt`) e pertence ao
# achado de id base, que o cita na prosa do `registro_visual`. O RE_ID não serve aqui: ele exige
# fronteira de palavra depois dos três dígitos, que a letra do sufixo elimina.
RE_ARQUIVO_DE_ACHADO = re.compile(r"^([ABC]-(?:H\d{1,2}|G\d)-\d{3})[A-Za-z]?\.")


def descobrir_coleta(raiz):
    """resultados/exec-<n>/resultados_<F>.jsonl pareado com evidencias/exec-<n>/<F>/."""
    raiz = Path(raiz)
    fontes = []
    for jsonl in sorted(raiz.glob("resultados/exec-*/resultados_*.jsonl")):
        m = re.fullmatch(r"exec-(\d+)", jsonl.parent.name)
        f = re.fullmatch(r"resultados_([ABC])\.jsonl", jsonl.name)
        if not (m and f):
            continue
        fontes.append({"jsonl": str(jsonl),
                       "evidencias": str(raiz / "evidencias" / jsonl.parent.name / f.group(1)),
                       "execucao": int(m.group(1))})
    if not fontes:
        falhar(f"nenhum resultados/exec-*/resultados_*.jsonl em {raiz}")
    return fontes


def ler_manifesto(caminho):
    man = ler_json(caminho)
    base = RAIZ_INSTRUMENTO
    fontes = []
    for f in man["fontes"]:
        jsonl = Path(f["jsonl"])
        ev = Path(f["evidencias"]) if f.get("evidencias") else None
        fontes.append({"jsonl": str(jsonl if jsonl.is_absolute() else base / jsonl),
                       "evidencias": None if ev is None else str(ev if ev.is_absolute() else base / ev),
                       "execucao": f.get("execucao")})
    return fontes


def execucao_da_fonte(fonte, cab):
    if fonte.get("execucao") is not None:
        return int(fonte["execucao"])
    ex = cab.get("execucao")
    if isinstance(ex, int):
        return ex
    falhar(f"{fonte['jsonl']}: o cabeçalho não traz `execucao` numérica; declare `execucao` na fonte")


def indexar_evidencias(pasta):
    """id -> lista de arquivos cujo nome começa por '<id>.' (recursivo), sem os .achado.md.

    Aceita também um sufixo de letra entre o id e o ponto, ligando-o ao mesmo achado: na coleta de
    21 a 23/09/2026 quatro arquivos saíram como `A-H5-003b.1.png` e `B-G2-009b.snapshot.txt`, citados
    na prosa do `registro_visual` do achado de id base, e sem isso ficavam fora do conjunto cego.
    """
    idx = defaultdict(list)
    if not pasta or not Path(pasta).is_dir():
        return idx
    for p in Path(pasta).rglob("*"):
        if not p.is_file() or p.name.endswith(ARQUIVOS_EXCLUIDOS):
            continue
        m = RE_ARQUIVO_DE_ACHADO.match(p.name)
        if m:
            idx[m.group(1)].append(p)
    return idx


def limpar_registro_visual(texto):
    """Remove os nomes de arquivo e arruma os separadores que sobram. Fica só a âncora em prosa."""
    # Só se mexe no que está colado a um nome de arquivo; a prosa fica intacta.
    s = RE_ARQUIVO_EVIDENCIA.sub("\x00", texto)
    s = re.sub(r"\x00(?:\s*(?:·|\be\b|,|;)\s*\x00)+", "\x00", s)   # "X.png e X.2.png · X.txt" -> um marcador
    s = re.sub(r"\x00\s*\((?:ambas|ambos|todas|todos)\s+", "\x00(", s)  # "(ambas área visível)" -> "(área visível)"
    s = re.sub(r"\x00\s*(?:·|—|–|\.|,|;|\s-\s)\s*", "\x00", s)    # separador logo depois do marcador
    s = re.sub(r"\s*(?:·|—|–|,|;|\s-\s)\s*\x00", "\x00", s)       # separador logo antes do marcador
    s = s.replace("\x00", " ")
    s = re.sub(r"\s{2,}", " ", s).strip(" ·—–,;.-")
    return s.strip()


RE_ID_EM_TEXTO = re.compile(r"\b([ABC]-(?:H\d{1,2}|G\d)-\d{3})([a-z]?)(?![0-9A-Za-z])")


def substituir_ids(texto, id_para_chave):
    """Troca qualquer id que apareça no texto pela chave cega correspondente ('[achado]' se desconhecido).

    Tolera o sufixo de letra do id e o preserva, para `A-H5-003b.1` virar `K174b.1`, igual ao nome que
    o arquivo recebe na pasta cega. O `RE_ID` não serve aqui: exige fronteira de palavra depois dos
    três dígitos, que a letra elimina, e o id ficaria à mostra no texto que o pesquisador lê.
    """
    def troca(m):
        return id_para_chave.get(m.group(1), "[achado]") + m.group(2)

    return RE_ID_EM_TEXTO.sub(troca, texto)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--coleta", help="raiz do instrumento com resultados/exec-*/ e evidencias/exec-*/")
    g.add_argument("--manifesto", help="JSON com a lista de fontes (jsonl, evidencias, execucao)")
    ap.add_argument("--semente", type=int, required=True, help="semente do embaralhamento, declarada")
    ap.add_argument("--saida", required=True, help="pasta cega de saída; a pasta fechada é <saida>-fechado")
    ap.add_argument("--sem-evidencias", action="store_true", help="não copia as evidências")
    ap.add_argument("--sobrescrever", action="store_true")
    args = ap.parse_args()

    fontes = descobrir_coleta(args.coleta) if args.coleta else ler_manifesto(args.manifesto)
    saida = Path(args.saida).resolve()
    fechado = saida.with_name(saida.name + "-fechado")
    for p in (saida, fechado):
        if p.exists() and any(p.iterdir()) and not args.sobrescrever:
            falhar(f"{p} já existe e não está vazia; use --sobrescrever")
    saida.mkdir(parents=True, exist_ok=True)
    fechado.mkdir(parents=True, exist_ok=True)

    # 1. Reunião
    reunidos, fora, cabecalhos, encerramentos = [], [], [], []
    vistos = set()
    for fonte in fontes:
        cab, achados, enc = ler_jsonl(fonte["jsonl"])
        formato = cab["formato"]
        execucao = execucao_da_fonte(fonte, cab)
        cab = dict(cab, execucao=execucao, _arquivo=fonte["jsonl"])
        enc = dict(enc, formato=formato, execucao=execucao, _arquivo=fonte["jsonl"])
        cabecalhos.append(cab)
        encerramentos.append(enc)
        idx = indexar_evidencias(fonte["evidencias"]) if not args.sem_evidencias else {}
        for a in achados:
            if a.get("formato") != formato:
                falhar(f"{fonte['jsonl']}: achado {a.get('id')} com formato {a.get('formato')!r} diferente do cabeçalho {formato!r}")
            f_id, _, _ = partes_id(a.get("id"))
            if f_id != formato:
                falhar(f"{fonte['jsonl']}: id {a['id']} não é do formato {formato}")
            marca = (formato, execucao, a["id"])
            if marca in vistos:
                falhar(f"{fonte['jsonl']}: id repetido dentro da execução: {a['id']}")
            vistos.add(marca)
            item = {"achado": a, "formato": formato, "execucao": execucao, "fonte": fonte["jsonl"],
                    "evidencias": sorted(idx.get(a["id"], []), key=lambda p: p.name)}
            (fora if a.get("fora_do_escopo") is True else reunidos).append(item)

    hashes = {c.get("objeto_hash_sha256") for c in cabecalhos}
    contextos = {c.get("contexto_hash_sha256") for c in cabecalhos}

    # 2. Embaralhamento com semente declarada, sobre a ordem determinística de entrada
    rng = random.Random(args.semente)
    ordem = list(range(len(reunidos)))
    rng.shuffle(ordem)
    largura = largura_chaves(len(reunidos))
    id_para_chave = {}  # (formato, execucao, id) -> chave, para trocar referências cruzadas
    for n, i in enumerate(ordem, 1):
        it = reunidos[i]
        it["chave"] = formatar_chave(n, largura)
        id_para_chave[(it["formato"], it["execucao"], it["achado"]["id"])] = it["chave"]

    # 3. Cegamento
    cegos, cegos_evidencias, mapa = [], {}, {}
    sem_evidencia, arquivos_copiados = [], 0
    pasta_cega = saida / "evidencias_cegas"
    if not args.sem_evidencias:
        pasta_cega.mkdir(exist_ok=True)
    for it in sorted(reunidos, key=lambda x: x["chave"]):
        a, chave = it["achado"], it["chave"]
        # uma referência cruzada só faz sentido dentro do mesmo formato e da mesma execução
        locais = {id_: k for (f, e, id_), k in id_para_chave.items() if f == it["formato"] and e == it["execucao"]}
        cego = {"chave": chave}
        for campo in CAMPOS_CEGOS_IA:
            v = a.get(campo)
            if campo == "registro_visual":
                v = limpar_registro_visual(v or "")
            if isinstance(v, str):
                v = substituir_ids(v, locais)
            cego[campo] = v
        cegos.append(cego)

        nomes_cegos = []
        for p in it["evidencias"]:
            novo = chave + p.name[len(a["id"]):]
            nomes_cegos.append(novo)
            if not args.sem_evidencias:
                shutil.copy2(p, pasta_cega / novo)
                arquivos_copiados += 1
        if not it["evidencias"] and not args.sem_evidencias:
            sem_evidencia.append(chave)
        rv_cego = RE_ARQUIVO_EVIDENCIA.sub(lambda m, _c=chave, _i=a["id"]: _c + m.group(0)[len(_i):],
                                          a.get("registro_visual") or "")
        cegos_evidencias[chave] = {"registro_visual_cego": substituir_ids(rv_cego, locais), "arquivos": nomes_cegos}

        mapa[chave] = {
            "id": a["id"], "formato": it["formato"], "execucao": it["execucao"], "chamada": chamada_do_id(a["id"]),
            "heuristica": codigo_heuristica(a["heuristica"]), "severidade_ia": a.get("severidade"),
            "fonte": it["fonte"], "evidencias_originais": [str(p) for p in it["evidencias"]],
        }

    # 4. Gravação
    gravar_json(saida / "achados_cegos.json", cegos)
    gravar_json(saida / "achados_cegos_evidencias.json", cegos_evidencias)
    ordem_entrada = " | ".join(f"{c['formato']}/exec-{c['execucao']}" for c in cabecalhos)
    (saida / "semente.txt").write_text(
        f"semente={args.semente}\n"
        f"algoritmo=random.Random(semente).shuffle sobre a ordem de entrada das fontes\n"
        f"ordem_de_entrada={ordem_entrada}\n"
        f"total_achados_cegos={len(cegos)}\nlargura_chave={largura}\n"
        f"data={datetime.now().isoformat(timespec='seconds')}\n", encoding="utf-8")
    gravar_json(fechado / "mapa_chaves.json", {"semente": args.semente, "chaves": mapa})
    gravar_json(fechado / "encerramentos.json", encerramentos)
    gravar_json(fechado / "cabecalhos.json", cabecalhos)
    por_formato_fora = Counter(it["formato"] for it in fora)
    por_fe_fora = Counter(f"{it['formato']}/{it['execucao']}" for it in fora)
    gravar_json(fechado / "fora_do_escopo.json", {
        "contagem_por_formato": {f: por_formato_fora.get(f, 0) for f in "ABC"},
        "contagem_por_formato_execucao": dict(sorted(por_fe_fora.items())),
        "achados": [dict(it["achado"], execucao=it["execucao"]) for it in fora]})

    # 5. Conferências (roteiro 2.2): achados cegos = soma dos achados dos encerramentos - fora do escopo
    total_enc = sum(int(e.get("achados_total", 0)) for e in encerramentos)
    bate = (total_enc - len(fora)) == len(cegos)
    linhas = [f"# Reunião e cegamento — {datetime.now():%d/%m/%Y %H:%M}", "",
              f"- Fontes: {len(fontes)} JSONL", f"- Semente: {args.semente}",
              f"- Achados reunidos e cegos: **{len(cegos)}**",
              f"- Achados fora do escopo (contados à parte): {len(fora)}",
              f"- Soma de `achados_total` dos encerramentos: {total_enc}; conferência "
              f"{'**passou**' if bate else '**REPROVOU**'} ({total_enc} - {len(fora)} {'=' if bate else '!='} {len(cegos)})",
              f"- Hash do objeto único nas fontes: {'sim' if len(hashes) == 1 else '**NÃO: ' + str(len(hashes)) + ' hashes**'}",
              f"- Hash do contexto único nas fontes: {'sim' if len(contextos) == 1 else '**NÃO: ' + str(len(contextos)) + ' hashes**'}"]
    if not args.sem_evidencias:
        linhas += [f"- Arquivos de evidência copiados para `evidencias_cegas/`: {arquivos_copiados}",
                   f"- Chaves sem nenhum arquivo de evidência: {len(sem_evidencia)}"
                   + (" (" + ", ".join(sem_evidencia) + ")" if sem_evidencia else "")]
    (saida / "reuniao.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    por_fe = Counter((it["formato"], it["execucao"]) for it in reunidos)
    detalhe = ["", "## Por formato e execução (só na pasta fechada)", "",
               "| Formato | Execução | Achados cegos | Fora do escopo | `achados_total` no encerramento | Confere |",
               "|---|---|---:|---:|---:|---|"]
    for e in encerramentos:
        k = (e["formato"], e["execucao"])
        n_fora = por_fe_fora.get(f"{k[0]}/{k[1]}", 0)
        ok = (int(e.get("achados_total", 0)) - n_fora) == por_fe.get(k, 0)
        detalhe.append(f"| {k[0]} | {k[1]} | {por_fe.get(k, 0)} | {n_fora} | {e.get('achados_total')} | {'sim' if ok else '**não**'} |")
    (fechado / "reuniao_relatorio.md").write_text("\n".join(linhas + detalhe) + "\n", encoding="utf-8")

    print("\n".join(linhas))
    print(f"\nPasta cega:    {saida}\nPasta fechada: {fechado}  (não abrir até o passo 3.5)")
    if not bate:
        sys.exit(2)


if __name__ == "__main__":
    main()
