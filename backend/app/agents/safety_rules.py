def triage_hint(place_type: str, count: int, radius_m: int) -> str:
    pt = (place_type or "").lower().strip()
    if pt in {"hospital"}:
        return "En cas d'urgence vitale, appelle les services d'urgence locaux immédiatement."
    if pt in {"pharmacy"} and count == 0:
        return f"Aucun résultat dans {radius_m}m. Élargis le rayon ou essaye un autre quartier."
    if count == 0:
        return "Aucun résultat. Change le type ou élargis le rayon."
    return "Vérifie les horaires avant de te déplacer."
