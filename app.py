from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# APIキー設定（環境変数から取得）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 専門家タイプに応じたシステムメッセージを生成
def get_system_prompt(expert_type: str) -> str:
    if expert_type == "法律の専門家":
        return "あなたは経験豊富な法律の専門家です。法律の専門的観点から回答してください。"
    elif expert_type == "医療の専門家":
        return "あなたは信頼できる医療の専門家です。医学的観点から丁寧に回答してください。"
    elif expert_type == "ビジネスコンサルタント":
        return "あなたは敏腕のビジネスコンサルタントです。ビジネス改善の観点でアドバイスしてください。"
    else:
        return "あなたは賢明なアシスタントです。"

# 入力と専門家タイプを元に LLM 応答を取得
def get_llm_response(user_input: str, expert_type: str) -> str:
    chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7, model="gpt-3.5-turbo")
    system_prompt = get_system_prompt(expert_type)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    
    response = chat(messages)
    return response.content

# Streamlit UI
st.title("専門家AIアシスタント ✨")

st.markdown("""
このアプリでは、入力した質問に対して、選択した分野の専門家になりきったAIが回答します。  
以下の手順で操作してください：

1. 下のラジオボタンで専門家の種類を選択  
2. 入力欄に質問を入力  
3. 「送信」ボタンを押すと、AIが専門家として回答します
""")

# ラジオボタンで専門家の種類を選ぶ
expert_type = st.radio(
    "専門家の種類を選んでください：",
    ("法律の専門家", "医療の専門家", "ビジネスコンサルタント")
)

# 入力フォーム
user_input = st.text_area("質問を入力してください：")

if st.button("送信"):
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが考えています..."):
            response = get_llm_response(user_input, expert_type)
            st.success("AIの回答：")
            st.write(response)