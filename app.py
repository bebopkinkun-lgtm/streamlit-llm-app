from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# APIキーの確認
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。")
    st.stop()

# LLM初期化
try:
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
except Exception as e:
    st.error(f"LLMの初期化中にエラーが発生しました: {e}")
    st.stop()

# タイトルと説明
st.title("ファッションと栄養のアドバイス")
st.write("##### 動作モード1: ファッションアドバイス")
st.write("フォーマル・カジュアルなど、場面に応じたコーディネートを提案します。")
st.write("##### 動作モード2: 栄養アドバイス")
st.write("食生活や健康に関する質問に、栄養士の視点で回答します。")

# モード選択
selected_item = st.radio(
    "動作モードを選択してください。",
    ["ファッションアドバイス", "栄養アドバイス"]
)

st.divider()

# ユーザー入力
user_query = st.text_input("質問を入力してください。")

if st.button("実行"):
    st.divider()

    if user_query:
        # モードに応じたSystemMessageを設定
        if selected_item == "ファッションアドバイス":
            system_prompt = """あなたは経験豊富なファッションスタイリストです。
            ユーザーからの質問に対して、具体的で実用的なファッションアドバイスを日本語で提供してください。
            場面、季節、体型、予算なども考慮したアドバイスをお願いします。"""
        else:
            system_prompt = """あなたは資格を持つ栄養士です。
            ユーザーからの質問に対して、科学的根拠に基づいた栄養アドバイスを日本語で提供してください。
            健康状態、年齢、活動レベルなども考慮したアドバイスをお願いします。"""

        # LLMへの問い合わせ
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]

        try:
            with st.spinner("回答を生成中..."):
                result = llm.invoke(messages)
            st.write("### 回答:")
            st.write(result.content)

        except ImportError:
            st.error("必要なライブラリがインストールされていません。requirements.txtを確認してください。")
        except Exception as e:
            st.error(f"LLMの応答中にエラーが発生しました: {str(e)}")
            st.info("OpenAI APIキーが正しく設定されているか、.envファイルを確認してください。")

    else:
        st.error("質問を入力してから「実行」ボタンを押してください。")