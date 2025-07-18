import json
import os
# Biometric Data Calculator and Health Analyzer 
# Create a health data processing tool that calculates BMI, 
# body fat percentage, and metabolic rates from input measurements, 
# analyzes fitness tracking data and exercise patterns, 
# implements calorie calculation and nutritional analysis algorithms, 
# tracks health metrics over time with trend analysis, 
# validates health data for medical consistency, and 
# generates health assessment reports with 
# personalized recommendations and risk factors.
name = input("Enter Your Name: ")
weight = float(input("input Weight(kg): "))
height = float(input("input Height(m): "))
age = float(input("input your Age: "))
sex_str = input("input your Sex: ")
sex_function = lambda sex: 1 if sex == 'Male' or sex == 'male' else 0
sex = sex_function(sex_str)
activity_level = input("Choose how active you are(sedentary, light activity, moderate, active, very active):")
with open("health_report.txt", "w") as f:
    f.write(f"BIOMETRIC DATA CALCULATOR AND HEALTH ANALYZER\n\nName: {name}\nWeight: {weight}\nHeight: {height}\nAge: {age}\nSex: {sex_str}")
errors = []
def validate_inputs(age, weight, height):
    
    if not (1 <= age <= 120):
        errors.append("Age must be between 1 and 120.")
    if not (0.8 <= height <= 2.5):  # height in meters
        errors.append("Height should be in meters (between 2.0m and 2.5m is typical).")
    if not (10 <= weight <= 300):
        errors.append("Weight should be realistic (10–300 kg).")

validate_inputs(age, weight, height)

def compute_activity(activity_leve):
    if activity_leve == 'sedentary':
        factor = 1.2
    elif activity_leve == 'light activity':
        factor = 1.375
    elif activity_leve == 'moderate':
        factor = 1.55
    elif activity_leve == 'active':
        factor = 1.725
    elif activity_leve == 'very active':
        factor = 1.9
    else:
        print('Invalid Input')
        return None
    return factor

def get_weekly_activity_log(weight):
    met_values = {
        "walking": 3.5,
        "jogging": 7,
        "running": 8.3,
        "cycling": 4,
        "gym": 6,
        "swimming": 6
    }
    # food_log = []
    activity_log = []
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for day in weekdays:
        print(f"\n--- {day} ---")
        activity = input("Enter activity (walking, jogging, running, cycling, gym, swimming or 'nothing'): ").strip().lower()
        
        minutes = int(input("How many minutes did you do it?: "))
        protein = float(input("Enter grams of protein consumed today: "))
        carbs = float(input("Enter grams of carbohydrates consumed today: "))
        fat = float(input("Enter grams of fat consumed today: "))
        water = float(input("Enter grams of water consumed today: "))
        
        calories_gained = protein*4 + carbs*4 + fat*9
        if activity == "nothing" or activity == "" or activity == "none" or activity == "nil":
            activity_log.append({
                "day": day,
                "activity": "none",
                "minutes": 0,
                "calories_burned": 0,
                "protein_gram": protein,
            "carbohydrate_gram": carbs,
            "fat_gram": fat,
            "water_gram": water,
            "calories_gained": calories_gained
            })
            continue

        met = met_values.get(activity, 3)  # fallback to MET=3
        calories_per_min = (met * weight * 3.5) / 200
        calories_burned = calories_per_min * minutes
        activity_log.append({
            "day": day,
            "activity": activity,
            "minutes": minutes,
            "calories_burned": calories_burned,
            "protein_gram": protein,
            "carbohydrate_gram": carbs,
            "fat_gram": fat,
            "water_gram": water,
            "calories_gained": calories_gained
        })
        
        if protein + carbs + fat == 0:
            errors.append("Nutrient intake cannot be zero.")
        if water < 1000:
            errors.append("Water intake is too low. Minimum is 1 liter.")
        # food_log.append({
        #     "day": day,
        #     "protein_gram": protein,
        #     "carbohydrate_gram": carbs,
        #     "fat_gram": fat,
        #     "water_gram": water,
        #     "calories_gained": calories_gained
        # })

    return activity_log

