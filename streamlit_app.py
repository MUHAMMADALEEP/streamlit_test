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

# --- Initialize session state to store ratings and comments ---
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

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

                # Get meal details if not full
                if search_type == "Meal Name":
                    full = meal
                else:
                    detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal['idMeal']}"
                    detail_response = requests.get(detail_url)
                    full = detail_response.json()["meals"][0]

                # Display Area (Cuisine type)
                cuisine = full.get("strArea", "Unknown")
                st.markdown(f"**Cuisine Type:** {cuisine}")

                # Instructions
                with st.expander("📖 View Instructions & Ingredients"):
                    st.markdown("**Instructions:**")
                    st.write(full.get("strInstructions", "No instructions available."))

                    st.markdown("**Ingredients:**")
                    for i in range(1, 21):
                        ing = full.get(f"strIngredient{i}")
                        measure = full.get(f"strMeasure{i}")
                        if ing and ing.strip():
                            st.write(f"- {ing} ({measure})")

                    if full.get("strYoutube"):
                        st.markdown("*🎥 Watch on YouTube:*")
                        st.video(full["strYoutube"])

                # Feedback section
                with st.expander("⭐ Rate & Comment this recipe"):
                    key_prefix = meal["idMeal"]
                    rating = st.slider(f"Rate this recipe (1-5 stars)", 1, 5, key=f"rate_{key_prefix}")
                    comment = st.text_area("Leave a comment:", key=f"comment_{key_prefix}")
                    if st.button("Submit Feedback", key=f"submit_{key_prefix}"):
                        st.session_state.feedback[key_prefix] = {
                            "rating": rating,
                            "comment": comment
                        }
                        st.success("Feedback submitted!")

                # Show feedback if already submitted
                if meal["idMeal"] in st.session_state.feedback:
                    feedback = st.session_state.feedback[meal["idMeal"]]
                    st.markdown("### ✅ User Feedback")
                    st.write(f"**Rating:** {'⭐' * feedback['rating']}")
                    st.write(f"**Comment:** {feedback['comment']}")

    except requests.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
