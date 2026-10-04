# -*- coding: utf-8 -*-
"""Funções compartilhadas pelos scripts da análise.

Vocabulário: `protocolo/analise.md` §1. Um **achado** é uma linha de JSONL sem a chave `registro`;
as linhas com `registro = cabecalho` e `registro = encerramento` são proveniência e custo.
"""
import json
import re
import sys
from pathlib import Path

for _fluxo in (sys.stdout, sys.stderr):  # console do Windows em cp1252: saída sempre em UTF-8
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

RAIZ_INSTRUMENTO = Path(__file__).resolve().parents[1]
RAIZ_MBA = RAIZ_INSTRUMENTO.parent

# id: A-H1-001 · B-G2-004 · C-H7-012 (o id não carrega a execução, por desenho)
RE_ID = re.compile(r"\b([ABC])-(H\d{1,2}|G\d)-(\d{3})\b")
# nome de arquivo de evidência derivado do id: <id>.png, <id>.elemento.png, <id>.1.png, <id>.snapshot.txt
# e também com sufixo de letra logo após o id (<id>b.1.png), que a coleta de 21 a 23/09/2026 produziu
RE_ARQUIVO_EVIDENCIA = re.compile(r"\b[ABC]-(?:H\d{1,2}|G\d)-\d{3}[a-z]?(?:\.[\w-]+)*\.(?:png|jpg|jpeg|txt|md|json)\b")
RE_HEURISTICA = re.compile(r"^\s*H(\d{1,2})\b")

# campos do achado que a IA da unificação recebe (`protocolo/unificacao.md`, "Preparação da entrada", item 4)
CAMPOS_CEGOS_IA = [
    "heuristica", "localizacao", "registro_visual", "descricao_falha", "justificativa_violacao",
    "severidade", "severidade_rotulo", "justificativa_severidade", "sugestao_correcao",
]

# identificador de achado unificado: U001, U002, … (G### é dos grupos de heurísticas do Formato B)
RE_UNIFICADO = re.compile(r"^U\d{3,}$")
RE_CHAVE = re.compile(r"^K\d{3,}$")

# colunas da trilha de decisões, na ordem declarada (`protocolo/analise.md` §4)
COLUNAS_TRILHA = [
    "chave", "id", "formato", "execucao", "chamada", "heuristica", "severidade_ia",
    "achado_unificado", "classificacao", "severidade_pesquisador", "elemento", "pontos_manifestacao",
    "observacao",
]
# colunas de texto livre: sempre entre aspas duplas no CSV
COLUNAS_LIVRES = {"elemento", "pontos_manifestacao", "observacao"}

DOMINIOS = {"classificacao": ["defeito", "falso_positivo"]}
SEVERIDADES_PESQUISADOR = [1, 2, 3, 4]

GRUPOS_B = {"G1": ["H1", "H5", "H9"], "G2": ["H2", "H4", "H8"], "G3": ["H3", "H7"], "G4": ["H6", "H10"]}


def falhar(msg, codigo=1):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(codigo)


def ler_json(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def gravar_json(caminho, dado):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dado, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def ler_jsonl(caminho):
    """Devolve (cabecalho, achados, encerramento). Falha se faltar cabeçalho ou encerramento."""
    cab = enc = None
    achados = []
    with open(caminho, encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            linha = linha.strip()
            if not linha:
                continue
            try:
                obj = json.loads(linha)
            except json.JSONDecodeError as e:
                falhar(f"{caminho}: linha {n} não parseia como JSON ({e})")
            reg = obj.get("registro")
            if reg == "cabecalho":
                cab = obj
            elif reg == "encerramento":
                enc = obj
            elif reg in (None, "achado"):
                # o campo é opcional nos arquivos da coleta de 21 a 23/09/2026: as skills mandavam
                # acrescentar só formato, id e fora_do_escopo, e o orquestrador de A o gravou em duas
                # das três execuções. As duas formas valem.
                achados.append(obj)
            else:
                falhar(f"{caminho}: linha {n} com registro desconhecido '{reg}'")
    if cab is None:
        falhar(f"{caminho}: sem registro de cabeçalho")
    if enc is None:
        falhar(f"{caminho}: sem registro de encerramento")
    return cab, achados, enc


def partes_id(id_):
    """'A-H1-001' -> ('A', 'H1', 1). Falha se o id não segue a convenção."""
    m = RE_ID.fullmatch(id_ or "")
    if not m:
        falhar(f"id fora da convenção: {id_!r}")
    return m.group(1), m.group(2), int(m.group(3))


def chamada_do_id(id_):
    """`chamada` deriva do id: H<k> em A, G<n> em B, 'unica' em C (`analise.md` §4)."""
    formato, meio, _ = partes_id(id_)
    return "unica" if formato == "C" else meio


def chave_ordem_id(id_):
    """Ordem natural do id: formato, número da chamada, sequência. A-H2-001 < A-H10-001."""
    formato, meio, seq = partes_id(id_)
    return (formato, int(meio[1:]), seq)


def codigo_heuristica(texto):
    """'H1 — Visibilidade do status do sistema' -> 'H1'."""
    m = RE_HEURISTICA.match(texto or "")
    if not m:
        falhar(f"heurística fora do padrão 'H<n> — nome': {texto!r}")
    return f"H{int(m.group(1))}"


def numero_heuristica(texto):
    return int(codigo_heuristica(texto)[1:])


def formatar_chave(n, largura):
    return f"K{n:0{largura}d}"


def largura_chaves(total):
    return max(3, len(str(total)))


def desvio_padrao_amostral(valores):
    """Desvio-padrão amostral (n − 1). Devolve None com menos de dois valores."""
    v = [float(x) for x in valores]
    if len(v) < 2:
        return None
    m = sum(v) / len(v)
    return (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5


def media(valores):
    v = [float(x) for x in valores]
    return sum(v) / len(v) if v else None
