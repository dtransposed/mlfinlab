# pylint: disable=missing-module-docstring
import numpy as np
import cvxpy as cp
from mlfinlab.online_portfolio_selection import FTL


class FTRL(FTL):
    """
    This class implements the Follow the Regularized Leader
    """
    def __init__(self, beta=0.1):
        self.beta = beta
        super(FTRL, self).__init__()

    def update_weight(self, _weights, _relative_return, _time):
        """

        :param _weights:
        :param _relative_return:
        :param _time:
        :return:
        """
        return self.optimize(_relative_return[:_time], _solver=cp.SCS)

    # optimize the weight that maximizes the returns
    def optimize(self, _optimize_array, _solver=None):
        length_of_time = _optimize_array.shape[0]
        number_of_assets = _optimize_array.shape[1]
        if length_of_time == 1:
            best_idx = np.argmax(_optimize_array)
            weight = np.zeros(number_of_assets)
            weight[best_idx] = 1
            return weight

        # initialize weights
        weights = cp.Variable(self.number_of_assets)

        # used cp.log and cp.sum to make the cost function a convex function
        # multiplying continuous returns equates to summing over the log returns
        portfolio_return = cp.sum(cp.log(_optimize_array * weights)) - self.beta * cp.norm(weights) / 2

        # Optimization objective and constraints
        allocation_objective = cp.Maximize(portfolio_return)
        allocation_constraints = [
                cp.sum(weights) == 1,
                cp.min(weights) >= 0
        ]
        # Define and solve the problem
        problem = cp.Problem(
                objective=allocation_objective,
                constraints=allocation_constraints
        )
        if _solver:
            problem.solve(solver=_solver)
        else:
            problem.solve()
        return weights.value