class Matrix:
    """Matrix class"""

    def __init__(self, values):
        # Copy each row so changes to the original list do not affect the matrix.
        self._values = [row.copy() for row in values]

    @property
    def rows(self):
        return len(self._values)

    @property
    def columns(self):
        return len(self._values[0])

    def to_list(self):
        """Return the matrix as a new two-dimensional list"""
        return [row.copy() for row in self._values]

    def multiply(self, other):
        """Multiply this matrix by another Matrix object"""
        if not isinstance(other, Matrix):
            raise TypeError("The other value must be a Matrix object.")

        if self.columns != other.rows:
            raise ValueError("Matrices cannot be multiplied.")

        result = []

        for row_index in range(self.rows):
            result_row = []

            for column_index in range(other.columns):
                cell_value = 0

                for item_index in range(self.columns):
                    cell_value += (self._values[row_index][item_index] * other._values[item_index][column_index])

                result_row.append(cell_value)

            result.append(result_row)

        return Matrix(result)

    def __matmul__(self, other):
        """Allow multiplication with the @ operator"""
        return self.multiply(other)

    def __str__(self):
        """Provides a representation for the print function"""
        return "\n".join(str(row) for row in self._values)


def main():
    matrix_1_values = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
    ]
    matrix_1 = Matrix(matrix_1_values)
    print(f"Matrix 1 ({matrix_1.rows}x{matrix_1.columns}):")
    print(matrix_1)

    matrix_2_values = [
        [1, 2],
        [3, 4],
        [5, 6],
        [7, 8],
        [9, 10],
    ]
    matrix_2 = Matrix(matrix_2_values)
    print(f"\nMatrix 2 ({matrix_2.rows}x{matrix_2.columns}):")
    print(matrix_2)

    result = matrix_1 @ matrix_2
    print(f"\nResult ({result.rows}x{result.columns}):")
    print(result)

if __name__ == "__main__":
    main()
