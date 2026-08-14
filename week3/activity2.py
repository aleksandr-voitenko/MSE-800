from pathlib import Path

def main():
  input_file_path = Path(__file__).parent / "junk.txt"
  output_file_path = Path(__file__).parent / "out.txt"

  with open(input_file_path, "r") as in_data:
    lines = in_data.readlines()
    print(f"Total number of lines: {len(lines)}")


    with open(output_file_path, "w") as out_data:
      for line in lines:
        out_data.write(line.lower())
      out_data.write("text file nanalyssis")

if __name__ == "__main__":
  main()