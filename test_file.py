import json

def load_translations():
    with open("translations.json", encoding="utf-8") as f:
        return json.load(f)

def choose_language_numbered():
    translations = load_translations()

    lang_codes = list(translations.keys())

    print("\nВыберите язык:\n")
    for idx, code in enumerate(lang_codes, start=1):
        lang = translations[code]
        print(f"{idx}. [{code.upper()}] {lang['LanguageWelcome']} — {lang['ChooseLanguage']}")

    choice = input("\nВведите номер языка: ")

    try:
        index = int(choice) - 1
        if 0 <= index < len(lang_codes):
            selected_lang = lang_codes[index]
            print(f"\n✅ Вы выбрали: {translations[selected_lang]['LanguageWelcome']}")
            show_main_menu(selected_lang, translations)
        else:
            print("❌ Номер вне диапазона.")
    except ValueError:
        print("❌ Введите только цифру.")

def show_main_menu(lang_code, translations):
    """
Показываем основное меню в зависимости от выбранного языка
    """
    print("\nМеню:\n")
    menu_items = [
        "MenuOption1",  # О компании
        "MenuOption2",  # Просмотр курса
        "MenuOption3"   # Пополнение
    ]

    for idx, item in enumerate(menu_items, start=1):
        print(f"{idx}. {translations[lang_code].get(item, item)}")

if __name__ == "__main__":
    choose_language_numbered()
    