import json

def load_translations():
    with open("translation.json", encoding="utf-8") as f:
        return json.load(f)

def choose_language():
    translations = load_translations()
    languages = list(translations.keys())

    print("Выберите язык:")
    for i, lang_code in enumerate(languages, start=1):
        welcome = translations[lang_code].get("LanguageWelcome") or translations[lang_code].get("ВыборЯзыка") or translations[lang_code].get("TilniTanlovi")
        print(f"{i}. [{lang_code.upper()}] — {welcome}")

    try:
        choice = int(input("Введите номер: ")) - 1
        if 0 <= choice < len(languages):
            selected_lang = languages[choice]
            return translations[selected_lang]
        else:
            print("Неверный номер. Попробуйте снова.")
    except ValueError:
        print("Введите число.")

    return None

if __name__ == "__main__":
    lang_data = choose_language()
    if lang_data:
        for key, value in lang_data.items():
            print(f"{key} -> {value}")
