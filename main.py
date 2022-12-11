from ecdsa import check_if_point_on_curve, find_n, check_if_public_key_is_correct, check_if_signature_is_valid, \
    replace_message

if __name__ == '__main__':
    G = (0, 1)
    q = 47
    a = -5
    b = 1
    assert check_if_point_on_curve(a, b, q, G), "Base point is not on curve"
    Q_a = (30, 22)
    n = find_n(a, q, Q_a)
    assert check_if_public_key_is_correct(a, b, q, n, Q_a), "Public key is incorrect"
    base_amount = 20
    new_amount = 200
    signature = (8, 10)
    r, s = signature
    z = base_amount
    s_inv = pow(s, -1, n)
    u1 = (z * s_inv) % n
    u2 = (r * s_inv) % n
    assert check_if_signature_is_valid(base_amount, a, q, n, signature, Q_a, G), "Real signature is invalid"
    new_signature = replace_message(new_amount, a, q, n, G, Q_a)
    assert check_if_signature_is_valid(new_amount, a, q, n, new_signature, Q_a, G), "Check signature is invalid"
