import matplotlib.pyplot as plt

# Scenario labels
scenarios = [
    "No change", "+10% Assembly", "+20% Assembly", "+30% Assembly", "No change (Processing +10%)", 
    "+10% Assembly + Processing +10%", "+20% Assembly + Processing +10%", "+30% Assembly + Processing +10%", 
    "No change (Processing +20%)", "+10% Assembly + Processing +20%", "+20% Assembly + Processing +20%", 
    "+30% Assembly + Processing +20%", "No change (Processing +30%)", "+10% Assembly + Processing +30%", 
    "+20% Assembly + Processing +30%", "+30% Assembly + Processing +30%"
]

# Corresponding Cmax values
Cmax_values = [23.5, 24.1, 24.7, 25.3, 25.25, 25.85, 26.45, 27.05, 27.0, 27.6, 28.2, 28.8, 28.75, 29.35, 29.95, 30.55]

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(scenarios, Cmax_values, marker='o', linestyle='-', color='b')

# Adding title and labels
plt.title('Sensitivity Analysis: Impact of Assembly and Processing Time Variations on Cmax')
plt.xlabel('Scenarios (Assembly & Processing Time Variations)')
plt.ylabel('Cmax (Makespan)')

# Rotating x-axis labels for better readability
plt.xticks(rotation=45, ha="right")

# Display the chart
plt.tight_layout()
plt.show()
