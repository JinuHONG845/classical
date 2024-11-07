import streamlit as st
import openai
from typing import Dict
import json

def get_composer_info(composer_name: str, api_key: str) -> Dict[str, str]:
    """작곡가 정보를 OpenAI API를 통해 가져오는 함수"""
    
    # API 키 설정
    openai.api_key = api_key
    
    system_prompt = """
    당신은 클래식 음악 전문가입니다. 다음 작곡가에 대해 세 가지 측면에서 정보를 제공해주세요:
    1. 생애 (500자 이내)
    2. 주요 음악 작품 5개 (각 작품별 간단한 설명 포함)
    3. 각 주요 작품별 추천 명반 2개 (지휘자/연주자, 오케스트라, 발매연도 포함)
    
    JSON 형식으로 응답해주세요.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{composer_name}에 대한 정보를 제공해주세요."}
            ],
            response_format={ "type": "json_object" },
            max_tokens=4000,  # 토큰 제한 추가
            temperature=0.7
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")
        return None

def main():
    st.title("🎼 클래식 음악 탐험")
    st.write("작곡가의 이름을 입력하시면 상세 정보를 제공해드립니다.")
    
    # API 키 입력 필드 (비밀번호 형태로 표시)
    api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")
    
    if not api_key:
        st.warning("API 키를 입력해주세요.")
        return
        
    composer_name = st.text_input("작곡가 이름을 입력하세요 (예: 모차르트, 베토벤)")
    
    if composer_name and api_key:
        with st.spinner("정보를 가져오는 중입니다..."):
            info = get_composer_info(composer_name, api_key)
            
            if info:
                st.header(f"📚 {composer_name}의 생애")
                st.write(info["생애"])
                
                st.header("🎵 주요 작품")
                for work in info["주요_작품"]:
                    st.subheader(work["제목"])
                    st.write(work["설명"])
                    
                    st.write("추천 명반:")
                    for recording in work["추천_명반"]:
                        st.write(f"- {recording}")

if __name__ == "__main__":
    main() 