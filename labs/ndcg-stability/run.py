#!/usr/bin/env python3
"""Lab ndcg-stability: estabilidade da avaliação offline entre condições.

Uso:
  python run.py --list-panel   # imprime as condições do painel (não precisa de dependências)
  python run.py --download     # baixa o MovieLens 100K para data/
  python run.py --reference    # tarefa 2: roda só a condição de referência
  python run.py --panel        # tarefa 3: roda o painel completo
"""
import argparse
import itertools
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"        # ignorado pelo git
OUT = HERE / "outputs"      # ignorado pelo git
ML100K_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"  # a verificar se continua válida

SPLITS = ["random_80_20", "leave_last_out", "temporal_global"]
SEEDS = [0, 1, 2]
ALGOS = ["popularity", "item_knn", "svd"]
REFERENCE = {"split": "random_80_20", "seed": 0}
K = 10


def panel():
    """Condições do painel: combinações de divisão e semente."""
    for split, seed in itertools.product(SPLITS, SEEDS):
        yield {"split": split, "seed": seed}


def download():
    DATA.mkdir(exist_ok=True)
    target = DATA / "ml-100k.zip"
    if not target.exists():
        print(f"baixando {ML100K_URL}")
        urllib.request.urlretrieve(ML100K_URL, target)
    with zipfile.ZipFile(target) as z:
        z.extractall(DATA)
    print(f"ok: {DATA / 'ml-100k'}")


# --- Tarefa 2: implementar as funções abaixo -------------------------------------------

def load_ratings():
    """Retorna um DataFrame com colunas user, item, rating, timestamp (de data/ml-100k/u.data)."""
    raise NotImplementedError("tarefa 2")


def make_split(ratings, split, seed):
    """Retorna (train, test) conforme `split` e `seed`. Documente aqui o que conta como relevante."""
    raise NotImplementedError("tarefa 2")


def recommend(algo, train, users, seed, k=K):
    """Retorna {user: [item, ...]} com os top-k itens não vistos, para cada algoritmo em ALGOS."""
    raise NotImplementedError("tarefa 2")


def ndcg_at_k(recs, test, k=K):
    """nDCG@k médio sobre os usuários presentes em `test`."""
    raise NotImplementedError("tarefa 2")


def run_condition(condition):
    ratings = load_ratings()
    train, test = make_split(ratings, condition["split"], condition["seed"])
    users = sorted(test["user"].unique())
    rows, lists = [], {}
    for algo in ALGOS:
        recs = recommend(algo, train, users, condition["seed"])
        lists[algo] = recs
        rows.append({**condition, "algo": algo, "ndcg@10": ndcg_at_k(recs, test)})
    return rows, lists


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list-panel", action="store_true")
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--reference", action="store_true")
    ap.add_argument("--panel", action="store_true")
    args = ap.parse_args()

    if args.list_panel:
        conds = list(panel())
        print(f"{len(conds)} condições x {len(ALGOS)} algoritmos = {len(conds) * len(ALGOS)} execuções")
        for c in conds:
            print(f"  split={c['split']:<16} seed={c['seed']}")
        print(f"referência: {REFERENCE}")
    elif args.download:
        download()
    elif args.reference or args.panel:
        OUT.mkdir(exist_ok=True)
        conds = [REFERENCE] if args.reference else list(panel())
        try:
            for c in conds:
                rows, _ = run_condition(c)
                for r in rows:
                    print(r)
        except NotImplementedError as e:
            raise SystemExit(f"falta implementar: {e} (veja as funções em run.py)")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
