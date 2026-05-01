import json
import os

SCORE_FILE = './data/scores.json'
MAX_SCORES = 5


def load_scores():
    # Se o arquivo não existe ainda, retorna lista vazia
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_score(new_score):
    scores = load_scores()
    scores.append(new_score)

    # Ordena do maior para o menor e mantém só os top 5
    scores = sorted(scores, reverse=True)[:MAX_SCORES]

    # Cria a pasta /data se não existir
    os.makedirs('./data', exist_ok=True)

    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f)

    return scores  # retorna a lista atualizada