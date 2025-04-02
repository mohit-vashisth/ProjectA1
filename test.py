from sympy import symbols, Eq

# Define variables
F, m, a = symbols('F m a')

# Newton's Second Law equation
equation = Eq(F, m * a)

# Solve for force
mass_value = 10  # kg
acceleration_value = 5  # m/s²
force_value = equation.subs({m: mass_value, a: acceleration_value}).rhs #type: ignore

print(f"Force = {force_value} Newtons")




# how much electricty consume in a month

def calculate_units(power_watts, hours_per_day, days, devices):
    power_kw = power_watts / 1000  # Convert watts to kilowatts
    total_units = power_kw * hours_per_day * days * devices  # Energy in kWh (units)
    return total_units

# User input
power = float(input("Enter power rating of device (in watts): "))
hours = float(input("Enter daily usage (hours): "))
devices = int(input("Enter number of devices: "))
days = 30  # Assume 30 days in a month

# Compute electricity consumption in units
monthly_units = calculate_units(power, hours, days, devices)
print(f"Monthly electricity consumption: {monthly_units:.2f} units")

# Optional: Estimate electricity bill
cost_per_unit = float(input("Enter electricity cost per unit (₹/unit): "))
bill = monthly_units * cost_per_unit
print(f"Estimated monthly bill: ₹{bill:.2f}")
