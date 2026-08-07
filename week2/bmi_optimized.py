class BMIcalculator:
  @staticmethod
  def getdata() -> list[float]:
    w = float(input("Please enter your weight in kilograms:"))
    h = float(input("Please enter your height in centimetres:")) / 100.0
    return [w, h]

  @staticmethod
  def calculate(w: float, h: float) -> float:
    return round(w/(h*h),2)


def main():
  calculator = BMIcalculator()
  [w,h] = calculator.getdata()
  bmi = calculator.calculate(w, h)

  print(f"Your BMI is {bmi}")

if __name__ == "__main__":
    main()