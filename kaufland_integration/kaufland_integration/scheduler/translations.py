import frappe


class translations:
    def add_translations(self, translations_list):

        for items in translations_list:
            translation = frappe.new_doc("Translation")
            translation.update(items)
            translation.insert()
        print(f"* All Translations installed for PL")

            
    def delete_translations(self, translations_list):
        for items in translations_list:
            translation = frappe.get_doc("Translation",items)
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