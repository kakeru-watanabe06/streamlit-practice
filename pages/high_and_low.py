import streamlit as st
import random
import os
from PIL import Image

# ====== 初期設定 ======
st.set_page_config(page_title="High and Low", page_icon="🃏", layout="centered")
init_money = 100


# トランプ画像を読み込む関数
@st.cache_data
def load_cards(path="cards"):
    suits = ["S", "H", "D", "C"]  # スペード, ハート, ダイヤ, クラブ
    ranks = ["A"] + [str(i) for i in range(2, 11)] + ["J", "Q", "K"]
    cards = {}
    for s in suits:
        for r in ranks:
            filename = f"{r}{s}.png"  # 例: "AS.png"
            img = Image.open(os.path.join(path, filename)).resize((100, 145))
            cards[f"{r}{s}"] = img
    return cards, ranks

import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont
import os

# --------- カード生成（シンプル版） ---------
def generate_cards(path="cards"):
    os.makedirs(path, exist_ok=True)
    suits = {"S":"♠","H":"♥","D":"♦","C":"♣"}
    ranks = ["A"] + [str(i) for i in range(2,11)] + ["J","Q","K"]
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)

    cards = {}
    for s_symbol, suit in suits.items():
        for r in ranks:
            filename = f"{r}{s_symbol}.png"
            filepath = os.path.join(path, filename)
            if not os.path.exists(filepath):
                img = Image.new("RGB", (150,200), "white")
                draw = ImageDraw.Draw(img)
                draw.rectangle([0,0,149,199], outline="black", width=3)
                color = "red" if s_symbol in ["H","D"] else "black"
                draw.text((10,10), r, font=font, fill=color)
                draw.text((100,150), suit, font=font, fill=color)
                img.save(filepath)
            cards[f"{r}{s_symbol}"] = filepath
    return cards

def card_value(rank):
    if rank == "A": return 99
    if rank == "J": return 11
    if rank == "Q": return 12
    if rank == "K": return 13
    return int(rank)

# --------- 初期化 ---------
if "deck" not in st.session_state:
    st.session_state.cards = generate_cards()
    st.session_state.deck = list(st.session_state.cards.keys())
    random.shuffle(st.session_state.deck)
    st.session_state.current = st.session_state.deck.pop()
    st.session_state.next = None
    st.session_state.money = init_money
    st.session_state.message = "High or Low ?"
    st.session_state.pre_bet = 10


# --------- UI ---------
st.title("🃏 High and Low Game!!")
st.write("カードの数字が次に出るカードより高いか低いかを当ててください。")
st.write("Aは最も高く、2が最も低いです。")
st.write("掛け金を設定し、当たれば掛け金の2倍、外れれば掛け金を失います。")
st.write("⚠️ダブルクリックしないと反応しないバグがありますが放置してます。")

col1, col2 = st.columns(2)
col1.image(st.session_state.cards[st.session_state.current], caption="現在のカード")
if st.session_state.next:
    col2.image(st.session_state.cards[st.session_state.next], caption="次のカード")
else:
    col2.image(Image.new("RGB", (150,200), (0,100,0)), caption="???")

st.info(st.session_state.message)
st.markdown(f"### 所持金: {st.session_state.money} 円")

# ----------掛け金設定----------
if st.session_state.money <= 0:
    st.error("💥 所持金がなくなりました！ゲームオーバー")
    st.stop()
if st.session_state.money < st.session_state.pre_bet:
    st.session_state.pre_bet = st.session_state.money
bet = st.number_input("掛け金を設定してください", min_value=1, max_value=st.session_state.money, value=st.session_state.pre_bet, step=1)
if st.button("掛け金を設定"):
    if bet > st.session_state.money:
        st.error("❌ 掛け金が所持金を超えています！")
    else:
        # st.session_state.money -= bet # ここで引くと破産する
        st.session_state.score = 0
        st.session_state.message = f"掛け金 {bet} を設定しました。High or Low ?"

# --------- ボタン ---------
colA, colB, colC = st.columns(3)

with colA:
    if st.button("🔼 High") and not st.session_state.next:
        st.session_state.next = st.session_state.deck.pop()
        cur_val = card_value(st.session_state.current[:-1])
        next_val = card_value(st.session_state.next[:-1])
        if next_val > cur_val:
            st.session_state.message = "✅ Correct! ➡ Click Next"
            st.session_state.money += bet * 2
            st.session_state.pre_bet = bet
        elif next_val == cur_val:
            st.session_state.message = f"➖ Same! ({st.session_state.next}) ➡ Click Next"
            # 所持金変動なし
            st.session_state.pre_bet = bet
        else:
            st.session_state.message = f"❌ Wrong! ({st.session_state.next}) ➡ Click Next"
            st.session_state.money -= bet
            st.session_state.pre_bet = bet

with colB:
    if st.button("🔽 Low") and not st.session_state.next:
        st.session_state.next = st.session_state.deck.pop()
        cur_val = card_value(st.session_state.current[:-1])
        next_val = card_value(st.session_state.next[:-1])
        if next_val < cur_val:
            st.session_state.message = "✅ Correct! ➡ Click Next"
            st.session_state.money += bet * 2
            st.session_state.pre_bet = bet
        elif next_val == cur_val:
            st.session_state.message = f"➖ Same! ({st.session_state.next}) ➡ Click Next"
            # 所持金変動なし
            st.session_state.pre_bet = bet
        else:
            st.session_state.message = f"❌ Wrong! ({st.session_state.next}) ➡ Click Next"
            st.session_state.money -= bet
            st.session_state.pre_bet = bet

with colC:
    if st.button("➡ Next") and st.session_state.next:
        st.session_state.current = st.session_state.next
        st.session_state.next = None
        st.session_state.message = "High or Low ?"

# --------- ゲーム終了 ---------
if not st.session_state.deck:
    st.warning("🎉 カードがなくなりました！ゲーム終了")
