import streamlit as st
import requests

# Configure the Streamlit page
st.set_page_config(page_title="🍽 Recipe Finder", layout="centered")

# App title and subheading
st.title("🍽 Recipe Finder")
st.subheader("Find delicious meals using TheMealDB API")

# --- Search Options ---
search_type = st.selectbox("Search by", ["Ingredient", "Meal Name", "Category"])
query = st.text_input(f"Enter {search_type.lower()}")

# --- Handle Search ---
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
            for meal in data["meals"][:5]:  # Show up to 5 meals
                st.markdown("---")
                st.subheader(meal["strMeal"])
                st.image(meal["strMealThumb"], use_column_width=True)

                # If user searched by Meal Name, full info already available
                if search_type == "Meal Name":
                    instructions = meal.get("strInstructions", "No instructions available.")
                    youtube = meal.get("strYoutube", "")
                    st.markdown("*Instructions:*")
                    st.write(instructions)

                    st.markdown("*Ingredients:*")
                    for i in range(1, 21):
                        ing = meal.get(f"strIngredient{i}")
                        measure = meal.get(f"strMeasure{i}")
                        if ing and ing.strip():
                            st.write(f"- {ing} ({measure})")

                    if youtube:
                        st.markdown("*Watch on YouTube:*")
                        st.video(youtube)

                else:
                    # For Ingredient or Category search, fetch full recipe details
                    with st.expander("View full recipe"):
                        meal_id = meal["idMeal"]
                        detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
                        detail_response = requests.get(detail_url)
                        full = detail_response.json()["meals"][0]
                        st.write("**Instructions:**")
                        st.write(full.get("strInstructions", "No instructions available."))

                        st.write("**Ingredients:**")
                        for i in range(1, 21):
                            ing = full.get(f"strIngredient{i}")
                            measure = full.get(f"strMeasure{i}")
                            if ing and ing.strip():
                                st.write(f"- {ing} ({measure})")

                        if full.get("strYoutube"):
                            st.markdown("*Watch on YouTube:*")
                            st.video(full["strYoutube"])

    except requests.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
