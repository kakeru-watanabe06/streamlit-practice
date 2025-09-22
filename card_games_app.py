import streamlit as st
st.title("簡易計算機能")
st.write("任意の二つの数字について四則演算の実行ができます。")

num1 = st.number_input("1つ目の数字を入力してください", value=0.0, step=0.1)
num2 = st.number_input("2つ目の数字を入力してください", value=0.0, step=0.1)
operation = st.selectbox("演算子を選択してください", ("+", "-", "*", "/"))
if st.button("計算実行"):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error: 0で割ることはできません"
    st.write(f"結果: {result}")