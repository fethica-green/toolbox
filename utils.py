# utils.py

import pandas as pd
import io
from datetime import datetime, date

def to_excel(df: pd.DataFrame) -> bytes:
    """
    Convertit un DataFrame en fichier Excel (XLSX) et renvoie les octets du fichier.
    Utile pour proposer un bouton de téléchargement via Streamlit.
    """
    output = io.BytesIO()
    # Utilisation de XlsxWriter par défaut
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    return output.getvalue()

def calculate_days(start_date, end_date) -> int:
    """
    Calcule le nombre de jours entre deux dates.
    - start_date et end_date peuvent être :
      • des str au format ISO ('YYYY-MM-DD' ou 'YYYY-MM-DD HH:MM:SS')
      • des objets datetime.datetime ou datetime.date
      • des pandas.Timestamp

    Renvoie un entier (peut être négatif si end_date < start_date).
    """
    # Normalisation en datetime.date
    def _to_date(d):
        if isinstance(d, date) and not isinstance(d, datetime):
            return d
        if isinstance(d, datetime):
            return d.date()
        if isinstance(d, str):
            # On gère ISO format
            try:
                return datetime.fromisoformat(d).date()
            except ValueError:
                raise ValueError(f"Format de date invalide : {d!r}")
        if hasattr(d, "to_pydatetime"):  # pandas.Timestamp
            return d.to_pydatetime().date()
        raise TypeError(f"Type non supporté pour une date : {type(d)}")

    d1 = _to_date(start_date)
    d2 = _to_date(end_date)
    return (d2 - d1).days
