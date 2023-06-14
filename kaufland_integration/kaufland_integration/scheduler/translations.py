import frappe


class translations:
    def add_translations(self, translations_list):
        translations = frappe.get_all("Translation", fields=["source_text"])
        for item in translations_list:
            if item not in translations:
                translation = frappe.get_doc({
                    "doctype": 'Translation',
                    "source_text": item["source_text"],
                    "language": item["language"],
                    "translated_text": item["translated_text"]
                })
                translation.insert()
        print(f"* All Translations installed for PL")

            
    def delete_translations(self, translations_list):
        translations = frappe.get_all("Translation", fields=["source_text"])
        for item in translations_list:
            if item in translations:
                translation = frappe.get_doc("Translation", item)
                frappe.db.delete("Translation", translation.name)
        frappe.clear_cache()
        print(f"* All Translations deleted")

            
    def get_translation_list(self):
        return [
            {
                "source_text": "Secret key",
                "language": "pl",
                "translated_text": "Sekretny klucz"
            },
            {
                "source_text": "Number of days back",
                "language": "pl",
                "translated_text": "Liczba dni wstecz"
            },
            {
                "source_text": "Kaufland Settings",
                "language": "pl",
                "translated_text": "Ustawienia Kaufland"
            }
        ]