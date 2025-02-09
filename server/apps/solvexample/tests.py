from urllib.parse import quote_plus

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TestSolveEquations(TestCase):
    def test_equations(self):
        equations = {"to_solve": "x+5=12", "to_find": "x", "type": "Рівняння"}
        inequality = {"to_solve": "x + 5 >= 12", "to_find": "x", "type": "Нерівність"}
        eq_system = {
            "to_solve": "x + 5 = 12, y - 5 = 12",
            "to_find": "x, y",
            "type": "Система",
        }
        ineq_system = {
            "to_solve": "x + 5 >= 12, y - 5 >= 12",
            "to_find": "x, y",
            "type": "Система нерівностей",
        }
        integrals = {"to_solve": "sin(x)", "to_find": "x", "type": "Первісна"}
        derivatives = {"to_solve": "sin(x)", "to_find": "x", "type": "Похідна"}

        for eq in (
            equations,
            inequality,
            eq_system,
            ineq_system,
            integrals,
            derivatives,
        ):
            url = reverse("equations") + "?example={}&to-find={}&type={}".format(
                quote_plus(eq["to_solve"]),
                quote_plus(eq["to_find"]),
                quote_plus(eq["type"]),
            )

            response = self.client.get(url)

            self.assertIsNotNone(response.context["solved_example"])
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_percents(self):
        first_type = {
            "example": 125,
            "percent": 13,
            "num": None,
            "type": "від відсотка x",
        }
        second_type = {
            "example": 1681,
            "percent": 100,
            "num": 567,
            "type": "від числа x",
        }

        for eq in (first_type, second_type):
            url = reverse("percents") + "?example={}&percent={}&num={}&type={}".format(
                eq["example"], eq["percent"], eq["num"], eq["type"]
            )
            response = self.client.get(url)

            self.assertIsNotNone(response.context["solved_example"])
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_matrix(self):
        add_example = {"matrixA": "[1, 2, 3]", "matrixB": "[5, 6, 7]", "operator": "+"}
        sub_example = {"matrixA": "[1, 2, 3]", "matrixB": "[5, 6, 7]", "operator": "-"}
        multiply_example = {
            "matrixA": "[1], [2], [3]",
            "matrixB": "[5, 6, 7]",
            "operator": "*",
        }

        for eq in (add_example, sub_example, multiply_example):
            url = reverse("matrices") + "?matrixA={}&matrixB={}&operator={}".format(
                quote_plus(eq["matrixA"]),
                quote_plus(eq["matrixB"]),
                quote_plus(eq["operator"]),
            )
            response = self.client.get(url)

            self.assertIsNotNone(response.context["solved_example"])
            self.assertEqual(response.status_code, status.HTTP_200_OK)
