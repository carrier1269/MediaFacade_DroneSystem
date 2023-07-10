from googletrans import Translator

# Translator 클래스 객체 선언 (translator라는 변수명은 마음대로 정해주면 됨)
translator = Translator()

def en_to_kr(prompt):
    return translator.translate(prompt).text