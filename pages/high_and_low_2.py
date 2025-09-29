import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from model.high_and_low import HighLowGame
import streamlit as st

def run_game_streamlit():
    st.title("High & Low Game")

    if "game" not in st.session_state:
        st.session_state.game = HighLowGame(chips=100)
        st.session_state.base_card = st.session_state.game.deck.pop()

    game = st.session_state.game

    if not game.deck:
        st.write("デッキがなくなりました。ゲーム終了！")
        st.write("履歴:", game.history)
        return

    if game.chips <= 0:
        st.write("チップがなくなりました。ゲーム終了！")
        st.write("履歴:", game.history)
        return

    base_card = st.session_state.base_card
    st.write(f"ベースカード: {base_card}")
    choice = st.selectbox("High or Low?", ["High", "Low"])
    bet = st.number_input("ベット額:", min_value=1, max_value=game.chips, value=10)

    if st.button("プレイ"):
        record = game.play_round(base_card, choice, bet)
        st.write(f"→ 出たカード: {record['result_card']}")
        st.write(f"→ 結果: {record['outcome']}, 残りチップ: {record['chips_after']}")

        if game.deck:
            st.session_state.base_card = game.deck.pop()
        else:
            st.session_state.base_card = None

        st.rerun()

    st.write(f"残りチップ: {game.chips}")
    st.write(f"残りデッキ数: {len(game.deck)}")

run_game_streamlit()

