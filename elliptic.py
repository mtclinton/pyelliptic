import os


class CurveParams:
    def __init__(self):
        self.P = 0  # the order of the underlying field
        self.N = 0  # the order of the base point
        self.B = 0  # the constant of the curve equation
        self.Gx = 0  # (x,y) of the base point
        self.Gy = 0  # (x,y) of the base point
        self.BitSize = 0  # the size of the underlying field

    def is_on_curve(self, x, y):
        # y² = x³ - 3x + b
        y2 = y * y
        y2 = y2 % self.P

        x3 = x**3

        threeX = 3 * x

        x3 = x3 - threeX + self.B
        x3 = x3 % self.P

        return x3 - y2 == 0

    def z_for_affine(self, x, y):
        if x != 0 or y != 0:
            return 1
        return 0

    def affine_from_jacobian(self, x, y, z):
        if z == 0:
            return 0, 0

        zinv = pow(z, -1, self.P)
        zinvsq = zinv * zinv

        xOut = x * zinvsq
        xOut = xOut % self.P
        zinvsq = zinvsq * zinv
        yOut = y * zinvsq
        yOut = yOut % self.P
        return xOut, yOut

    def add(self, x1, y1, x2, y2):
        z1 = self.z_for_affine(x1, y1)
        z2 = self.z_for_affine(x2, y2)
        return self.affine_from_jacobian(self.add_jacobian(x1, y1, z1, x2, y2, z2))

    def add_jacobian(self, x1, y1, z1, x2, y2, z2):
        if z1 == 0:
            x3 = x2
            y3 = y2
            z3 = z2
            return x3, y3, z3

        if z2 == 0:
            x3 = x1
            y3 = y1
            z3 = z1
            return x3, y3, z3

        z1z1 = z1 * z1
        z1z1 = z1z1 % self.P
        z2z2 = z2 * z2
        z2z2 = z2z2 % self.P

        u1 = x1 * z2z2
        u1 = u1 % self.P
        u2 = x2 * z1z1
        u2 = u2 % self.P
        h = u2 - u1
        xEqual = h == 0
        if h < 0:
            h += self.P
        i = h << 1
        i = i * i
        j = h * i

        s1 = y1 * z2

        s1 *= z2z2
        s1 = s1 % self.P
        s2 = y2 * z1

        s2 = s2 * z1z1

        s2 = s2 % self.P

        r = s2 - s1
        if r < 0:
            r += self.P
        yEqual = r == 0
        if xEqual and yEqual:
            return self.double_jacobian(x1, y1, z1)
        r = r << 1
        v = u1 * i

        x3 = r
        x3 = x3 * x3
        x3 -= j
        x3 -= v
        x3 -= v
        x3 = x3 % self.P

        y3 = r
        v -= x3
        y3 *= v
        s1 *= j
        s1 = s1 << 1
        y3 -= s1
        y3 = y3 % self.P

        z3 = z1 + z2
        z3 *= z3
        z3 -= z1z1
        z3 -= z2z2
        z3 *= h
        z3 = z3 % self.P

        return x3, y3, z3

    def double(self, x1, y1):
        z1 = self.z_for_affine(x1, y1)
        return self.affine_from_jacobian(self.double_jacobian(x1, y1, z1))

    def double_jacobian(self, x, y, z):
        delta = z * z

        delta = delta % self.P
        gamma = y * y
        gamma = gamma % self.P
        alpha = x - delta

        if alpha < 0:
            alpha += self.P
        alpha2 = x + delta
        alpha = alpha * alpha2

        alpha2 = alpha

        alpha = alpha << 1
        alpha += alpha2

        alpha2 = x * gamma
        beta = alpha2

        x3 = alpha * alpha
        beta8 = beta << 3
        x3 -= beta8
        if x3 < 0:
            x3 += self.P
        x3 = x3 % self.P

        z3 = y + z
        z3 *= z3
        z3 -= gamma
        if z3 < 0:
            z3 += self.P
        z3 -= delta
        if z3 < 0:
            z3 += self.P
        z3 = z3 % self.P

        beta = beta << 2
        beta -= x3
        if beta < 0:
            beta += self.P
        y3 = alpha * beta

        gamma *= gamma
        gamma = gamma << 3
        gamma = gamma % self.P

        y3 -= gamma
        if y3 < 0:
            y3 += self.P
        y3 = y3 % self.P

        return x3, y3, z3

    def scalar_mult(self, bx, by, k):
        bz = 1
        x, y, z = 0, 0, 0
        for b in k:
            for _ in range(8):
                x, y, z = self.double_jacobian(x, y, z)
                if b & 0x80 == 0x80:
                    x, y, z = self.add_jacobian(bx, by, bz, x, y, z)
                b = b << 1
        return self.affine_from_jacobian(x, y, z)

    def scalar_base_mult(self, k):

        return self.scalar_mult(self.Gx, self.Gy, k)


mask = [0xFF, 0x1, 0x3, 0x7, 0xF, 0x1F, 0x3F, 0x7F]


def generate_key(curve):
    bit_size = 384
    byte_len = (bit_size + 7) // 8
    priv = bytearray(byte_len)
    x, y = 0, 0
    while x == 0:
        priv = os.urandom(byte_len)
        priv = (
            (priv[0] & mask[bit_size % 8]).to_bytes(1, byteorder="big")
            + (priv[1] ^ 0x42).to_bytes(1, byteorder="big")
            + priv[2:]
        )

        x, y = curve.scalar_base_mlt(priv)

    return priv, x, y


def marshall(curve, x, y):
    byte_len = (curve.BitSize + 7) // 8

    ret = bytearray(1 + 2 * byte_len)
    ret[0] = 4  # uncompressed point

    x_bytes = x.to_bytes((x.bit_length() + 7) // 8, byteorder="big")
    ret[1 + byte_len - len(x_bytes) : 1 + byte_len] = x_bytes
    y_bytes = y.to_bytes((y.bit_length() + 7) // 8, byteorder="big")
    ret[1 + 2 * byte_len - len(y_bytes) : 1 + 2 * byte_len] = y_bytes
    return bytes(ret)


def unmarshall(curve, data):
    byte_len = (curve.BitSize + 7) >> 3
    if len(data) != 1 + 2 * byte_len:
        return 0, 0
    if data[0] != 4:
        return 0, 0

    x = int.from_bytes(data[1 : 1 + byte_len], byteorder="big")
    y = int.from_bytes(data[1 + byte_len :], byteorder="big")
    return x, y
