import unittest
from numpy.testing import assert_allclose
from task import Task


class TestTask(unittest.TestCase):
    def test_solve_linear_system(self):
        size = 50
        task = Task(size=size)
        task.work()
        ax = task.a @ task.x
        assert_allclose(ax, task.b, rtol=1e-6, atol=1e-8)


if __name__ == "__main__":
    unittest.main()
