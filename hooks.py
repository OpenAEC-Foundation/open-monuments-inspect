app_name = "monuments_inspect"
app_title = "Open-Monuments Inspect"
app_publisher = "OpenAEC Foundation"
app_description = "NEN 2767 conditiemeting, ERM-gebrekregistratie en thermografische inspectie voor monumenten."
app_email = "info@openaec.org"
app_license = "lgpl-3.0"
app_version = "0.1.0"

required_apps = ["frappe", "erpnext", "monuments_core"]

hide_in_desk = 1

fixtures = [
    {
        "dt": "Role",
        "filters": [["role_name", "in", ["Inspecteur"]]],
    },
]

# NEN 2767 IxO-matrix scoring wordt uitgevoerd via lib/nen2767
# Frappe server-side: roept de Python library aan bij opslaan van Bevinding
doc_events = {
    "Bevinding": {
        "before_save": "monuments_inspect.monuments_inspect.doctype.bevinding.bevinding.bereken_conditiescore",
    },
    "ThermografischeInspectie": {
        "before_save": "monuments_inspect.monuments_inspect.doctype.thermografische_inspectie.thermografische_inspectie.bereken_delta_t",
    },
}

app_documentation = "https://github.com/OpenAEC-Foundation/Open-Monuments/tree/main/apps/inspect"
