import fileinput

# Calculation of body mass index
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Provide meaning to a numeric BMI value
def explain_bmi(bmi):
    if bmi < 18.5:
        return "Underweight (less than 18.5)"
    elif bmi < 24.9:
        return "Healthy weight (18.5 to 24.9)"
    elif bmi < 29.9:
        return "Overweight (25 to 29.9)"
    else:
        return "Obese: (30 or higher)"

# Application's entry point
def main():
    weight = float(input('Input weight (kg): '))
    height = float(input('Input height (cm): ')) / 100.0
    bmi = calculate_bmi(weight, height)
    print(f"BMI: {bmi:.2f}, {explain_bmi(bmi)}")

if __name__ == "__main__":
    main()