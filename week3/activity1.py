from ucimlrepo import fetch_ucirepo
import pandas as pd

def main():
  # fetch dataset 
  iris = fetch_ucirepo(id=53)

  # Explicit types help VS Code/Pylance provide autocomplete
  features: pd.DataFrame = iris.data.features
  targets: pd.DataFrame = iris.data.targets

  flower_names = targets["class"].dropna().unique().tolist()

  print(f"Number of different flowers: {len(flower_names)}")
  print(f"Flower names: {flower_names}")

if __name__ == "__main__":
  main()