from backend.Functions.main_menu.translate.translate import translations


def connect_sms_phone(lang):
    print(translations[lang]['ConnectSMS'])
    input(translations[lang]['BackToMenu'])
    