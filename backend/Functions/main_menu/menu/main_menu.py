from backend.Functions.main_menu.menu_phone.menu_phone import connect_sms_phone
from backend.Functions.main_menu.translate.translate import translations, select_language


def about_us(lang):
    print(translations[lang]['AboutUs'])
    input(translations[lang]['BackToMenu'])


def see_course_and_change(lang):
    print(translations[lang]['CourseInfo'])
    input(translations[lang]['BackToMenu'])


def change_pin(lang):
    print(translations[lang]['ChangePin'])
    input(translations[lang]['BackToMenu'])






def main_menu():
    lang = select_language()

    while True:
        data = translations[lang]
        print(f"\n{data['LanguageWelcome']}")
        print(data['ChooseLanguage'])

        for item in data['MenuOption']:
            print(item)

        choice_m = input(data['PromptOption']).strip()

        if not choice_m.isdigit():
            print(data['InvalidOption'])
            continue

        choice_m = int(choice_m)

        if choice_m == 1:
            about_us(lang)
        elif choice_m == 2:
            see_course_and_change(lang)
        elif choice_m == 3:
            change_pin(lang)
        elif choice_m == 4:
            tranzactions(lang)
        elif choice_m == 5:
            connect_sms_phone(lang)
        elif choice_m == 6:
            lang = select_language()
        elif choice_m == 7:
            print(data['Exit'])
            break
        else:
            print(data['InvalidOptionRange'])


if __name__ == "__main__":
    main_menu()


