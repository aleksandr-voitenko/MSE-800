from dataclasses import dataclass

# Temperature representation for Celsius and Fahrenheit, can have invalid state
@dataclass
class Temperature:
  type: str = "_"; # invalid state
  value: int = 0;

  # Is the current state valid
  def is_valid(self) -> bool:
    return self.type == "C" or self.type == "F"

  # Parse user input
  def parse(self, s: str) -> None:
    if len(s) < 2:
      return

    self.type = s[0]
    try:
      self.value = int(s[1:])
    except ValueError:
      # Making type invalid in case of numeric parsing error
      self.type = "_"

# Temperature converter. This is a user-facing class
class TemperatureConverter:
  _should_stop: bool = False
  _temperature: Temperature = Temperature()
  _raw_input_string: str = ""

  # Is user input valid
  def is_input_valid(self):
    return self._temperature.is_valid()

  # Parse user input string
  def parse_input(self):
    self._temperature.parse(self._raw_input_string)

  # Prompt for user input
  def prompt_for_input(self):
    self._raw_input_string = input("Temperature: ")
    if len(self._raw_input_string) == 0:
      self._should_stop = True;

  # Shoud stop and exit
  def should_stop(self):
    return self._should_stop;

  # Convert temperature and print results
  def convert_and_print(self):
    if self._temperature.type == "C":
      f = (self._temperature.value * 9 / 5) + 32
      print(f"{self._raw_input_string} degrees Celsius is converted to {f:.2f} degrees Fahrenheit")
    else:
      c = (self._temperature.value - 32) * 5 / 9
      print(f"{self._raw_input_string} degrees Fahrenheit is converted to {c:.2f} degrees Celsius")

# Main entry point
def main():
  print("Input empty string to exit.");
  converter = TemperatureConverter()

  # Convertion loop
  while (True):
    converter.prompt_for_input();

    if converter.should_stop():
      return

    converter.parse_input()

    if not converter.is_input_valid():
      print("Invalid input. Please enter the temperature with the correct 'C' or F' prefix.")
      continue

    converter.convert_and_print()

if __name__ == "__main__":
  main()
  print("Done")