import streamlit as st
from dotenv import load_dotenv
import base64
from fpdf import FPDF
import os
import re

from trip_agents import call_llm
from trip_tasks import plan_itinerary_prompt, gather_city_info_prompt
from utils.flight_api import get_flight_price
from utils.hotel_api import get_hotel_prices

load_dotenv()

st.set_page_config(page_title="AI Trip Planner", page_icon="🧳", layout="centered")
st.title("🧳 Smart AI Trip Planner (gemma:2b)")

predefined_cities = ["Paris", "Tokyo", "New York", "London", "Bangkok", "Sydney", "Rome", "Istanbul"]

with st.form("trip_form"):
    origin = st.text_input("🌍 From where will you be travelling? (IATA code, e.g., DEL)")
    selected_city = st.multiselect("🏙️ Choose your dream destinations:", predefined_cities)
    custom_city = st.text_input("➕ Or add a custom city (optional, city name or IATA)")
    date_range = st.text_input("📅 Date range (e.g., 2024-08-10 to 2024-08-17)")
    interests = st.text_area("🎯 Your interests/hobbies")
    submitted = st.form_submit_button("Generate Trip Plan")


def estimate_budget(num_days, cities, origin, travel_date):
    food_per_day = 40
    activity_per_day = 60
    transport_per_day = 15

    total_food = food_per_day * num_days
    total_activity = activity_per_day * num_days
    total_transport = transport_per_day * num_days

    hotel_total = 0
    for city in cities:
        nightly_rate = get_hotel_prices(city)
        try:
            hotel_total += float(nightly_rate) * num_days
        except:
            hotel_total += 100 * num_days

    total_flight = 0
    for city in cities:
        flight_data = get_flight_price(origin, city, travel_date)
        if isinstance(flight_data, dict) and "Quotes" in flight_data and flight_data["Quotes"]:
            total_flight += flight_data["Quotes"][0].get("MinPrice", 300)
        else:
            total_flight += 300

    return [
        ("Flights", f"${int(total_flight)}"),
        ("Hotels", f"${int(hotel_total)}"),
        ("Food", f"${int(total_food)}"),
        ("Activities", f"${int(total_activity)}"),
        ("Transport", f"${int(total_transport)}")
    ]


if submitted:
    with st.spinner("Generating trip plan..."):
        all_cities = selected_city.copy()
        if custom_city:
            all_cities.append(custom_city)
        cities_str = ", ".join(all_cities) if all_cities else "No cities provided"

        try:
            if "to" in date_range:
                start_str, end_str = [s.strip() for s in date_range.split("to")]
                start_day = int(start_str.split("-")[-1])
                end_day = int(end_str.split("-")[-1])
                days = abs(end_day - start_day) + 1
            else:
                days = 7
        except:
            days = 7

        travel_date = date_range.split(" to ")[0] if "to" in date_range else "2024-08-10"
        budget = estimate_budget(days, all_cities, origin, travel_date)

        # City infos
        city_infos = []
        for city in all_cities:
            prompt_city = gather_city_info_prompt(city, interests, date_range)
            info = call_llm(prompt_city, model_name="gemma:2b", temperature=0.7, max_tokens=512)
            city_infos.append((city, info))

        # Itinerary
        plan_prompt = plan_itinerary_prompt(origin, selected_city, interests, date_range)
        itinerary = call_llm(plan_prompt, model_name="gemma:2b", temperature=0.7, max_tokens=1024)

    st.success("✅ Trip Plan Ready!")
    st.subheader("7-Day Itinerary")
    st.markdown(itinerary, unsafe_allow_html=True)

    st.subheader("Estimated Budget")
    for item, cost in budget:
        st.markdown(f"<b>{item}:</b> {cost}", unsafe_allow_html=True)
    st.markdown("*Note: This is a rough estimate and actual costs may vary.*")

    if city_infos:
        st.subheader("City Information")
        for city, info in city_infos:
            st.markdown(f"### {city}")
            st.markdown(info, unsafe_allow_html=True)

    # ==============================
    # ✅ PDF Generation with Unicode Font
    # ==============================
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add Unicode font (make sure DejaVuSans.ttf exists in "fonts/" folder)
    font_path = os.path.join("fonts", "DejaVuSans.ttf")     
    if not os.path.exists(font_path):
        st.error("❌ Missing font file: fonts/DejaVuSans.ttf. Please download and place it in the fonts/ folder.")
    else:
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", '', 16)

        pdf.cell(0, 10, "AI Trip Planner Itinerary", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("DejaVu", '', 12)
        pdf.multi_cell(0, 10, itinerary)
        pdf.ln(10)

        pdf.set_font("DejaVu", '', 14)
        pdf.cell(0, 10, "Estimated Budget", ln=True)
        pdf.set_font("DejaVu", '', 12)
        for item, cost in budget:
            pdf.cell(0, 10, f"{item}: {cost}", ln=True)

        if city_infos:
            pdf.ln(10)
            pdf.set_font("DejaVu", '', 14)
            pdf.cell(0, 10, "City Information", ln=True)
            pdf.set_font("DejaVu", '', 12)
            for city, info in city_infos:
                pdf.set_font("DejaVu", '', 12)
                pdf.cell(0, 10, city, ln=True)
                pdf.set_font("DejaVu", '', 12)
                pdf.multi_cell(0, 10, info)
                pdf.ln(5)

        pdf_output = "trip_itinerary.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as f:
            pdf_data = f.read()
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="trip_itinerary.pdf">📄 Download Itinerary as PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
        os.remove(pdf_output)

    st.markdown("---")
