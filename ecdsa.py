import numpy as np
import typing as tp


def point_multiplication(a: int, p: int, point: tp.Optional[tuple[int, int]], m: int):
    res = point
    for i in range(m - 1):
        res = add_points(a, p, point, res)
    return res


def check_if_point_on_curve(a: int, b: int, p: int, point: tp.Optional[tuple[int, int]]) -> bool:
    if point is None:
        return True
    x, y = point
    return (y ** 2 - x ** 3 - a * x - b) % p == 0


def add_points(a: int, p: int, first_point: tp.Optional[tuple[int, int]],
               second_point: tp.Optional[tuple[int, int]]) -> tp.Optional[tuple[int, int]]:
    if first_point is None:
        return second_point
    elif second_point is None:
        return first_point

    x_p, y_p = first_point
    x_q, y_q = second_point

    if x_p == x_q and y_p == (-y_q % p):
        return None

    if first_point != second_point:
        m = (y_q - y_p) * pow(x_q - x_p, -1, p) % p
    else:
        m = (3 * (x_p ** 2) + a) * pow(2 * y_p, -1, p)
    x = (m ** 2 - x_p - x_q) % p
    return x, (m * (x_p - x) - y_p) % p


def find_n(a: int, p: int, Q_a: tp.Optional[tuple[int, int]]):
    if Q_a == (0, 0):
        return 1
    i = 1
    res = Q_a
    while True:
        res = add_points(a, p, Q_a, res)
        i += 1
        if res is None:
            return i


def check_if_public_key_is_correct(a: int, b: int, p: int, n: int, Q_a: tp.Optional[tuple[int, int]]):
    return Q_a is not None and check_if_point_on_curve(a, b, p, Q_a) and point_multiplication(a, p, Q_a, n) is None


def check_if_signature_is_valid(amount: int, a: int, p: int, n: int, signature: tp.Optional[tuple[int, int]],
                                Q_a: tp.Optional[tuple[int, int]], G: tp.Optional[tuple[int, int]]):
    r, s = signature
    z = amount % n
    s_inv = pow(s, -1, n)
    u1 = (z * s_inv) % n
    u2 = (r * s_inv) % n
    point = add_points(a, p,
                       point_multiplication(a, p, G, u1),
                       point_multiplication(a, p, Q_a, u2))
    return point is None or (point[0] % n) == (r % n)


def find_private_key(a: int, p: int, G: tp.Optional[tuple[int, int]], Q_a: tp.Optional[tuple[int, int]]) -> int:
    if Q_a == G:
        return 1
    i = 1
    res = G
    while True:
        res = add_points(a, p, G, res)
        i += 1
        if res == Q_a:
            return i


def replace_message(new_amount: int, a: int, p: int, n: int, G: tp.Optional[tuple[int, int]],
                    Q_a: tp.Optional[tuple[int, int]]):
    z = new_amount % n
    da = find_private_key(a, p, G, Q_a)

    r = 0
    s = 0

    while s == 0 or r == 0:
        k = np.random.randint(1, n)
        x1, y1 = point_multiplication(a, p, G, k)
        r = x1 % n
        k_inv = pow(k, -1, n)
        s = (k_inv * (z + r * da)) % n
    return (r, s)
