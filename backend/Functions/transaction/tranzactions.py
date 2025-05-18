from backend.Functions.main_menu.translate.translate import translations


def tranzactions(lang):
    print(translations[lang]['Transactions'])
    input(translations[lang]['BackToMenu'])
