from textwrap import dedent

def identify_city_prompt(origin, cities, interests, date_range):
    return dedent(f"""
    You are a travel expert. Based on the following details, rank the candidate cities:

    Origin: {origin}
    Candidate Cities: {cities}
    Traveler Interests: {interests}
    Date Range: {date_range}

    Provide a ranked list of cities with a short explanation for each ranking.
    Use clean formatting with bold section titles, but DO NOT wrap text in asterisks.
    """).strip()


def plan_itinerary_prompt(origin, selected_city, interests, date_range):
    return dedent(f"""
    You are an expert travel planner. Create a detailed **7-day itinerary**.

    Origin: {origin}
    Destination City: {selected_city}
    Traveler Interests: {interests}
    Date Range: {date_range}

    STRICT REQUIREMENTS:
    - Write ONLY one cleanly formatted day-by-day itinerary first.
    - Do NOT include any budget inside daily schedules.
    - Each day must include clearly labeled sections:
        Morning: activity + notes
        Afternoon: activity + notes
        Lunch: recommend a restaurant
        Evening: activity + notes
        Dinner: recommend a restaurant
        Night Stay: recommend a hotel
    - Use plain bold titles like Morning:, Afternoon:, etc. (no asterisks).
    - Keep activities realistic and geographically consistent.
    - Include local food and cultural experiences daily.
    - Provide short justifications only for key recommendations.

    ✅ Important: The "Estimated Budget" section must come ONLY AFTER all 7 days are completed.
    - Absolutely NO budget lines should appear inside Day 1–7.
    - The final "Estimated Budget" block should appear once, at the very end.

    Output format:

    Day 1:
    Morning: ...
    Afternoon: ...
    Lunch: ...
    Evening: ...
    Dinner: ...
    Night Stay: ...

    Day 2:
    ...

    Day 7:
    ...

    Estimated Budget:
    Flights: ...
    Hotels: ...
    Food: ...
    Activities: ...
    Transport: ...
    """).strip()


def gather_city_info_prompt(city, interests, date_range):
    return dedent(f"""
    For {city} (dates: {date_range}), give:
    - Top attractions
    - Best food picks
    - Safety tips tailored to {interests}

    Use bold text for section titles, no asterisks.
    """).strip()
