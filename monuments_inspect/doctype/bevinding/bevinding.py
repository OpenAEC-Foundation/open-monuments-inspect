import frappe
from frappe.model.document import Document
import sys
import os

# lib/nen2767 staat in de repo root — voeg toe aan path als nog niet aanwezig
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..'))
NEN_LIB = os.path.join(REPO_ROOT, 'lib')
if NEN_LIB not in sys.path:
    sys.path.insert(0, NEN_LIB)


class Bevinding(Document):
    pass


def bereken_conditiescore(doc, method=None):
    """
    Bereken de NEN 2767 conditiescore op basis van intensiteit en omvang.
    Wordt aangeroepen via hooks.py doc_events["Bevinding"]["before_save"].
    """
    if not doc.intensiteit or not doc.omvang:
        return

    try:
        from nen2767.scoring import intensity_extent_to_score

        # Intensiteit: "1 - Gering" -> 1
        intensiteit = int(str(doc.intensiteit).split(' - ')[0].strip())
        # Omvang: "3 - 10-30%" -> 3
        omvang = int(str(doc.omvang).split(' - ')[0].strip())

        score = intensity_extent_to_score(intensiteit, omvang)
        doc.conditiescore = score

    except Exception as e:
        frappe.log_error(f"NEN 2767 scoring mislukt voor Bevinding {doc.name}: {e}")
