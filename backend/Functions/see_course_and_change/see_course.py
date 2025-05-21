from backend.Functions.main_menu.translate.translate import translations


def see_course_and_change(lang):
    print(translations[lang]['CourseInfo'])
    input(translations[lang]['BackToMenu'])