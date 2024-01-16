import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

x1 = [
    datetime(2021, 2, 17),
    datetime(2021, 2, 24),
    datetime(2021, 7, 13),
    datetime(2021, 7, 21),
    datetime(2021, 9, 15),
]

x2 = [
    datetime(2022, 1, 27),
    datetime(2022, 2, 16),
    datetime(2022, 6, 17),
    datetime(2022, 6, 21),
    datetime(2022, 6, 22),
    datetime(2022, 7, 15),
    datetime(2022, 6, 28),
    datetime(2022, 9, 12),
    datetime(2022, 9, 30),
]

x3 = [
    datetime(2023, 1, 25),
    datetime(2023, 2, 2),
    datetime(2023, 2, 17),
    datetime(2023, 2, 22),
    datetime(2023, 6, 23),
    datetime(2023, 6, 26),
]


mark1 = [
    24,
    25,
    27,
    23,
    27,
]

mark2 = [
    22,
    30,
    28,
    26,
    29,
    28,
    26,
    28,
    23,
]

mark3 = [
    28,
    28,
    25,
    27,
    28,
    30,
]

# Convert x_values to numerical values
dates1 = mdates.date2num(x1)
dates2 = mdates.date2num(x2)
dates3 = mdates.date2num(x3)

# Fit a polynomial line to the data
coefficients = np.polyfit(dates1, mark1, 1)
poly_line1 = np.poly1d(coefficients)
poly_values1 = poly_line1(dates1)

coefficients = np.polyfit(dates2, mark2, 1)
poly_line2 = np.poly1d(coefficients)
poly_values2 = poly_line2(dates2)

coefficients = np.polyfit(dates3, mark3, 1)
poly_line3 = np.poly1d(coefficients)
poly_values3 = poly_line3(dates3)

# Specify the date format for the x-axis labels
date_format = mdates.DateFormatter("%d-%m-%Y")

# Create a single subplot for all data and trend lines
fig, ax = plt.subplots()
fig.subplots_adjust(top=0.8)

# Plot the data points and trend lines
ax.plot_date(dates1, mark1, ":o", label="First Year Data")  # Data points
ax.plot_date(dates1, poly_values1, "-", label="First Year Trend ")  # Trend line

ax.plot_date(dates2, mark2, ":o", label="Second Year Data")  # Data points
ax.plot_date(dates2, poly_values2, "-", label="Second Year Trend ")  # Trend line

ax.plot_date(dates3, mark3, ":o", label="Third Year Data")  # Data points
ax.plot_date(dates3, poly_values3, "-", label="Third Year Trend ")  # Trend line

# Place the legend below the graph
plt.legend(bbox_to_anchor=(0.5, 1.3), loc="upper center", ncol=3)

plt.title("Mark Analysis")
plt.xlabel("Date")
plt.ylabel("Mark")
plt.gcf().autofmt_xdate()

plt.style.use("default")
plt.savefig("graph_light.png")

# Save the dark version
plt.style.use("dark_background")
plt.savefig("graph_dark.png")