week_log = get_weekly_activity_log(weight)
def summarize_week(log):
    workout_days = [entry for entry in log if entry['activity'] != 'none']
    total_days = len(workout_days)
    total_minutes = sum(entry['minutes'] for entry in workout_days)
    total_calories_burned = sum(entry['calories_burned'] for entry in workout_days)
    total_calories_gained = sum(entry['calories_gained'] for entry in log)
    check_water_intake = sum(entry['water_gram'] for entry in log)
    water_warning = lambda: "please take in more water" if check_water_intake < 13500 else ""
    
   
    print(water_warning())
    return total_days, total_calories_gained, total_calories_burned,total_minutes, check_water_intake


factor = compute_activity(activity_level)

def compute_bmr(sex, w,h,a):
    h_cm = h * 100
    if sex == 1:
        #BMR=10×weight (kg)+6.25×height (cm)−5×age (years)+5
        
        bmr =  10 * w + 6.25 * h_cm - 5 * a + 5
    else:
        #BMR=10×weight (kg)+6.25×height (cm)−5×age (years)−161
        bmr = 10 * w + 6.25 * h_cm - 5 * a - 161
    return bmr
bmr = compute_bmr(sex, weight, height, age)
tdee = lambda: bmr * factor if factor else 0

def compute_bmi(h, w):
    bmi = w/(h**2)
    return bmi

def compute_body_fat_percentage(bmi, s, a):
    #BFP=1.20×BMI+0.23×Age−10.8×Sex−5.4
    bfp = 1.2 * bmi + 0.23 * a - 10.8 * s - 5.4
    return bfp

bmi = compute_bmi(height, weight)
bfp = compute_body_fat_percentage(bmi, sex, age)
# print(f"Your BMI is:  {bmi:.2f}")
# print(f"Your Body Fat Percentage is: {bfp:.2f}")
# print(f"Basal Metabolic Rate (BMR): {bmr:.2f} kcal/day")
# print(f"Total Daily Energy Expenditure (TDEE): {tdee():.2f} kcal/day")



def validate_calorie_distribution(total_cal):
    if total_cal < 1000:
        return "Total calorie intake is too low for healthy function."
    elif total_cal > 5000:
        return "Total calorie intake is too high and may be unhealthy."
    return None
if os.path.exists("health_trends.json"):
    with open("health_trends.json", "r") as file:
        health_trends = json.load(file)
else:
    health_trends = []

week = len(health_trends) + 1
workout_days, cal_gained, cal_burned,  total_minutes, water_gram = summarize_week(week_log)
if not errors:
    print(f"Your BMI is:  {bmi:.2f}")
    print(f"Your Body Fat Percentage is: {bfp:.2f}")
    print(f"Basal Metabolic Rate (BMR): {bmr:.2f} kcal/day")
    print(f"Total Daily Energy Expenditure (TDEE): {tdee():.2f} kcal/day")
    net = cal_gained - cal_burned
    print(f"\nNet Calories Today: {net:.2f} kcal")
    if net > 0:
        print("You are in a calorie surplus (weight gain).")
    elif net < 0:
        print("You are in a calorie deficit (weight loss).")
    else:
        print("You maintained your current weight.")
    print(f"\nYou worked out {workout_days} day(s) this week.")
    print(f"Total exercise time: {total_minutes} minutes")
    print(f"Total calories burned: {cal_burned:.2f} kcal")
    with open("health_report.txt", "a") as f:
        f.write(f"\n\nBMI: {bmi:.2f}\nBody Fat: {bfp:.2f}\nBasal Metabolic Rate (BMR): {bmr:.2f} kcal/day\nTotal Daily Energy Expenditure (TDEE): {tdee():.2f} kcal/day\nNet Calories Today: {net:.2f} kcal\nYou worked out {workout_days} day(s) this week.\nTotal exercise time: {total_minutes} minutes\nTotal calories burned: {cal_burned:.2f} kcal")
else:
    print("Medical Consistency Warnings:")
    for err in errors:
        print("-", err)
cal_check = validate_calorie_distribution(cal_gained)
if cal_check:
    print(cal_check)
print(workout_days, cal_gained, cal_burned)
weekly_summary = {
    "week": week,
    "workout_days": workout_days,
    "calories_gained": cal_gained,
    "calories_burned": cal_burned,
    "bmi": bmi,
    "body_fat_pct": bfp,
    "tdee": tdee(),
}
health_trends.append(weekly_summary)

