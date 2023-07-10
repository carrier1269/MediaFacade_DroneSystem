from PyKakao import Karlo

def image_generator_karlo(prompt, kakao_api_key):
    api = Karlo(service_key = kakao_api_key)

    img_dict = api.text_to_image(prompt, 1)

    # 생성된 이미지 정보
    img_str = img_dict.get("images")[0].get('image')

    # base64 string을 이미지로 변환
    return api.string_to_image(base64_string = img_str, mode = 'RGBA')

    # 이미지 저장하기
    # img.save("./original.png")