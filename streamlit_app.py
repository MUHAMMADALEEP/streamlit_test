import streamlit as st
import requests

# Configure Streamlit
st.set_page_config(page_title="🍽 Recipe Finder with Real Ratings", layout="centered")

API_KEY = "8e111fe53e634d2e83ffabf11a102ae7"  # Your actual Spoonacular API key

st.title("🍽 Recipe Finder with Real Ratings")
st.subheader("Search meals with actual community ratings")

# Search input
query = st.text_input("Search for a meal or ingredient")

if st.button("Search") and query:
    # Spoonacular search endpoint
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": query,
        "number": 5,
        "addRecipeInformation": True,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            st.warning("No recipes found. Try something else.")
        else:
            for meal in data["results"]:
                st.markdown("---")
                st.subheader(meal["title"])
                st.image(meal["image"], use_column_width=True)

                # --- Actual Rating ---
                score = meal.get("spoonacularScore", 0)
                health = meal.get("healthScore", 0)
                st.markdown(f"**Community Score:** {'⭐' * round(score / 20)} ({score}/100)")
                st.markdown(f"**Health Score:** 🥗 {health}/100")

                # --- Summary ---
                st.markdown("**Summary:**", unsafe_allow_html=True)
                st.write(meal.get("summary", "No description.").replace("<b>", "").replace("</b>", ""))

                # --- Instructions ---
                if meal.get("analyzedInstructions"):
                    st.markdown("**Instructions:**")
                    for step in meal["analyzedInstructions"][0]["steps"]:
                        st.write(f"{step['number']}. {step['step']}")
                else:
                    st.write("No instructions available.")

                # --- Ingredients ---
                if meal.get("extendedIngredients"):
                    with st.expander("🛒 Ingredients"):
                        for ing in meal["extendedIngredients"]:
                            st.write(f"- {ing['original']}")

                # --- External link to full recipe ---
                if meal.get("sourceUrl"):
                    st.markdown(f"[🔗 Full Recipe Source]({meal['sourceUrl']})")

    except requests.RequestException as e:
        st.error(f"Error: {e}")
