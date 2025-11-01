import json
from pathlib import Path
from typing import Dict, List, Any


def write_results_to_json(results: List[Dict[str, Any]], json_path: Path):
    """
    Écrit la liste complète des résultats d'évaluation dans un seul fichier JSON.

    Args:
        results: La liste des dictionnaires de résultats (de make_n_evaluations).
        json_path: Le chemin du fichier JSON de sortie.
    """

    json_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        json_path.write_text(
            json.dumps(results, indent=4, ensure_ascii=False), encoding="utf-8"
        )

        print(
            f"✅ {len(results)} évaluations écrites dans '{json_path}' au format JSON."
        )

    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier JSON : {e}")
