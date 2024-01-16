import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

x_values = [
    datetime(2021, 2, 17),
    datetime(2021, 2, 24),
    datetime(2021, 7, 13),
    datetime(2021, 7, 21),
    datetime(2021, 9, 15),
    datetime(2022, 1, 27),
    datetime(2022, 2, 16),
    datetime(2022, 6, 17),
    datetime(2022, 6, 21),
    datetime(2022, 6, 22),
    datetime(2022, 7, 15),
    datetime(2022, 6, 28),
    datetime(2022, 9, 12),
    datetime(2022, 9, 30),
    datetime(2023, 1, 25),
    datetime(2023, 2, 2),
    datetime(2023, 2, 17),
    datetime(2023, 2, 22),
    datetime(2023, 6, 23),
    datetime(2023, 6, 26),
]

allmark = [
    24,
    25,
    27,
    23,
    27,
    22,
    30,
    28,
    26,
    29,
    28,
    26,
    28,
    23,
    28,
    28,
    25,
    27,
    28,
    30,
]

# Convert x_values to numerical values
dates = mdates.date2num(x_values)

# Fit a polynomial line to the data
coefficients = np.polyfit(dates, allmark, 1)
poly_line = np.poly1d(coefficients)
poly_values = poly_line(dates)

# Specify the date format for the x-axis labels
date_format = mdates.DateFormatter("%d-%m-%Y")

# Plot the data points and trend line
plt.figure()
plt.title("Mark Analysis")
plt.xlabel("Date")
plt.ylabel("Mark")
plt.gcf().autofmt_xdate()
plt.plot_date(dates, allmark, ":o", label="Data")  # Data points
plt.plot_date(dates, poly_values, "-", label="Trend Line")  # Trend line
plt.legend()
plt.show()