def analyze_trend(health_trends):
    if len(health_trends) < 2:
        print("Not enough data for trend analysis.")
        return

    last_week = health_trends[-2]
    this_week = health_trends[-1]

    print("\nTrend Analysis")
    print(f"Workout days: {last_week['workout_days']} → {this_week['workout_days']} ({this_week['workout_days'] - last_week['workout_days']:+})")
    print(f"Calories Gained: {last_week['calories_gained']:.2f} → {this_week['calories_gained']:.2f} ({this_week['calories_gained'] - last_week['calories_gained']:+.2f} kcal)")
    print(f"Calories Burned: {last_week['calories_burned']:.2f} → {this_week['calories_burned']:.2f} ({this_week['calories_burned'] - last_week['calories_burned']:+.2f} kcal)")
    print(f"BMI: {last_week['bmi']} → {this_week['bmi']} ({this_week['bmi'] - last_week['bmi']:+.2f})")
    print(f"Body Fat %: {last_week['body_fat_pct']} → {this_week['body_fat_pct']} ({this_week['body_fat_pct'] - last_week['body_fat_pct']:+.2f}%)")
    with open("health_report.txt", "a") as f:
        f.write(f"\n\nTrend Analysis\n\nWorkout days: {last_week['workout_days']} to {this_week['workout_days']} ({this_week['workout_days'] - last_week['workout_days']:+})\nCalories Gained: {last_week['calories_gained']:.2f} to {this_week['calories_gained']:.2f} ({this_week['calories_gained'] - last_week['calories_gained']:+.2f} kcal)\nCalories Burned: {last_week['calories_burned']:.2f} to {this_week['calories_burned']:.2f} ({this_week['calories_burned'] - last_week['calories_burned']:+.2f} kcal)\nBMI: {last_week['bmi']} to {this_week['bmi']} ({this_week['bmi'] - last_week['bmi']:+.2f})\nBody Fat %: {last_week['body_fat_pct']} to {this_week['body_fat_pct']} ({this_week['body_fat_pct'] - last_week['body_fat_pct']:+.2f}%)")
with open("health_trends.json", "w") as file:
    json.dump(health_trends, file, indent=4)

analyze_trend(health_trends)

def generate_health_report(bmi, bfp, cal_gained, cal_burned, water_gram, workout_days):
    print("\n📝 Health Assessment Report")
    net_calories =  cal_gained - cal_burned
    # --- BMI Status
    if bmi < 18.5:
        print("• BMI Status: Underweight – Consider increasing calorie intake and strength training.")
    elif 18.5 <= bmi <= 24.9:
        print("• BMI Status: Normal – Keep up the good work!")
    elif 25 <= bmi <= 29.9:
        print("• BMI Status: Overweight – Consider reducing daily calories and increasing activity.")
    else:
        print("• BMI Status: Obese – High risk for cardiovascular diseases. Medical advice recommended.")

    # --- Body Fat %
    if bfp > 32:
        print("• Body Fat: High – Try to reduce fat intake and increase cardio.")
    elif bfp < 10:
        print("• Body Fat: Low – Ensure you're getting enough nutrition.")
    else:
        print("• Body Fat: Within healthy range.")

    # --- Net Calories
    if net_calories > 500:
        print("• Calorie Balance: High surplus – Possible weight gain risk.")
    elif net_calories < -500:
        print("• Calorie Balance: Large deficit – May cause fatigue or muscle loss.")
    else:
        print("• Calorie Balance: Stable – Good for maintaining weight.")

    # --- Water
    if water_gram < 13500:  # ~1.5L per day for 5 days
        print("• Hydration: Low – Drink more water daily (2–3L recommended).")
    else:
        print("• Hydration: Good")

    # --- Workout Days
    if workout_days < 3:
        print(f"• Activity: Only {workout_days} day(s) – Try to exercise at least 3–5 times per week.")
    else:
        print(f"• Activity: Great! {workout_days} workout days this week.")

    print("\n✅ Personalized Recommendations:")
    if bmi > 25 or bfp > 30:
        print("- Try reducing sugary and fatty foods.")
    if water_gram < 10000:
        print("- Keep a water bottle handy to drink more often.")
    if workout_days < 3:
        print("- Start with 15-minute walks daily to build consistency.")
    if net_calories < 0:
        print("- Eat more whole grains and lean proteins to stay energized.")

generate_health_report(bmi, bfp, cal_gained, cal_burned, water_gram, workout_days)
