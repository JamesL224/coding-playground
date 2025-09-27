# First Practical Exercise: Patient Vitals Calculator

print("--- Simple Patient Vitals Check ---")

# We'll use variables to store some patient data.
# In a real application, this would come from a database or user input.
patient_id = "PID-9871"
heart_rate = 98  # Beats per minute
body_temperature_f = 101.3 # Fahrenheit

# --- Heart Rate Check ---
# Let's write a simple check for tachycardia (a fast heart rate, often defined as > 100 bpm for adults)
is_tachycardic = heart_rate > 100

print(f"Patient {patient_id} Heart Rate: {heart_rate} bpm")
print(f"Is patient tachycardic? {is_tachycardic}")
print("-" * 20) # A separator line for clarity

# --- Temperature Conversion ---
# Let's convert the temperature from Fahrenheit to Celsius.
# The formula is: C = (F - 32) * 5/9
temperature_celsius = (body_temperature_f - 32) * (5/9)
has_fever = body_temperature_f > 100.4

print(f"Body Temperature (F): {body_temperature_f}°F")
# We use :.2f to format the Celsius temperature to two decimal places for easier reading.
print(f"Body Temperature (C): {temperature_celsius:.2f}°C")
print("-" * 20)
print(f"Does patient have a fever? {has_fever}")

# --- Next Steps ---
# Think about what other checks you could do!
# - Check for fever (e.g., if temperature is above 100.4°F)
# - Categorize blood pressure (you'd need two more variables: systolic and diastolic)
# Feel free to add more code below and experiment!
