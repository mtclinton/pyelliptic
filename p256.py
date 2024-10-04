from elliptic import CurveParams


class p256Curve(CurveParams):
    def __init__(self):
        super().__init__()

    def params(self):
        return {
            "P": self.P,
            "N": self.N,
            "B": self.B,
            "Gx": self.Gx,
            "Gy": self.Gy,
            "BitSize": self.BitSize,
        }

    def get_scalar(self, out, _in):
        n = int.from_bytes(_in, 'big')
        if n >= self.N:
            n = n % self.N
            l = (n.bit_length() + 7) // 8
            scalar_bytes = int.to_bytes(n, byteorder="big", length=l)
        else:
            scalar_bytes = _in
        for i, v in enumerate(scalar_bytes):
            out[len(scalar_bytes) - (1 + i)] = v

    def scalar_mult(self, bigX1, bigY1, scalar):
        scalarReversed = [0] * 32
        self.get_scalar(scalarReversed, scalar)
        breakpoint()