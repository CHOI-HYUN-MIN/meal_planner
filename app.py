import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="일주일 식단 추천기", page_icon="🍽️")

st.title("🍱 일주일 식단 추천 앱")
st.write("지난 주에 먹은 음식과 냉장고 재료를 바탕으로 새로운 식단을 추천해드려요!")

uploaded_file = st.file_uploader("📁 음식/레시피 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 🍳 음식 이름을 키로 하여 재료와 만드는 법을 함께 저장
    recipe_db = {
        row["음식이름"]: {
            "재료": [i.strip() for i in str(row["재료"]).split(",")],
            "레시피": row["만드는법"] if "만드는법" in row and pd.notna(row["만드는법"]) else "설명 없음"
        }
        for _, row in df.iterrows()
    }

    all_meals = list(recipe_db.keys())

    past_input = st.text_input("📝 지난 일주일 동안 먹은 음식 (쉼표로 구분)", placeholder="예: 볶음밥,오므라이스")
    fridge_input = st.text_input("🧊 냉장고에 있는 재료 (쉼표로 구분)", placeholder="예: 감자,고기,양파")

    if st.button("🍽️ 식단 추천 받기"):
        if not past_input or not fridge_input:
            st.warning("지난 식사와 냉장고 재료를 모두 입력해주세요.")
        else:
            past_meals = [x.strip() for x in past_input.split(",") if x.strip()]
            fridge_ingredients = set(x.strip() for x in fridge_input.split(",") if x.strip())

            available_meals = list(set(all_meals) - set(past_meals))
            if len(available_meals) < 7:
                st.warning("⚠️ 겹치지 않는 음식이 7개보다 적습니다. 가능한 만큼만 추천합니다.")
            next_meals = random.sample(available_meals, min(7, len(available_meals)))

            st.subheader("📆 다음 주 식단 추천")
            missing_ingredients = set()
            for meal in next_meals:
                st.markdown(f"### 🍽️ {meal}")
                meal_info = recipe_db.get(meal, {})
                ingredients = meal_info.get("재료", [])
                recipe_text = meal_info.get("레시피", "레시피 없음")

                st.write("**재료:**", ", ".join(ingredients))
                st.write("**간단한 만드는 법:**", recipe_text)  # 👈 레시피 출력 추가

                for item in ingredients:
                    if item not in fridge_ingredients:
                        missing_ingredients.add(item)

            st.subheader("🧾 부족한 재료")
            if missing_ingredients:
                st.error("필요한 재료: " + ", ".join(missing_ingredients))
            else:
                st.success("모든 재료가 냉장고에 있습니다!")
