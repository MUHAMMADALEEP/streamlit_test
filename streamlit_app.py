import streamlit as st
import requests
import random

st.set_page_config(page_title="🍽 Recipe Finder", layout="centered")

st.title("🍽 Recipe Finder")
st.subheader("Find delicious meals using TheMealDB API")

search_type = st.selectbox("Search by", ["Ingredient", "Meal Name", "Category"])
query = st.text_input(f"Enter {search_type.lower()}")

sample_comments = [
    "Absolutely delicious!",
    "My kids loved it!",
    "Easy to make and so tasty.",
    "Perfect for a weekend meal.",
    "Will definitely cook again!",
    "A bit spicy for my taste, but still good.",
    "Needed more seasoning.",
    "Tasted just like a restaurant dish!"
]

if st.button("Search") and query:
    if search_type == "Ingredient":
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={query}"
    elif search_type == "Meal Name":
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
    elif search_type == "Category":
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={query}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["meals"] is None:
            st.warning("No recipes found. Try something else!")
        else:
            for meal in data["meals"][:5]:
                st.markdown("---")
                st.subheader(meal["strMeal"])
                st.image(meal["strMealThumb"], use_column_width=True)

                if search_type == "Meal Name":
                    full = meal
                else:
                    meal_id = meal["idMeal"]
                    detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
                    detail_response = requests.get(detail_url)
                    full = detail_response.json()["meals"][0]

                cuisine = full.get("strArea", "Unknown")
                st.markdown(f"*Cuisine Type:* {cuisine}")

                rating = random.randint(3, 5)
                comments = random.sample(sample_comments, k=2)
                st.markdown(f"*Community Rating:* {'⭐' * rating} ({rating}/5)")
                st.markdown("*User Comments:*")
                for c in comments:
                    st.write(f"- {c}")

                with st.expander("📖 View Instructions & Ingredients"):
                    st.markdown("*Instructions:*")
                    st.write(full.get("strInstructions", "No instructions available."))

                    st.markdown("*Ingredients:*")
                    for i in range(1, 21):
                        ing = full.get(f"strIngredient{i}")
                        measure = full.get(f"strMeasure{i}")
                        if ing and ing.strip():
                            st.write(f"- {ing} ({measure})")

                    if full.get("strYoutube"):
                        st.markdown("🎥 Watch on YouTube:")
                        st.video(full["strYoutube"])

    except requests.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
