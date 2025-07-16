weight = float(input("input Weight(kg): "))
height = float(input("input Height(m): "))
age = float(input("input your Age: "))
sex_str = input("input your Sex: ")
sex_function = lambda sex: 1 if sex == 'Male' or sex == 'male' else 0
sex = sex_function(sex_str)
activity_level = input("Choose how active you are(sedentary, light activity, moderate, active, very active):")
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
factor = compute_activity(activity_level)

def compute_bmr(sex, w,h,a):
    if sex == 1:
        #BMR=10×weight (kg)+6.25×height (cm)−5×age (years)+5
        h_cm = h * 100
        bmr =  10 * w + 6.25 * h_cm - 5 * a + 5
    else:
        #BMR=10×weight (kg)+6.25×height (cm)−5×age (years)−161
        bmr = 10 * w + 6.25 * h_cm - 5 * a - 161
    return bmr
bmr = compute_bmr(sex, weight, height, age)
tdee = bmr * factor

def compute_bmi(h, w):
    bmi = w/(h**2)
    return bmi

def compute_body_fat_percentage(bmi, s, a):
    #BFP=1.20×BMI+0.23×Age−10.8×Sex−5.4
    bfp = 1.2 * bmi + 0.23 * a - 10.8 * s - 5.4
    return bfp

bmi = compute_bmi(height, weight)
bfp = compute_body_fat_percentage(bmi, sex, age)
print("Your BMI is: ", bmi)
print("Your Body Fat Percentage is: ", bfp)
print(f"Basal Metabolic Rate (BMR): {bmr:.2f} kcal/day")
print(f"Total Daily Energy Expenditure (TDEE): {tdee:.2f} kcal/day")

