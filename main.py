import streamlit as st
from openai import OpenAI


# OpenAI API 키 설정
#OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(openai_api_key=st.secrets["OPENAI_API_KEY"])

def generate_questions(content, category, difficulty, num_questions):
    prompt = f"""- 종류: {category}
    - 난이도: {difficulty}
    - 문제수: {num_questions}
    - 지문 : {content} """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """한국의 내신 유형에 맞는 국어 문제를 생성하는 툴 생성

문제를 제작하기 위해 알아야 하는 조건
1. 만들어야 되는 문제의 주제(문학(시), 문학(소설), 비문학, 문법 중 선택)
2. 내신 범위의 지문 제시
3. 난이도 정하기(전국 단위로 고3이 풀었을 때, 정답률이 얼마나 나올 지 0~100% 까지 중 선택하기(숫자가 작을수록 어려운 문제임을 의미함))

문제의 유형(모두 객관식)
-문학(시)
1. 표현상의 특징 문제: 이 시에 사용된 표현법을 맞추는 문제
2~4. 시어/시구 문제: 시 안의 시어 혹은 시구가 어떤 뜻을 갖는지 맞추는 문제
5. 보기 문제: 시와 관련된 보기를 준 후, 보기를 참고하여 시에 관련된 일치/불일치 판단 문제

-문학(소설)
1. 표현상의 특징 문제: 시와 동일
2~3 내용일치 문제
4. 단어의 의미 해석 문제
5. 보기 문제

-비문학
1-2. 내용 일치 문제
3-5 적용 문제: 지문과 관련된 예시를 보기로 든 후, 그 예시의 정보를 분석하는 문제

-문법
국어 문법에 관련된 일치/불일치 문제

난이도에 관련한 내용은 무엇을 뜻하는지 첫 채팅에 설명

문제의 객관식은 오지선다형, 문제 생성 시 문제 위에 내신 범위의 지문을 필수적으로 포함하고, 단어의 의미를 묻는 문제의 경우 해당하는 단어에 강조 표시

보기는 시에 대한 주제를 설명하는데, 시인의 환경과 같은 외부적 요인을 포함해 3줄 정도로 만들어줘

객관식 예시
다음 중 사용된 표현법으로 적절하지 않은 것은?

1. 대조법
2. 의인법
3. 점층법
4. 직유법
5. 반어법

표현법 문제의 경우, 어떤한 방법을 써서 시 안에서어떠한 의미를 갖는다라는 형식으로 만들어줘. 어디에 이러한 표현법이 있다의 형식이 아니라, 그 표현법을 이용함을 통해 나타난 정서

문제 다 생성 후, 약 10줄 띄우고, 문제의 답과 해설도 작성

지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함
지문은 무조건적으로 포함

지문은 무조건적으로 포함
지문은 무조건적으로 포함
"""},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
    )

    return response.choices[0].message.content

# Streamlit UI 구성
st.title("내신용 국어 문제 생성기")
st.markdown("""### 세상에 없는 문제를 만들어 드립니다.

made by MSKoo""")

# 종류 선택
category = st.selectbox("종류", ["문학(시)", "문학(소설,수필)", "비문학", "문법"])

# 난이도 입력
difficulty = st.number_input("난이도 (0~100) 입력", min_value=0, max_value=100, step=1, value=50)
st.markdown("""0에 가까울수록 어렵다.""")

# 문제 수 입력
num_questions = st.number_input("문제 수 (1~5) 입력", min_value=1, max_value=5, step=1, value=5)

# 내용 입력
content = st.text_area("지문을 입력하세요", height=250)


# 문제 생성 버튼
if st.button("문제 생성"):
    if not content.strip():
        st.error("내용을 입력해주세요.")
    else:
        with st.spinner("문제를 생성하는 중..."):
            questions = generate_questions(content, category, difficulty, num_questions)
            st.subheader("생성된 문제")
            st.write(questions)
