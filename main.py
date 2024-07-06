import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client with your API key from Streamlit secrets
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

def generate_travel_instructions(current_location, destination):
    # Construct system prompt for AI
    system_prompt = f"""
    You are currently at {current_location}. You want to go to {destination}. Here are the travel instructions:

    Please provide detailed travel instructions for the following modes of transportation, including every stop and the cost estimates:

    🚆 By Train:
    1. Go to the nearest train station. (state the KTM station name)
    2. Buy a ticket to your destination. (include ticket price)
    3. Board the train and take your seat.
    4. Follow the route, including every stop, until you reach your destination.

    🚌 By Bus:
    1. Find the nearest bus stop.
    2. Check the bus schedule and choose the appropriate bus.
    3. Board the bus and pay the fare. (include bus fare)
    4. Travel on the bus route, including every stop, until you reach your destination.

    🚗 By Car (Driving):
    1. Navigate to {destination} using a navigation app.
    2. The distance to {destination} is approximately [distance in km].
    3. Choose the appropriate route - highway or local roads (jalan dalam).
    4. Follow traffic rules and signs, including every major intersection and landmark, until you reach your destination.
    5. Estimate the fuel consumption and cost based on the distance and an average fuel consumption rate of [fuel consumption rate].
    6. Estimated toll prices.

    Summary of Costs:
    - Include summarized costs for each mode of transportation here.
    """

    return system_prompt.strip()  # Remove any extra whitespace

def main():
    # Inject custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content {
            background-color: #e8eef3;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .output-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            color: black;  /* Ensure text color in output box is black */
        }
        h1, h2, h3, h4, h5, h6, p, div, input, button {
            color: black;  /* Ensure all text color is black */
        }
        .sidebar .sidebar-content h2, .sidebar .sidebar-content label {
            color: white;  /* Make sidebar header and labels white */
        }
        </style>
        """,
                unsafe_allow_html=True)

    # Streamlit app title and description
    st.title("🚗 Travel Instructions Assistant")
    st.write(
        "Enter your current location and destination to get detailed travel instructions."
    )

    # Collect user input for current location and destination
    with st.sidebar:
        st.header("Just ask me ! 😡")
        current_location = st.text_input("Enter your current location :")
        destination = st.text_input("Enter your destination :")
        generate_button = st.button("Generate Instructions")

    if generate_button:
        if not current_location or not destination:
            st.error("Both current location and destination must be provided.")
        else:
            # Generate system prompt
            system_prompt = generate_travel_instructions(
                current_location, destination)

            # Display spinner while generating instructions
            with st.spinner('Wait for it...'):
                time.sleep(5)  # Simulate a delay for demonstration purposes

                # Send request to OpenAI API for response
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{
                            "role": "system",
                            "content": system_prompt
                        }, {
                            "role":
                            "user",
                            "content":
                            f"My current location is {current_location} and I want to travel to {destination}."
                        }])

                    # Extract and display response from OpenAI API
                    travel_instructions = response.choices[0].message.content

                    st.markdown("## 📋 Travel Instructions")
                    st.markdown(
                        f"<div class='output-box'>{travel_instructions}</div>",
                        unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                st.success('Done!')

if __name__ == "__main__":
    main()
