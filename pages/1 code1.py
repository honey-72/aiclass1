import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "AIzaSyDx9hbv30XZRZNNvXUVR9t1PIrLNXCATLs"


# 콘텐츠 생성 함수
def try_generate_content(api_key, prompt):
    # API 키 설정
    genai.configure(api_key=api_key)
    
    # 모델 설정
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config={
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    )
    
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 예외 발생 시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# Streamlit 앱 설정
st.title("생물 분류 정보 제공 앱")
st.write("생물 이름을 입력하면 그 생물의 분류 정보를 알려드립니다. 🐾")

# 생물 이름 입력받기
creature_name = st.text_input("생물 이름을 입력하세요")

if creature_name:
    prompt = f"생물 이름: {creature_name}\n이 생물의 분류 정보를 설명해줘."
    content = try_generate_content(api_key, prompt)
    
    if content:
        st.markdown(to_markdown(content))
    else:
        st.write("정보를 가져오는 데 실패했습니다. 나중에 다시 시도해주세요.")
