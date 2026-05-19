def check_grade(mark=0):
    if (mark >= 90 and mark <= 100):
        return "A"
    elif (mark >= 80 and mark < 90):
        return "B"
    elif (mark >= 70 and mark < 80):
        return "C"
    elif (mark >= 60 and mark < 70):
        return "D"
    else:
        return "F"

def main():
    grade_desc = {
        "A": "Excellent",
        "B": "Very Good",
        "C": "Good",
        "D": "Pass",
        "F": "Fail"
    }

    while True:
        marks_obtained = input("Enter your marks: ")

        grade = check_grade(int(marks_obtained))

        match grade:
            case "A":
                print(f"{grade_desc["A"]} (A)")
            case "B":
                print(f"{grade_desc["B"]} (B)")
            case "C":
                print(f"{grade_desc["C"]} (C)")
            case "D":
                print(f"{grade_desc["D"]} (D)")
            case "F":
                print(f"{grade_desc["F"]} (F)")
            case _:
                print("Please try again.")

if __name__ == "__main__":
    main()
