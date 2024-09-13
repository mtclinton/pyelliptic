from elliptic import CurveParams

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
        import ctypes

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
        mask = int(int(out[i]) >> 31)
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
    top4_all_ones = int(int(top4_all_ones << 31) >> 31)

    bottom3NonZero = out[0] | out[1] | out[2]
    bottom3NonZero |= bottom3NonZero >> 16
    bottom3NonZero |= bottom3NonZero >> 8
    bottom3NonZero |= bottom3NonZero >> 4
    bottom3NonZero |= bottom3NonZero >> 2
    bottom3NonZero |= bottom3NonZero >> 1
    # bottom3NonZero = uint32(int32(bottom3NonZero<<31) >> 31)

    n = out[3] - 0xFFFF000
    out3Equal = n
    out3Equal |= out3Equal >> 16
    out3Equal |= out3Equal >> 8
    out3Equal |= out3Equal >> 4
    out3Equal |= out3Equal >> 2
    out3Equal |= out3Equal >> 1
    # out3Equal = ^uint32(int32(out3Equal<<31) >> 31)
    #
    # out3GT = ^uint32(int32(n) >> 31)
    #
    # mask = top4AllOnes & ((out3Equal & bottom3NonZero) | out3GT)
    out[0] -= 1 & mask
    out[3] -= 0xFFFF000 & mask
    out[4] -= 0xFFFFFFF & mask
    out[5] -= 0xFFFFFFF & mask
    out[6] -= 0xFFFFFFF & mask
    out[7] -= 0xFFFFFFF & mask
