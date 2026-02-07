from deep_translator import GoogleTranslator

def tr_to_en(text):
    return GoogleTranslator(source="tr", target="en").translate(text)

if __name__ == "__main__":
    src = input("Türkçe metni gir: ")
    print("İngilizce:", tr_to_en(src))