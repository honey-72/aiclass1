import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "AIzaSyDx9hbv30XZRZNNvXUVR9t1PIrLNXCATLs"

def try_generate_content(api_key, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
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
                                  ])
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

def get_country_location(country_name):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    country = world[world.name == country_name]
    if not country.empty:
        return country
    else:
        return None

st.title("국가의 판 구조와 판 변화 예측")
st.write("나라 이름을 입력하면 해당 나라가 속한 판 구조와 판의 변화에 대한 예측을 확인하고 지도를 볼 수 있습니다.")

country = st.text_input("나라 이름을 입력하세요")

if country:
    location = get_country_location(country)
    
    if location is not None:
        country_location = location.geometry.centroid.iloc[0].coords[:][0]
        m = folium.Map(location=[country_location[1], country_location[0]], zoom_start=4)
        folium.GeoJson(location.geometry).add_to(m)
        st_folium(m, width=700)
        
        prompt = f"{country}가 속한 판 구조와 판의 변화에 대해 설명해주세요."
        result = try_generate_content(api_key, prompt)
        
        if result:
            st.markdown(to_markdown(result))
        else:
            st.write("결과를 생성하는 데 실패했습니다. 다시 시도해주세요.")
    else:
        st.write(f"'{country}'에 대한 위치 정보를 찾을 수 없습니다.")
