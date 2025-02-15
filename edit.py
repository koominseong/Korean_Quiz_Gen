import streamlit as st
import openai  # ✅ 최신 openai 라이브러리 사용
import os

# ✅ OpenAI API 키 설정 (KeyError 예외 처리)
try:
    api_key = st.secrets["openai"]["OPENAI_API_KEY"]
except KeyError:
    st.error("🚨 OpenAI API 키가 설정되지 않았습니다! `secrets.toml` 파일을 확인하세요.")
    st.stop()  # 앱 실행 중지

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# ✅ 최신 방식으로 API 키 설정
openai.api_key = api_key

# ✅ 문제 생성 함수
def generate_questions(content, category, difficulty, num_questions):
    prompt = f"""
    - 종류: {category}
    - 난이도: {difficulty} (정답률 기준, 숫자가 작을수록 어려운 문제)
    - 문제수: {num_questions}
    - 지문: {content}
    
    문제를 생성할 때 반드시 다음 사항을 준수하세요:
    1. 객관식 오지선다형 문제로 생성 (정확한 정답 포함).
    2. 문제의 유형은 {category}에 맞게 선택.
    3. 난이도를 고려하여 문제를 설계.
    4. 문제 생성 후, 지문을 다시 제공하고 문제의 정답 및 해설 포함.
    """

    try:
        response = client.Chat.Completions.create(
            model="gpt-4o",  # ✅ 최신 GPT-4o 모델 사용
            messages=[
                {"role": "system", "content": "국어 내신 문제 생성기"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )
        return response["choices"][0]["message"]["content"]
    
    except Exception as e:
        return f"🚨 오류 발생: {e}"

# ✅ Streamlit UI
st.title("📚 내신용 국어 문제 생성기")
st.markdown("#### ✨ 세상에 없는 문제를 만들어 드립니다! \n **Made by MSKoo**")

# ✅ 문제 설정 입력 UI
category = st.selectbox("📖 문제 종류", ["문학(시)", "문학(소설,수필)", "비문학", "문법"])
difficulty = st.slider("🎯 난이도 (정답률 %)", 0, 100, 50, help="0에 가까울수록 어려운 문제입니다.")
num_questions = st.slider("📝 문제 수", 1, 5, 3)
content = st.text_area("✏️ 지문을 입력하세요", height=250)

# ✅ 문제 생성 버튼
if st.button("🚀 문제 생성"):
    if not content.strip():
        st.warning("⚠️ 내용을 입력해주세요.")
    else:
        with st.spinner("🔄 문제를 생성하는 중..."):
            questions = generate_questions(content, category, difficulty, num_questions)
            st.subheader("📌 생성된 문제")
            st.write(questions)
