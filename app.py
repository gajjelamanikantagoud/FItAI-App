import streamlit as st
import joblib
import pandas as pd
import datetime
import plotly.express as px

from workout_planner import generate_workout
from diet_planner import generate_diet
from helpers import calculate_bmi, activity_factor


# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Fitness Planner", layout="wide")


# ================= LOAD CSS =================
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ================= DAILY RESET =================
today = str(datetime.date.today())

if "date" not in st.session_state or st.session_state.date != today:
    st.session_state.date = today
    st.session_state.plan_generated = False
    st.session_state.diet_plan = None
    st.session_state.workout_plan = None
    st.session_state.calories_needed = 0
    st.session_state.bmi = 0


# ================= DEFAULT STATE =================
st.session_state.setdefault("plan_generated", False)
st.session_state.setdefault("diet_plan", None)
st.session_state.setdefault("workout_plan", None)
st.session_state.setdefault("calories_needed", 0)
st.session_state.setdefault("bmi", 0)


# ================= TITLE =================
st.markdown("## 💪 AI Personalized Workout & Diet Planner")
st.caption("Live daily tracker • Workout + Diet • Auto reset every day")


# ================= USER INPUT =================
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 16, 60, 22)
    height = st.number_input("Height (cm)", 140, 210, 170)
    weight = st.number_input("Weight (kg)", 40, 150, 65)

with col2:
    activity_label = st.selectbox(
        "Activity Level", ["Sedentary", "Light", "Moderate", "Active"]
    )
    goal = st.selectbox(
        "Goal", ["Fat Loss", "Muscle Gain", "Maintenance"]
    )
    diet_type = st.selectbox(
        "Diet Type", ["Veg", "Non-Veg"]
    )
    budget = st.slider("Monthly Food Budget (₹)", 1000, 5000, 2000)

activity = activity_factor(activity_label)


# ================= GENERATE PLAN =================
if st.button("🚀 Generate Today’s Plan"):
    model = joblib.load("models/calorie_model.pkl")

    input_df = pd.DataFrame([{
        "age": age,
        "height": height,
        "weight": weight,
        "activity": activity
    }])

    st.session_state.calories_needed = int(model.predict(input_df)[0])
    st.session_state.bmi = calculate_bmi(weight, height)
    st.session_state.workout_plan = generate_workout(goal, 30)
    st.session_state.diet_plan = generate_diet(diet_type, budget)
    st.session_state.plan_generated = True


# ================= DISPLAY PLAN =================
if st.session_state.plan_generated:

    st.divider()

    # ---------- STATS ----------
    st.subheader("📊 Your Stats")
    c1, c2 = st.columns(2)
    c1.metric("BMI", st.session_state.bmi)
    c2.metric("Daily Calories", f"{st.session_state.calories_needed} kcal")

    st.divider()

    # =====================================================
    # 🏋️ WORKOUT TRACKING
    # =====================================================
    st.subheader("🏋️ Workout Progress")

    workout_total = len(st.session_state.workout_plan)
    workout_done = 0

    for i, workout in enumerate(st.session_state.workout_plan, start=1):
        key = f"{today}_workout_{i}"

        if st.checkbox(f"Day {i}: {workout}", key=key):
            workout_done += 1

    workout_data = {
        "Completed": workout_done,
        "Remaining": workout_total - workout_done
    }

    workout_fig = px.pie(
    names=list(workout_data.keys()),
    values=list(workout_data.values()),
    hole=0.45,
    color=list(workout_data.keys()),
    color_discrete_map={
        "Completed": "#22c55e",   # Green = done
        "Remaining": "#ef4444"    # Red = pending
    }
)


    st.plotly_chart(workout_fig, use_container_width=True)
    st.success(f"🏋️ Workout completion: {int((workout_done/workout_total)*100)}%")

    st.divider()

    # =====================================================
    # 🥗 DIET TRACKING
    # =====================================================
    st.subheader("🥗 Diet Progress")

    total_cal = 0
    consumed_cal = 0

    for meal_time, foods in st.session_state.diet_plan.items():
        st.markdown(f"### 🍽️ {meal_time}")

        for food in foods:
            key = f"{today}_diet_{meal_time}_{food['item']}"

            if st.checkbox(
                f"{food['item']} — {food['grams']}g ({food['cal']} kcal)",
                key=key
            ):
                consumed_cal += food["cal"]

            total_cal += food["cal"]

    diet_data = {
        "Consumed": consumed_cal,
        "Remaining": max(total_cal - consumed_cal, 0)
    }

    diet_fig = px.pie(
    names=list(diet_data.keys()),
    values=list(diet_data.values()),
    hole=0.45,
    color=list(diet_data.keys()),
    color_discrete_map={
        "Consumed": "#00f5d4",    # Teal = eaten
        "Remaining": "#f97316"    # Orange = pending
    }
)



    st.plotly_chart(diet_fig, use_container_width=True)
    st.success(f"🥗 Diet completion: {int((consumed_cal/total_cal)*100)}%")

    st.caption("✅ Automatically resets every day • Stay consistent")

