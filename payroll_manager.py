
import csv
import os

FILENAME = "sample-employees.csv"


def load_employees():
    """Load employee details from the CSV file."""
    if not os.path.exists(FILENAME):
        print(f"Error: {FILENAME} not found.")
        return None

    try:
        with open(FILENAME, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("Error: CSV file is empty.")
                return None

            # Normalize column headings
            reader.fieldnames = [
                heading.strip().lower() for heading in reader.fieldnames
            ]

            # Accept common variations of column names
            employees = []
            for row in reader:
                employee = {
                    key.strip().lower(): (value or "").strip()
                    for key, value in row.items()
                    if key is not None
                }
                employees.append(employee)

            if not employees:
                print("No employee records found.")
                return []

            return employees

    except (OSError, csv.Error) as error:
        print("Error reading CSV:", error)
        return None


def get_value(employee, possible_names, default="N/A"):
    """Find a value using alternative column names."""
    for name in possible_names:
        value = employee.get(name)
        if value not in (None, ""):
            return value
    return default


def get_salary(employee):
    """Read salary and convert it to a number."""
    salary_text = get_value(
        employee,
        ["salary", "annual_salary", "basic_salary", "wage"],
        ""
    )

    # Remove currency symbols and commas
    salary_text = salary_text.replace(",", "").replace("$", "").replace("₹", "")

    return float(salary_text)


def display_payroll():
    employees = load_employees()

    if employees is None:
        return

    print("\n================ PAYROLL DETAILS ================")
    print(
        f"{'Employee ID':<15}{'Name':<25}"
        f"{'Annual Salary':>16}{'Monthly Salary':>18}"
    )
    print("-" * 74)

    for employee in employees:
        try:
            emp_id = get_value(
                employee, ["employee_id", "employeeid", "id", "emp_id"]
            )
            name = get_value(employee, ["name", "employee_name", "full_name"])
            annual_salary = get_salary(employee)
            monthly_salary = annual_salary / 12

            print(
                f"{emp_id:<15}{name[:24]:<25}"
                f"{annual_salary:>16.2f}{monthly_salary:>18.2f}"
            )

        except (ValueError, TypeError):
            print("Skipping a record with a missing or invalid salary.")

    print("-" * 74)
    print("Monthly salary is estimated as annual salary divided by 12.")


def search_employee():
    employees = load_employees()

    if employees is None:
        return

    emp_id_to_find = input("Enter employee ID: ").strip().lower()

    for employee in employees:
        emp_id = get_value(
            employee, ["employee_id", "employeeid", "id", "emp_id"], ""
        ).lower()

        if emp_id == emp_id_to_find:
            print("\n========== EMPLOYEE DETAILS ==========")
            print("Employee ID:", get_value(
                employee, ["employee_id", "employeeid", "id", "emp_id"]
            ))
            print("Name:", get_value(
                employee, ["name", "employee_name", "full_name"]
            ))
            print("Department:", get_value(
                employee, ["department", "dept"]
            ))
            print("Job Title:", get_value(
                employee, ["title", "job_title", "position"]
            ))
            print("Location:", get_value(
                employee, ["location", "city"]
            ))

            try:
                annual_salary = get_salary(employee)
                print(f"Annual Salary: {annual_salary:.2f}")
                print(f"Estimated Monthly Salary: {annual_salary / 12:.2f}")
            except (ValueError, TypeError):
                print("Salary: Unavailable")

            return

    print("Employee not found.")


def main():
    while True:
        print("\n===== CSV PAYROLL MANAGEMENT SYSTEM =====")
        print("1. Display all employee payrolls")
        print("2. Search employee by ID")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_payroll()
        elif choice == "2":
            search_employee()
        elif choice == "3":
            print("Payroll Management System closed.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
