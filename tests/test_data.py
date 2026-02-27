from vrp.data import sample_problem_data


def test_distance_matrix_dimensions() -> None:
    problem = sample_problem_data()
    n = 1 + len(problem.customers)
    assert len(problem.distance_matrix) == n
    assert all(len(row) == n for row in problem.distance_matrix)
