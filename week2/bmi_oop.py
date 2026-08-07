class BmiCalculator:
    bmi_value: float;

    def get(self):
        return self.bmi_value;

    # Calculation of body mass index
    def calculate(self, weight, height):
        self.bmi_value = weight / (height ** 2)

    # Provide meaning to a numeric BMI value
    def explain(self):
        if self.bmi_value < 18.5:
            return "Underweight (less than 18.5)"
        elif self.bmi_value < 24.9:
            return "Healthy weight (18.5 to 24.9)"
        elif self.bmi_value < 29.9:
            return "Overweight (25 to 29.9)"
        else:
            return "Obese: (30 or higher)"

# Application's entry point
def main():
    weight = float(input('Input weight (kg): '))
    height = float(input('Input height (cm): ')) / 100.0

    bmi_calculator = BmiCalculator()
    bmi_calculator.calculate(weight, height)
    print(f"BMI: {bmi_calculator.get():.2f}, {bmi_calculator.explain()}")

if __name__ == "__main__":
    main()