import numpy as np
import pandas as pd

from numpy.linalg import inv

from utils import transform, matrix, printing, instruments

from cov_est import white_var, nw_corrected, white_var_2sls
from tests import panel_dw

# --- Typings

from typing import List, NewType, Union, Tuple

# TODO: Instruments can be passed as a dataframe or as a number of lags of the regressors
Instruments = NewType("Instruments", Union[pd.DataFrame, int])


def lagged_gmm(
    data: pd.DataFrame, dependent: str,
    lag_inst=1,
    regressors: List[str] = [],
    het_robust=False, gmm=False,
    verbose=1
):

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lag_inst < 1:
        raise ValueError("Specify a number for lag_inst")

    Z, W, Y, N, T = instruments.extract_regs(
        data, dependent, regressors, lag_inst)

    W_f = Z@inv(Z.T@Z)@Z.T@W

    beta = inv(W_f.T@W_f)@W_f.T@Y

    resid = Y - W@beta

    if gmm:

        # Generalize the IV for Hansen, 1982

        omega = np.diag(np.diag(resid@resid.T))

        Pi = inv(Z.T@omega@Z)

        beta = inv(W.T@Z@Pi@Z.T@W)@W.T@Z@Pi@Z.T@Y

        resid = Y - W@beta

    # FIXME: How to compute this?!
    cov = np.zeros((3, 3)) if gmm else white_var_2sls(W, W_f, resid)

    resid_by_n = resid.reshape(T, N, order="F")
    durbin_watson = panel_dw(resid_by_n, N, T)

    if verbose > 0:
        printing.pprint(
            beta, cov, regressors, durbin_watson,
            title="GMM Estimation" if gmm else "IV Estimation"
        )

    return beta, resid_by_n, cov, durbin_watson


if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    lagged_gmm(
        data, "S/Y",
        regressors=["d(lnY)", "INF"], lag_inst=1
    )

    lagged_gmm(
        data, "S/Y",
        regressors=["d(lnY)", "INF"], lag_inst=1,
        gmm=True
    )