import frappe
from frappe.model.document import Document


class ThermografischeInspectie(Document):
    pass


def bereken_delta_t(doc, method=None):
    """
    Bereken ΔT en stel waarschuwing in als ΔT < 10 K (F-THERM-002).
    Wordt aangeroepen via hooks.py doc_events["ThermografischeInspectie"]["before_save"].
    """
    if doc.temperatuur_binnen is None or doc.temperatuur_buiten is None:
        return

    delta_t = abs(doc.temperatuur_binnen - doc.temperatuur_buiten)
    doc.delta_t = round(delta_t, 1)
    doc.delta_t_waarschuwing = 1 if delta_t < 10 else 0

    if doc.delta_t_waarschuwing:
        frappe.msgprint(
            f"Waarschuwing: ΔT = {delta_t:.1f} K is kleiner dan 10 K. "
            "De thermografische meting is mogelijk onbetrouwbaar (F-THERM-002).",
            indicator='orange',
            alert=True
        )
