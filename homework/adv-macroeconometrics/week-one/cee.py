from utils.read_data import read_data
from utils.plot import plot_var
from utils.var import var


if __name__ == "__main__":
    df = read_data("data/cee.xls", f = "1963Q3")

    standard_res = var(df, lags = 4)
    plot_var(standard_res, impulse = "FF", folder="cee/ex")

    standard_res = var(df, trend="c", maxlags=15, ic = "aic")
    plot_var(standard_res, impulse = "FF", folder="cee/aic")
