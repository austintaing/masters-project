import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# Generates sampling of points to plot a polynomial function
def reg_eq(coefficients, x):
    y = 0
    for i in range(len(coefficients)):
        y += coefficients[i] * x ** i
    return y


def main():
    result_file = open("Results - Hurricane.csv", 'r', encoding='utf-8')
    mode = int(input("Result number: "))
    data_x = []
    data_y = []

    for line in result_file:
        parts = line.split(',')
        data_x.append(float(parts[2*mode-1]))
        data_y.append(float(parts[2*mode]))

    plt.plot(data_x, data_y, 'bo')
    axis_min = min(min(data_x), min(data_y))
    axis_max = max(max(data_x), max(data_y))
    axis_shift = (axis_max - axis_min) / 10
    axis_min -= axis_shift
    axis_max += axis_shift

    x = np.linspace(axis_min, axis_max, 100)
    y = np.linspace(axis_min, axis_max, 100)
    plt.plot(x, y, label="no change (y = x)")

    slope, intercept, r_value, p_value, std_err = stats.linregress(data_x, data_y)
    y_reg = reg_eq([intercept, slope], x)
    plt.plot(x, y_reg, label="line of best fit (r^2="+str(round(r_value**2, 4))+")")
    print("Slope:", slope)
    print("Intercept:", intercept)
    print("r-squared:", r_value**2)

    plt.axis([axis_min, axis_max, axis_min, axis_max])

    #plt.title("Measure")
    #plt.xlabel("Base")
    #plt.ylabel("Experiment group")
    plt.legend()
    plt.show()
    result_file.close()


main()
