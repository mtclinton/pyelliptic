from pyelliptic.elliptic import CurveParams
import ctypes

bottom28Bits = 0xFFFFFFF


def get_28_bits_from_end(buf, shift):
    ret = 0
    for i in range(4):
        b = 0
        l = len(buf)
        if l > 0:
            b = buf[l - 1]
            if i != 3 or shift == 4:
                buf = buf[: l - 1]
        ret |= b << (8 * i) >> shift
    ret &= bottom28Bits
    return ret, buf


def p224_is_zero(a):
    minimal = [0] * 8
    p224_contract(minimal, a)

    isZero, isP = 0, 0
    for i, v in enumerate(minimal):
        isZero |= v
        isP |= v - p224P[i]

    isZero |= isZero >> 16
    isZero |= isZero >> 8
    isZero |= isZero >> 4
    isZero |= isZero >> 2
    isZero |= isZero >> 1

    isP |= isP >> 16
    isP |= isP >> 8
    isP |= isP >> 4
    isP |= isP >> 2
    isP |= isP >> 1

    result = isZero & isP
    result = (~result) & 1

    return result


def p224_from_big(out, _in):
    bytes = _in.to_bytes((_in.bit_length() + 7) // 8, "big")
    out[0], bytes = get_28_bits_from_end(bytes, 0)
    out[1], bytes = get_28_bits_from_end(bytes, 4)
    out[2], bytes = get_28_bits_from_end(bytes, 0)
    out[3], bytes = get_28_bits_from_end(bytes, 4)
    out[4], bytes = get_28_bits_from_end(bytes, 0)
    out[5], bytes = get_28_bits_from_end(bytes, 4)
    out[6], bytes = get_28_bits_from_end(bytes, 0)
    out[7], bytes = get_28_bits_from_end(bytes, 4)


def p224_to_big(p224_input):
    buf = bytearray(28)
    buf[27] = p224_input[0] & 0xFF
    buf[26] = (p224_input[0] >> 8) & 0xFF
    buf[25] = (p224_input[0] >> 16) & 0xFF
    buf[24] = ((p224_input[0] >> 24) & 0x0F) | ((p224_input[1] << 4) & 0xF0)

    buf[23] = p224_input[1] >> 4
    buf[22] = p224_input[1] >> 12
    buf[21] = p224_input[1] >> 20

    buf[20] = p224_input[2] & 0xFF
    buf[19] = (p224_input[2] >> 8) & 0xFF
    buf[18] = (p224_input[2] >> 16) & 0xFF
    buf[17] = ((p224_input[2] >> 24) & 0x0F) | ((p224_input[3] << 4) & 0xF0)

    buf[16] = p224_input[3] >> 4
    buf[15] = p224_input[3] >> 12
    buf[14] = p224_input[3] >> 20

    buf[13] = p224_input[4] & 0xFF
    buf[12] = (p224_input[4] >> 8) & 0xFF
    buf[11] = (p224_input[4] >> 16) & 0xFF
    buf[10] = ((p224_input[4] >> 24) & 0x0F) | ((p224_input[5] << 4) & 0xF0)

    buf[9] = p224_input[5] >> 4
    buf[8] = p224_input[5] >> 12
    buf[7] = p224_input[5] >> 20

    buf[6] = p224_input[6] & 0xFF
    buf[5] = (p224_input[6] >> 8) & 0xFF
    buf[4] = (p224_input[6] >> 16) & 0xFF
    buf[3] = ((p224_input[6] >> 24) & 0x0F) | ((p224_input[7] << 4) & 0xF0)

    buf[2] = p224_input[7] >> 4
    buf[1] = p224_input[7] >> 12
    buf[0] = p224_input[7] >> 20

    return int.from_bytes(buf, byteorder="big")


def p224_to_affine(x, y, z):
    zinv, zinvsq, outx, outy = [0] * 8, [0] * 8, [0] * 8, [0] * 8
    tmp = [0] * 15

    if p224_is_zero(z) == 1:
        return 0, 0

    p224_invert(zinv, z)
    p224_square(zinvsq, zinv, tmp)
    p224_mul(x, x, zinvsq, tmp)
    p224_mul(zinvsq, zinvsq, zinv, tmp)
    p224_mul(y, y, zinvsq, tmp)

    p224_contract(outx, x)
    p224_contract(outy, y)
    return p224_to_big(outx), p224_to_big(outy)


def p224_invert(out, _in):
    f1, f2, f3, f4 = [0] * 8, [0] * 8, [0] * 8, [0] * 8
    c = [0] * 15

    p224_square(f1, _in, c)
    p224_mul(f1, f1, _in, c)
    p224_square(f1, f1, c)
    p224_mul(f1, f1, _in, c)
    p224_square(f2, f1, c)
    p224_square(f2, f2, c)
    p224_square(f2, f2, c)
    p224_mul(f1, f1, f2, c)
    p224_square(f2, f1, c)
    for i in range(5):
        p224_square(f2, f2, c)
    p224_mul(f2, f2, f1, c)
    p224_square(f3, f2, c)
    for i in range(11):
        p224_square(f3, f3, c)
    p224_mul(f2, f3, f2, c)
    p224_square(f3, f2, c)
    for i in range(23):
        p224_square(f3, f3, c)
    p224_mul(f3, f3, f2, c)
    p224_square(f4, f3, c)
    for i in range(47):
        p224_square(f4, f4, c)
    p224_mul(f3, f3, f4, c)
    p224_square(f4, f3, c)
    for i in range(23):
        p224_square(f4, f4, c)
    p224_mul(f2, f4, f2, c)
    for i in range(6):
        p224_square(f2, f2, c)
    p224_mul(f1, f1, f2, c)
    p224_square(f1, f1, c)
    p224_mul(f1, f1, _in, c)
    for i in range(97):
        p224_square(f1, f1, c)
    p224_mul(out, f1, f3, c)


def p224_add_jacobian(x3, y3, z3, x1, y1, z1, x2, y2, z2):
    z1z1, z2z2, u1, u2, s1, s2, h, i, j, r, v = (
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
        [0] * 8,
    )
    c = [0] * 15

    z1IsZero = p224_is_zero(z1)
    z2IsZero = p224_is_zero(z2)

    p224_square(z1z1, z1, c)
    p224_square(z2z2, z2, c)
    p224_mul(u1, x1, z2z2, c)
    p224_mul(u2, x2, z1z1, c)
    p224_mul(s1, z2, z2z2, c)
    p224_mul(s1, y1, s1, c)
    p224_mul(s2, z1, z1z1, c)
    p224_mul(s2, y2, s2, c)
    p224_sub(h, u2, u1)
    p224_reduce(h)
    xEqual = p224_is_zero(h)

    for j in range(8):
        i[j] = h[j] << 1
    p224_reduce(i)
    p224_square(i, i, c)
    p224_mul(j, h, i, c)
    p224_sub(r, s2, s1)
    p224_reduce(r)
    yEqual = p224_is_zero(r)

    if xEqual == 1 and yEqual == 1 and z1IsZero == 0 and z2IsZero == 0:
        p224_double_jacobian(x3, y3, z3, x1, y1, z1)
        return

    for i in range(8):
        r[i] <<= 1
    p224_reduce(r)
    p224_mul(v, u1, i, c)
    p224_add(z1z1, z1z1, z2z2)
    p224_add(z2z2, z1, z2)
    p224_reduce(z2z2)
    p224_square(z2z2, z2z2, c)
    p224_sub(z3, z2z2, z1z1)
    p224_reduce(z3)
    p224_mul(z3, z3, h, c)

    for i in range(8):
        z1z1[i] = v[i] << 1
    p224_add(z1z1, j, z1z1)
    p224_reduce(z1z1)
    p224_square(x3, r, c)
    p224_sub(x3, x3, z1z1)
    p224_reduce(x3)

    for i in range(8):
        s1[i] <<= 1
    p224_mul(s1, s1, j, c)
    p224_sub(z1z1, v, x3)
    p224_reduce(z1z1)
    p224_mul(z1z1, z1z1, r, c)
    p224_sub(y3, z1z1, s1)
    p224_reduce(y3)

    p224_copy_conditional(x3, x2, z1IsZero)
    p224_copy_conditional(x3, x1, z2IsZero)
    p224_copy_conditional(y3, y2, z1IsZero)
    p224_copy_conditional(y3, y1, z2IsZero)
    p224_copy_conditional(z3, z2, z1IsZero)
    p224_copy_conditional(z3, z1, z2IsZero)


def p224_double_jacobian(x3, y3, z3, x1, y1, z1):
    delta, gamma, beta, alpha, t = [0] * 8, [0] * 8, [0] * 8, [0] * 8, [0] * 8
    c = [0] * 16

    p224_square(delta, z1, c)
    p224_square(gamma, y1, c)
    p224_mul(beta, x1, gamma, c)

    t = [x1[i] + delta[i] for i in range(8)]
    for i in range(8):
        t[i] += t[i] << 1
    p224_reduce(t)
    p224_sub(alpha, x1, delta)
    p224_reduce(alpha)
    p224_mul(alpha, alpha, t, c)

    p224_add(z3, y1, z1)
    p224_reduce(z3)
    p224_square(z3, z3, c)
    p224_sub(z3, z3, gamma)
    p224_reduce(z3)
    p224_sub(z3, z3, delta)
    p224_reduce(z3)

    for i in range(8):
        delta[i] = beta[i] << 3
    p224_reduce(delta)
    p224_square(x3, alpha, c)
    p224_sub(x3, x3, delta)
    p224_reduce(x3)

    for i in range(8):
        beta[i] <<= 2
    p224_sub(beta, beta, x3)
    p224_reduce(beta)
    p224_square(gamma, gamma, c)
    for i in range(8):
        gamma[i] <<= 3
    p224_reduce(gamma)
    p224_mul(y3, alpha, beta, c)
    p224_sub(y3, y3, gamma)
    p224_reduce(y3)


def p224_copy_conditional(out, in_, control):
    control = ctypes.c_uint32(control << 31).value
    control = (control & 0x80000000) >> 31

    for i in range(8):
        out[i] ^= (out[i] ^ in_[i]) & control


def p224_scalar_mult(outX, outY, outZ, inX, inY, inZ, scalar):
    xx, yy, zz = [0] * 8, [0] * 8, [0] * 8
    for i in range(8):
        outX[i] = 0
        outY[i] = 0
        outZ[i] = 0

    for byte in scalar:
        for bitNum in range(8):
            p224_double_jacobian(outX, outY, outZ, outX, outY, outZ)
            bit = (byte >> (7 - bitNum)) & 1
            p224_add_jacobian(xx, yy, zz, inX, inY, inZ, outX, outY, outZ)
            p224_copy_conditional(outX, xx, bit)
            p224_copy_conditional(outY, yy, bit)
            p224_copy_conditional(outZ, zz, bit)


class p224Curve(CurveParams):
    def __init__(self):
        super().__init__()
        self.gx = [0] * 8
        self.gy = [0] * 8
        self.b = [0] * 8

    def params(self):
        return {
            "P": self.P,
            "N": self.N,
            "B": self.B,
            "Gx": self.Gx,
            "Gy": self.Gy,
            "BitSize": self.BitSize,
        }

    def is_on_curve(self, bigX, bigY):
        x, y = [0] * 8, [0] * 8
        p224_from_big(x, bigX)
        p224_from_big(y, bigY)

        # y² = x³ - 3x + b
        tmp = [0] * 15
        x3 = [0] * 8
        p224_square(x3, x, tmp)
        p224_mul(x3, x3, x, tmp)

        for i in range(8):
            x[i] *= 3

        p224_sub(x3, x3, x)
        p224_reduce(x3)

        p224_add(x3, x3, self.b)

        p224_contract(x3, x3)

        p224_square(y, y, tmp)
        p224_contract(y, y)
        for i in range(8):
            if y[i] != x3[i]:
                return False
        return True


p224_curve = p224Curve()


def initP224():
    p224_curve.P = int(
        "26959946667150639794667015087019630673557916260026308143510066298881"
    )
    p224_curve.N = int(
        "26959946667150639794667015087019625940457807714424391721682722368061"
    )
    p224_curve.B = int("b4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4", 16)
    p224_curve.Gx = int("b70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21", 16)
    p224_curve.Gy = int("bd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34", 16)
    p224_curve.BitSize = 224

    p224_from_big(p224_curve.gx, p224_curve.Gx)
    p224_from_big(p224_curve.gy, p224_curve.Gy)
    p224_from_big(p224_curve.b, p224_curve.B)


def p224():
    initP224()
    return p224_curve


# p224P is the order of the field, represented as a p224FieldElement.
p224P = [1, 0, 0, 0xFFFF000, 0xFFFFFFF, 0xFFFFFFF, 0xFFFFFFF, 0xFFFFFFF]


def p224_add(out, a, b):
    for i in range(8):
        out[i] = a[i] + b[i]


two31p3 = (1 << 31) + (1 << 3)
two31m3 = (1 << 31) - (1 << 3)
two31m15m3 = (1 << 31) - (1 << 15) - (1 << 3)

p224ZeroModP31 = [
    two31p3,
    two31m3,
    two31m3,
    two31m15m3,
    two31m3,
    two31m3,
    two31m3,
    two31m3,
]


def p224_sub(out, a, b):
    for i in range(8):
        out[i] = a[i] + p224ZeroModP31[i] - b[i]


two63p35 = (1 << 63) + (1 << 35)
two63m35 = (1 << 63) - (1 << 35)
two63m35m19 = (1 << 63) - (1 << 35) - (1 << 19)

p224ZeroModP63 = [
    two63p35,
    two63m35,
    two63m35,
    two63m35,
    two63m35m19,
    two63m35,
    two63m35,
    two63m35,
]

bottom12Bits = 0xFFF


def p224_mul(out, a, b, tmp):
    for i in range(15):
        tmp[i] = 0

    for i in range(8):
        for j in range(8):
            tmp[i + j] += a[i] * b[j]

    p224_reduce_large(out, tmp)


def p224_square(out, a, tmp):
    for i in range(15):
        tmp[i] = 0

    for i in range(8):
        for j in range(i + 1):
            r = a[i] * a[j]
            if i == j:
                tmp[i + j] += r
            else:
                tmp[i + j] += r << 1

    p224_reduce_large(out, tmp)


def p224_reduce_large(out, _in):
    for i in range(8):
        _in[i] += p224ZeroModP63[i]

    for i in range(14, 7, -1):
        _in[i - 8] -= _in[i]
        _in[i - 5] += (_in[i] & 0xFFFF) << 12
        _in[i - 4] += _in[i] >> 16
    _in[8] = 0

    for i in range(1, 8):
        _in[i + 1] += _in[i] >> 28
        out[i] = _in[i] & bottom28Bits
    _in[0] -= _in[8]
    out[3] += (_in[8] & 0xFFFF) << 12
    out[4] += _in[8] >> 16

    out[0] = _in[0] & bottom28Bits
    out[1] += (_in[0] >> 28) & bottom28Bits
    out[2] += _in[0] >> 56


def p224_reduce(a):
    for i in range(7):
        a[i + 1] += a[i] >> 28
        a[i] &= bottom28Bits

    top = a[7] >> 28
    a[7] &= bottom28Bits

    mask = top
    mask |= mask >> 2
    mask |= mask >> 1

    mask <<= 31
    mask &= (1 << 32) - 1

    import ctypes

    mask = ctypes.c_uint32(ctypes.c_int32(mask).value >> 31).value

    a[0] -= top
    a[3] += top << 12

    a[3] -= 1 & mask
    a[2] += mask & ((1 << 28) - 1)
    a[1] += ctypes.c_uint32(mask & ((1 << 28) - 1)).value
    a[0] += mask & (1 << 28)


def p224_contract(out, _in):
    out[:] = _in[:]
    for i in range(7):
        out[i + 1] += out[i] >> 28
        out[i] &= bottom28Bits
    top = out[7] >> 28
    out[7] &= bottom28Bits

    out[0] -= top
    out[3] += top << 12

    for i in range(3):
        mask = ctypes.c_uint32(ctypes.c_int32(out[i] >> 31).value).value
        out[i] += (1 << 28) & mask
        out[i + 1] -= 1 & mask

    for i in range(3, 7):
        out[i + 1] += out[i] >> 28
        out[i] &= bottom28Bits
    top = out[7] >> 28
    out[7] &= bottom28Bits

    out[0] -= top
    out[3] += top << 12

    for i in range(3):
        mask = ctypes.c_uint32(ctypes.c_int32(out[i]).value >> 31).value
        out[i] += (1 << 28) & mask
        out[i + 1] -= 1 & mask

    top4_all_ones = 0xFFFFFFFF
    for i in range(4, 8):
        top4_all_ones &= out[i]
    top4_all_ones |= 0xF0000000

    # Now we replicate any zero bits to all the bits in top4_all_ones.
    top4_all_ones &= top4_all_ones >> 16
    top4_all_ones &= top4_all_ones >> 8
    top4_all_ones &= top4_all_ones >> 4
    top4_all_ones &= top4_all_ones >> 2
    top4_all_ones &= top4_all_ones >> 1
    top4_all_ones = ctypes.c_uint32(
        ctypes.c_int32(top4_all_ones << 31).value >> 31
    ).value

    bottom3NonZero = out[0] | out[1] | out[2]
    bottom3NonZero |= bottom3NonZero >> 16
    bottom3NonZero |= bottom3NonZero >> 8
    bottom3NonZero |= bottom3NonZero >> 4
    bottom3NonZero |= bottom3NonZero >> 2
    bottom3NonZero |= bottom3NonZero >> 1
    bottom3NonZero = ctypes.c_uint32(
        ctypes.c_int32(bottom3NonZero << 31).value >> 31
    ).value

    n = out[3] - 0xFFFF000
    out3Equal = n
    out3Equal |= out3Equal >> 16
    out3Equal |= out3Equal >> 8
    out3Equal |= out3Equal >> 4
    out3Equal |= out3Equal >> 2
    out3Equal |= out3Equal >> 1
    out3Equal = ~int(ctypes.c_int32(out3Equal << 31).value >> 31) & 0xFFFFFFFF

    out3GT = ~int(n) >> 31 & 0xFFFFFFFF

    mask = top4_all_ones & ((out3Equal & bottom3NonZero) | out3GT)
    out[0] -= 1 & mask
    out[3] -= 0xFFFF000 & mask
    out[4] -= 0xFFFFFFF & mask
    out[5] -= 0xFFFFFFF & mask
    out[6] -= 0xFFFFFFF & mask
    out[7] -= 0xFFFFFFF & mask
