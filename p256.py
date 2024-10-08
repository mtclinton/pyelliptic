from elliptic import CurveParams
import ctypes

p256Limbs = 9
bottom29Bits = 0x1FFFFFFF
bottom28Bits = 0xFFFFFFF

# p256One is the number 1 as a field element.
p256One = [2, 0, 0, 0xFFFF800, 0x1FFFFFFF, 0xFFFFFFF, 0x1FBFFFFF, 0x1FFFFFF, 0]
p256Zero = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# p256P is the prime modulus as a field element.
p256P = [0x1FFFFFFF, 0xFFFFFFF, 0x1FFFFFFF, 0x3FF, 0, 0, 0x200000, 0xF000000, 0xFFFFFFF]
# p2562P is the twice prime modulus as a field element.
p2562P = [
    0x1FFFFFFE,
    0xFFFFFFF,
    0x1FFFFFFF,
    0x7FF,
    0,
    0,
    0x400000,
    0xE000000,
    0x1FFFFFFF,
]

two30m2 = (1 << 30) - (1 << 2)
two30p13m2 = (1 << 30) + (1 << 13) - (1 << 2)
two31m2 = (1 << 31) - (1 << 2)
two31m3 = (1 << 31) - (1 << 3)
two31p24m2 = (1 << 31) + (1 << 24) - (1 << 2)
two30m27m2 = (1 << 30) - (1 << 27) - (1 << 2)


# p256Zero31 is 0 mod p.
p256Zero31 = [
    two31m3,
    two30m2,
    two31m2,
    two30p13m2,
    two31m2,
    two30m2,
    two31p24m2,
    two30m27m2,
    two31m2,
]


def non_zero_to_all_ones(x):
    return (ctypes.c_uint32(x - 1).value >> 31) - 1


def p256_reduce_carry(inout, carry):
    carry_mask = non_zero_to_all_ones(carry)

    inout[0] += carry << 1
    inout[3] += 0x10000000 & carry_mask
    inout[3] -= carry << 11
    inout[4] += (0x20000000 - 1) & carry_mask
    inout[5] += (0x10000000 - 1) & carry_mask
    inout[6] += (0x20000000 - 1) & carry_mask
    inout[6] -= carry << 22
    inout[7] -= 1 & carry_mask
    inout[7] += carry << 25


def p256_reduce_degree(out, tmp):
    tmp2 = [0] * 18
    tmp2[0] = ctypes.c_uint32(tmp[0]).value & bottom29Bits

    tmp2[1] = (ctypes.c_uint32(tmp[0]).value >> 29) | (
        ctypes.c_uint32(tmp[0] >> 32).value << 3
    ) & bottom28Bits
    tmp2[1] += ctypes.c_uint32(tmp[1]).value & bottom28Bits
    carry = ctypes.c_uint32(tmp2[1]).value >> 28
    tmp2[1] &= bottom28Bits

    i = 2
    while True:
        # print("-----------------------------------")
        # print(i)
        # print(tmp2)
        tmp2[i] = ctypes.c_uint32(tmp[i - 2] >> 32).value >> 25
        tmp2[i] += ctypes.c_uint32(tmp[i - 1]).value >> 28
        tmp2[i] += (
            ctypes.c_uint32((ctypes.c_uint32(tmp[i - 1] >> 32).value) << 4).value
            & bottom29Bits
        )
        tmp2[i] += ctypes.c_uint32(tmp[i]).value & bottom29Bits
        tmp2[i] += carry

        carry = ctypes.c_uint32(tmp2[i]).value >> 29
        tmp2[i] &= bottom29Bits

        i += 1
        if i == 17:
            break

        tmp2[i] = (ctypes.c_uint32(tmp[i - 2] >> 32).value) >> 25

        tmp2[i] += ctypes.c_uint32(tmp[i - 1]).value >> 29

        tmp2[i] += (ctypes.c_uint32((tmp[i - 1] >> 32)).value << 3) & bottom28Bits
        tmp2[i] += ctypes.c_uint32(tmp[i]).value & bottom28Bits
        tmp2[i] += carry

        carry = tmp2[i] >> 28
        tmp2[i] &= bottom28Bits

        i += 1

    tmp2[17] = ctypes.c_uint32(tmp[15] >> 32).value >> 25
    tmp2[17] += ctypes.c_uint32(tmp[16]).value >> 29
    tmp2[17] += ctypes.c_uint32(tmp[16] >> 32).value << 3
    tmp2[17] += carry
    # print(tmp2)
    # print('-'*10)

    i = 0
    while True:

        tmp2[i + 1] += tmp2[i] >> 29
        x = tmp2[i] & bottom29Bits
        xMask = non_zero_to_all_ones(x)
        tmp2[i] = 0

        tmp2[i + 3] += (x << 10) & bottom28Bits
        tmp2[i + 4] += x >> 18

        tmp2[i + 6] += (x << 21) & bottom29Bits
        tmp2[i + 7] += x >> 8

        tmp2[i + 7] += 0x10000000 & xMask
        tmp2[i + 8] += (x - 1) & xMask
        tmp2[i + 7] -= (x << 24) & bottom28Bits
        tmp2[i + 8] -= x >> 4

        tmp2[i + 8] += 0x20000000 & xMask
        tmp2[i + 8] -= x
        tmp2[i + 8] += (x << 28) & bottom29Bits
        tmp2[i + 9] += ((x >> 1) - 1) & xMask

        if i + 1 == p256Limbs:
            break
        tmp2[i + 2] += tmp2[i + 1] >> 28
        x = tmp2[i + 1] & bottom28Bits
        xMask = non_zero_to_all_ones(x)
        tmp2[i + 1] = 0

        tmp2[i + 4] += (x << 11) & bottom29Bits
        tmp2[i + 5] += x >> 18

        tmp2[i + 7] += (x << 21) & bottom28Bits
        tmp2[i + 8] += x >> 7
        tmp2[i + 8] += 0x20000000 & xMask
        tmp2[i + 9] += (x - 1) & xMask
        tmp2[i + 8] -= (x << 25) & bottom29Bits
        tmp2[i + 9] -= x >> 4

        tmp2[i + 9] += 0x10000000 & xMask
        tmp2[i + 9] -= x
        tmp2[i + 10] += (x - 1) & xMask
        i += 2
    carry = 0
    i = 0
    while i < 8:
        out[i] = tmp2[i + 9]
        out[i] += carry
        out[i] += (tmp2[i + 10] << 28) & bottom29Bits
        carry = out[i] >> 29
        out[i] &= bottom29Bits

        i += 1
        out[i] = tmp2[i + 9] >> 1
        out[i] += carry
        carry = out[i] >> 28
        out[i] &= bottom28Bits
        i += 1

    out[8] = tmp2[17]
    out[8] += carry
    carry = out[8] >> 29
    out[8] &= bottom29Bits

    p256_reduce_carry(out, carry)


def p256_point_add(xOut, yOut, zOut, x1, y1, z1, x2, y2, z2):
    z1z1, z1z1z1, z2z2, z2z2z2, s1, s2, u1, u2, h, i, j, r, rr, v, tmp = (
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
    )

    p256_square(z1z1, z1)
    p256_square(z2z2, z2)
    p256_mul(u1, x1, z2z2)

    p256_sum(tmp, z1, z2)
    p256_square(tmp, tmp)
    p256_diff(tmp, tmp, z1z1)
    p256_diff(tmp, tmp, z2z2)

    p256_mul(z2z2z2, z2, z2z2)
    p256_mul(s1, y1, z2z2z2)

    p256_mul(u2, x2, z1z1)
    p256_mul(z1z1z1, z1, z1z1)
    p256_mul(s2, y2, z1z1z1)
    p256_diff(h, u2, u1)
    p256_sum(i, h, h)
    p256_square(i, i)
    p256_mul(j, h, i)
    p256_diff(r, s2, s1)
    p256_sum(r, r, r)
    p256_mul(v, u1, i)

    p256_mul(zOut, tmp, h)
    p256_square(rr, r)
    p256_diff(xOut, rr, j)
    p256_diff(xOut, xOut, v)
    p256_diff(xOut, xOut, v)

    p256_diff(tmp, v, xOut)
    p256_mul(yOut, tmp, r)
    p256_mul(tmp, s1, j)
    p256_diff(yOut, yOut, tmp)
    p256_diff(yOut, yOut, tmp)


def p256_copy_conditional(out, in_, mask):
    for i in range(9):
        tmp = mask & (in_[i] ^ out[i])
        out[i] ^= tmp


def p256_select_jacobian_point(x_out, y_out, z_out, table, index):
    for i in range(len(x_out)):
        x_out[i] = 0
    for i in range(len(y_out)):
        y_out[i] = 0
    for i in range(len(z_out)):
        z_out[i] = 0

    # The implicit value at index 0 is all zero. We don't need to perform that
    # iteration of the loop because we already set out_* to zero.
    for i in range(1, 16):
        mask = ctypes.c_uint32(i ^ index).value
        mask |= ctypes.c_uint32(mask >> 2).value
        mask |= ctypes.c_uint32(mask >> 1).value
        mask &= 1
        mask -= 1
        for j in range(len(x_out)):
            x_out[j] |= ctypes.c_uint32(table[i][0][j] & mask).value
        for j in range(len(y_out)):
            y_out[j] |= ctypes.c_uint32(table[i][1][j] & mask).value
        for j in range(len(z_out)):
            z_out[j] |= ctypes.c_uint32(table[i][2][j] & mask).value


def p256_square(out, in_):
    tmp = [0] * 17

    tmp[0] = in_[0] * in_[0]
    tmp[1] = in_[0] * (in_[1] << 1)
    tmp[2] = in_[0] * (in_[2] << 1) + in_[1] * (in_[1] << 1)
    tmp[3] = in_[0] * (in_[3] << 1) + in_[1] * (in_[2] << 1)
    tmp[4] = in_[0] * (in_[4] << 1) + in_[1] * (in_[3] << 2) + in_[2] * in_[2]
    tmp[5] = in_[0] * (in_[5] << 1) + in_[1] * (in_[4] << 1) + in_[2] * (in_[3] << 1)
    tmp[6] = (
        in_[0] * (in_[6] << 1)
        + in_[1] * (in_[5] << 2)
        + in_[2] * (in_[4] << 1)
        + in_[3] * (in_[3] << 1)
    )
    tmp[7] = (
        in_[0] * (in_[7] << 1)
        + in_[1] * (in_[6] << 1)
        + in_[2] * (in_[5] << 1)
        + in_[3] * (in_[4] << 1)
    )
    tmp[8] = (
        in_[0] * (in_[8] << 1)
        + in_[1] * (in_[7] << 2)
        + in_[2] * (in_[6] << 1)
        + in_[3] * (in_[5] << 2)
        + in_[4] * in_[4]
    )
    tmp[9] = (
        in_[1] * (in_[8] << 1)
        + in_[2] * (in_[7] << 1)
        + in_[3] * (in_[6] << 1)
        + in_[4] * (in_[5] << 1)
    )
    tmp[10] = (
        in_[2] * (in_[8] << 1)
        + in_[3] * (in_[7] << 2)
        + in_[4] * (in_[6] << 1)
        + in_[5] * (in_[5] << 1)
    )
    tmp[11] = in_[3] * (in_[8] << 1) + in_[4] * (in_[7] << 1) + in_[5] * (in_[6] << 1)
    tmp[12] = in_[4] * (in_[8] << 1) + in_[5] * (in_[7] << 2) + in_[6] * in_[6]
    tmp[13] = in_[5] * (in_[8] << 1) + in_[6] * (in_[7] << 1)
    tmp[14] = in_[6] * (in_[8] << 1) + in_[7] * (in_[7] << 1)
    tmp[15] = in_[7] * (in_[8] << 1)
    tmp[16] = in_[8] * in_[8]
    # print(tmp)
    p256_reduce_degree(out, tmp)


def p256_mul(out, in_arr, in2_arr):
    tmp = [0] * 17

    tmp[0] = int(in_arr[0]) * int(in2_arr[0])
    tmp[1] = int(in_arr[0]) * (int(in2_arr[1]) << 0) + int(in_arr[1]) * (
        int(in2_arr[0]) << 0
    )
    tmp[2] = (
        int(in_arr[0]) * (int(in2_arr[2]) << 0)
        + int(in_arr[1]) * (int(in2_arr[1]) << 1)
        + int(in_arr[2]) * (int(in2_arr[0]) << 0)
    )
    tmp[3] = (
        int(in_arr[0]) * (int(in2_arr[3]) << 0)
        + int(in_arr[1]) * (int(in2_arr[2]) << 0)
        + int(in_arr[2]) * (int(in2_arr[1]) << 0)
        + int(in_arr[3]) * (int(in2_arr[0]) << 0)
    )
    tmp[4] = (
        int(in_arr[0]) * (int(in2_arr[4]) << 0)
        + int(in_arr[1]) * (int(in2_arr[3]) << 1)
        + int(in_arr[2]) * (int(in2_arr[2]) << 0)
        + int(in_arr[3]) * (int(in2_arr[1]) << 1)
        + int(in_arr[4]) * (int(in2_arr[0]) << 0)
    )
    tmp[5] = (
        int(in_arr[0]) * (int(in2_arr[5]) << 0)
        + int(in_arr[1]) * (int(in2_arr[4]) << 0)
        + int(in_arr[2]) * (int(in2_arr[3]) << 0)
        + int(in_arr[3]) * (int(in2_arr[2]) << 0)
        + int(in_arr[4]) * (int(in2_arr[1]) << 0)
        + int(in_arr[5]) * (int(in2_arr[0]) << 0)
    )
    tmp[6] = (
        int(in_arr[0]) * (int(in2_arr[6]) << 0)
        + int(in_arr[1]) * (int(in2_arr[5]) << 1)
        + int(in_arr[2]) * (int(in2_arr[4]) << 0)
        + int(in_arr[3]) * (int(in2_arr[3]) << 1)
        + int(in_arr[4]) * (int(in2_arr[2]) << 0)
        + int(in_arr[5]) * (int(in2_arr[1]) << 1)
        + int(in_arr[6]) * (int(in2_arr[0]) << 0)
    )
    tmp[7] = (
        int(in_arr[0]) * (int(in2_arr[7]) << 0)
        + int(in_arr[1]) * (int(in2_arr[6]) << 0)
        + int(in_arr[2]) * (int(in2_arr[5]) << 0)
        + int(in_arr[3]) * (int(in2_arr[4]) << 0)
        + int(in_arr[4]) * (int(in2_arr[3]) << 0)
        + int(in_arr[5]) * (int(in2_arr[2]) << 0)
        + int(in_arr[6]) * (int(in2_arr[1]) << 0)
        + int(in_arr[7]) * (int(in2_arr[0]) << 0)
    )
    tmp[8] = (
        int(in_arr[0]) * (int(in2_arr[8]) << 0)
        + int(in_arr[1]) * (int(in2_arr[7]) << 1)
        + int(in_arr[2]) * (int(in2_arr[6]) << 0)
        + int(in_arr[3]) * (int(in2_arr[5]) << 1)
        + int(in_arr[4]) * (int(in2_arr[4]) << 0)
        + int(in_arr[5]) * (int(in2_arr[3]) << 1)
        + int(in_arr[6]) * (int(in2_arr[2]) << 0)
        + int(in_arr[7]) * (int(in2_arr[1]) << 1)
        + int(in_arr[8]) * (int(in2_arr[0]) << 0)
    )
    tmp[9] = (
        int(in_arr[1]) * (int(in2_arr[8]) << 0)
        + int(in_arr[2]) * (int(in2_arr[7]) << 0)
        + int(in_arr[3]) * (int(in2_arr[6]) << 0)
        + int(in_arr[4]) * (int(in2_arr[5]) << 0)
        + int(in_arr[5]) * (int(in2_arr[4]) << 0)
        + int(in_arr[6]) * (int(in2_arr[3]) << 0)
        + int(in_arr[7]) * (int(in2_arr[2]) << 0)
        + int(in_arr[8]) * (int(in2_arr[1]) << 0)
    )
    tmp[10] = (
        int(in_arr[2]) * (int(in2_arr[8]) << 0)
        + int(in_arr[3]) * (int(in2_arr[7]) << 1)
        + int(in_arr[4]) * (int(in2_arr[6]) << 0)
        + int(in_arr[5]) * (int(in2_arr[5]) << 1)
        + int(in_arr[6]) * (int(in2_arr[4]) << 0)
        + int(in_arr[7]) * (int(in2_arr[3]) << 1)
        + int(in_arr[8]) * (int(in2_arr[2]) << 0)
    )
    tmp[11] = (
        int(in_arr[3]) * (int(in2_arr[8]) << 0)
        + int(in_arr[4]) * (int(in2_arr[7]) << 0)
        + int(in_arr[5]) * (int(in2_arr[6]) << 0)
        + int(in_arr[6]) * (int(in2_arr[5]) << 0)
        + int(in_arr[7]) * (int(in2_arr[4]) << 0)
        + int(in_arr[8]) * (int(in2_arr[3]) << 0)
    )
    tmp[12] = (
        int(in_arr[4]) * (int(in2_arr[8]) << 0)
        + int(in_arr[5]) * (int(in2_arr[7]) << 1)
        + int(in_arr[6]) * (int(in2_arr[6]) << 0)
        + int(in_arr[7]) * (int(in2_arr[5]) << 1)
        + int(in_arr[8]) * (int(in2_arr[4]) << 0)
    )
    tmp[13] = (
        int(in_arr[5]) * (int(in2_arr[8]) << 0)
        + int(in_arr[6]) * (int(in2_arr[7]) << 0)
        + int(in_arr[7]) * (int(in2_arr[6]) << 0)
        + int(in_arr[8]) * (int(in2_arr[5]) << 0)
    )
    tmp[14] = (
        int(in_arr[6]) * (int(in2_arr[8]) << 0)
        + int(in_arr[7]) * (int(in2_arr[7]) << 1)
        + int(in_arr[8]) * (int(in2_arr[6]) << 0)
    )
    tmp[15] = int(in_arr[7]) * (int(in2_arr[8]) << 0) + int(in_arr[8]) * (
        int(in2_arr[7]) << 0
    )
    tmp[16] = int(in_arr[8]) * (int(in2_arr[8]) << 0)

    p256_reduce_degree(out, tmp)


def p256_sum(out, in1, in2):
    carry = 0
    i = 0
    while True:
        out[i] = in1[i] + in2[i] + carry
        carry = out[i] >> 29
        out[i] &= bottom29Bits

        i += 1
        if i == p256Limbs:
            break

        out[i] = in1[i] + in2[i] + carry
        carry = out[i] >> 28
        out[i] &= bottom28Bits
        i += 1
    p256_reduce_carry(out, carry)


def p256_diff(out, in1, in2):
    carry = 0
    i = 0
    while True:
        out[i] = in1[i] - in2[i]
        out[i] += p256Zero31[i]
        out[i] += carry
        carry = out[i] >> 29
        out[i] &= bottom29Bits

        i += 1
        if i == p256Limbs:
            break

        out[i] = in1[i] - in2[i]
        out[i] += p256Zero31[i]
        out[i] += carry
        carry = out[i] >> 28
        out[i] &= bottom28Bits
        i += 1
    p256_reduce_carry(out, carry)


def p256_assign(out, in_):
    out[:] = in_[:]


def p256_invert(out, in_):
    ftmp, ftmp2 = [0] * p256Limbs, [0] * p256Limbs

    # each e_I will hold |in|^{2^I - 1}
    e2, e4, e8, e16, e32, e64 = (
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
        [0] * p256Limbs,
    )

    p256_square(ftmp, in_)  # 2^1
    p256_mul(ftmp, in_, ftmp)  # 2^2 - 2^0
    p256_assign(e2, ftmp)
    p256_square(ftmp, ftmp)  # 2^3 - 2^1
    p256_square(ftmp, ftmp)  # 2^4 - 2^2
    p256_mul(ftmp, ftmp, e2)  # 2^4 - 2^0
    p256_assign(e4, ftmp)
    p256_square(ftmp, ftmp)  # 2^5 - 2^1
    p256_square(ftmp, ftmp)  # 2^6 - 2^2
    p256_square(ftmp, ftmp)  # 2^7 - 2^3
    p256_square(ftmp, ftmp)  # 2^8 - 2^4
    p256_mul(ftmp, ftmp, e4)  # 2^8 - 2^0
    p256_assign(e8, ftmp)
    for i in range(8):
        p256_square(ftmp, ftmp)  # 2^16 - 2^8
    p256_mul(ftmp, ftmp, e8)  # 2^16 - 2^0
    p256_assign(e16, ftmp)
    for _ in range(16):
        p256_square(ftmp, ftmp)  # 2^32 - 2^16
    p256_mul(ftmp, ftmp, e16)  # 2^32 - 2^0
    p256_assign(e32, ftmp)
    for _ in range(32):
        p256_square(ftmp, ftmp)  # 2^64 - 2^32
    p256_assign(e64, ftmp)
    p256_mul(ftmp, ftmp, in_)  # 2^64 - 2^32 + 2^0
    for _ in range(192):
        p256_square(ftmp, ftmp)  # 2^256 - 2^224 + 2^192

    p256_mul(ftmp2, e64, e32)  # 2^64 - 2^0
    for _ in range(16):
        p256_square(ftmp2, ftmp2)  # 2^80 - 2^16
    p256_mul(ftmp2, ftmp2, e16)  # 2^80 - 2^0
    for _ in range(8):
        p256_square(ftmp2, ftmp2)  # 2^88 - 2^8
    p256_mul(ftmp2, ftmp2, e8)  # 2^88 - 2^0
    for _ in range(4):
        p256_square(ftmp2, ftmp2)  # 2^92 - 2^4
    p256_mul(ftmp2, ftmp2, e4)  # 2^92 - 2^0
    p256_square(ftmp2, ftmp2)  # 2^93 - 2^1
    p256_square(ftmp2, ftmp2)  # 2^94 - 2^2
    p256_mul(ftmp2, ftmp2, e2)  # 2^94 - 2^0
    p256_square(ftmp2, ftmp2)  # 2^95 - 2^1
    p256_square(ftmp2, ftmp2)  # 2^96 - 2^2
    p256_mul(ftmp2, ftmp2, in_)  # 2^96 - 3

    p256_mul(out, ftmp2, ftmp)  # 2^256 - 2^224 + 2^192 + 2^96 - 3


def p256_scalar_3(out):
    carry = 0

    i = 0
    while True:
        out[i] *= 3
        out[i] += carry
        carry = out[i] >> 29
        out[i] &= bottom29Bits

        if i + 1 == p256Limbs:
            break

        i += 1
        out[i] *= 3
        out[i] += carry
        carry = out[i] >> 28
        out[i] &= bottom28Bits
        i += 1

    p256_reduce_carry(out, carry)


def p256_scalar_4(out):
    carry = 0

    i = 0
    while True:
        nextCarry = out[i] >> 27
        out[i] <<= 2
        out[i] &= bottom29Bits
        out[i] += carry
        carry = nextCarry + (out[i] >> 29)
        out[i] &= bottom29Bits

        if i + 1 == p256Limbs:
            break

        i += 1
        nextCarry = out[i] >> 26
        out[i] <<= 2
        out[i] &= bottom28Bits
        out[i] += carry
        carry = nextCarry + (out[i] >> 28)
        out[i] &= bottom28Bits
        i += 1

    p256_reduce_carry(out, carry)


def p256_scalar_8(out):
    carry = 0

    i = 0
    while True:
        nextCarry = out[i] >> 26
        out[i] <<= 3
        out[i] &= bottom29Bits
        out[i] += carry
        carry = nextCarry + (out[i] >> 29)
        out[i] &= bottom29Bits

        if i + 1 == p256Limbs:
            break

        i += 1
        nextCarry = out[i] >> 25
        out[i] <<= 3
        out[i] &= bottom28Bits
        out[i] += carry
        carry = nextCarry + (out[i] >> 28)
        out[i] &= bottom28Bits
        i += 1

    p256_reduce_carry(out, carry)


def int_to_bits(_in):
    _in_bin = bin(_in)
    bits_list = []
    while _in_bin:
        _input = _in_bin[-64:]
        if _input[0] == "b":
            _input = "0" + _input
        bits_list.append(int(_input, 2))
        _in_bin = _in_bin[:-64]
        if _in_bin == "0b":
            break
    return bits_list


class p256Curve(CurveParams):
    def __init__(self):
        super().__init__()
        self.p256RInverse = 0

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
        n = int.from_bytes(_in, "big")
        if n >= self.N:
            n = n % self.N
            l = (n.bit_length() + 7) // 8
            scalar_bytes = int.to_bytes(n, byteorder="big", length=l)
        else:
            scalar_bytes = _in
        for i, v in enumerate(scalar_bytes):
            out[len(scalar_bytes) - (1 + i)] = v

    def scalar_mult(self, bigX, bigY, scalar):
        scalarReversed = [0] * 32
        self.get_scalar(scalarReversed, scalar)

        px, py, x1, y1, z1 = (
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
        )
        self.p256_from_big(px, bigX)
        self.p256_from_big(py, bigY)

        self.p256_scalar_mult(x1, y1, z1, px, py, scalarReversed)
        return self.p256_to_affine(x1, y1, z1)

    def p256_scalar_mult(self, x_out, y_out, z_out, x, y, scalar):
        px, py, pz, tx, ty, tz = (
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
        )
        precomp = [[([0] * p256Limbs) for _ in range(3)] for _ in range(16)]
        n_is_infinity_mask, index, p_is_noninfinite_mask, mask = 0, 0, 0, 0

        precomp[1][0] = x
        precomp[1][1] = y
        precomp[1][2] = p256One

        i = 2
        while i < 16:
            self.p256_point_double(
                precomp[i][0],
                precomp[i][1],
                precomp[i][2],
                precomp[int(i / 2)][0],
                precomp[int(i / 2)][1],
                precomp[int(i / 2)][2],
            )
            self.p256_point_add_mixed(
                precomp[i + 1][0],
                precomp[i + 1][1],
                precomp[i + 1][2],
                precomp[i][0],
                precomp[i][1],
                precomp[i][2],
                x,
                y,
            )
            i += 2
        for i in range(len(x_out)):
            x_out[i] = 0

        for i in range(len(y_out)):
            y_out[i] = 0

        for i in range(len(z_out)):
            z_out[i] = 0

        n_is_infinity_mask = (1 << 32) - 1

        for i in range(64):
            if i != 0:
                self.p256_point_double(x_out, y_out, z_out, x_out, y_out, z_out)
                self.p256_point_double(x_out, y_out, z_out, x_out, y_out, z_out)
                self.p256_point_double(x_out, y_out, z_out, x_out, y_out, z_out)
                self.p256_point_double(x_out, y_out, z_out, x_out, y_out, z_out)

            index = ctypes.c_uint32(scalar[31 - i // 2]).value
            if (i & 1) == 1:
                index &= 15
            else:
                index >>= 4

            p256_select_jacobian_point(px, py, pz, precomp, index)
            p256_point_add(tx, ty, tz, x_out, y_out, z_out, px, py, pz)
            p256_copy_conditional(x_out, px, n_is_infinity_mask)
            p256_copy_conditional(y_out, py, n_is_infinity_mask)
            p256_copy_conditional(z_out, pz, n_is_infinity_mask)

            p_is_noninfinite_mask = non_zero_to_all_ones(index)
            mask = p_is_noninfinite_mask & ~n_is_infinity_mask
            p256_copy_conditional(x_out, tx, mask)
            p256_copy_conditional(y_out, ty, mask)
            p256_copy_conditional(z_out, tz, mask)
            n_is_infinity_mask &= ~p_is_noninfinite_mask

    def p256_point_double(self, xOut, yOut, zOut, x, y, z):
        delta, gamma, alpha, beta, tmp, tmp2 = (
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
        )

        p256_square(delta, z)
        p256_square(gamma, y)
        p256_mul(beta, x, gamma)

        p256_sum(tmp, x, delta)
        p256_diff(tmp2, x, delta)
        p256_mul(alpha, tmp, tmp2)
        p256_scalar_3(alpha)
        # print(tmp)
        # print(alpha)
        # print(beta)
        # print(delta)
        # print(gamma)
        # print(x)
        # breakpoint()

        p256_sum(tmp, y, z)
        p256_square(tmp, tmp)
        p256_diff(tmp, tmp, gamma)
        p256_diff(zOut, tmp, delta)

        p256_scalar_4(beta)
        p256_square(xOut, alpha)
        p256_diff(xOut, xOut, beta)
        p256_diff(xOut, xOut, beta)

        p256_diff(tmp, beta, xOut)
        p256_mul(tmp, alpha, tmp)
        p256_square(tmp2, gamma)
        p256_scalar_8(tmp2)
        p256_diff(yOut, tmp, tmp2)

    def p256_point_add_mixed(self, x_out, y_out, z_out, x1, y1, z1, x2, y2):
        z1z1 = [0] * p256Limbs
        z1z1z1 = [0] * p256Limbs
        s2 = [0] * p256Limbs
        u2 = [0] * p256Limbs
        h = [0] * p256Limbs
        i = [0] * p256Limbs
        j = [0] * p256Limbs
        r = [0] * p256Limbs
        rr = [0] * p256Limbs
        v = [0] * p256Limbs
        tmp = [0] * p256Limbs

        p256_square(z1z1, z1)
        p256_sum(tmp, z1, z1)

        p256_mul(u2, x2, z1z1)
        p256_mul(z1z1z1, z1, z1z1)
        p256_mul(s2, y2, z1z1z1)
        p256_diff(h, u2, x1)
        p256_sum(i, h, h)
        p256_square(i, i)
        p256_mul(j, h, i)
        p256_diff(r, s2, y1)
        p256_sum(r, r, r)
        p256_mul(v, x1, i)

        p256_mul(z_out, tmp, h)
        p256_square(rr, r)
        p256_diff(x_out, rr, j)
        p256_diff(x_out, x_out, v)
        p256_diff(x_out, x_out, v)

        p256_diff(tmp, v, x_out)
        p256_mul(y_out, tmp, r)
        p256_mul(tmp, y1, j)
        p256_diff(y_out, y_out, tmp)
        p256_diff(y_out, y_out, tmp)

    def p256_point_to_affine(self, xOut, yOut, x, y, z):
        zInv, zInvSq = [0] * p256Limbs, [0] * p256Limbs

        p256_invert(zInv, z)
        p256_square(zInvSq, zInv)
        p256_mul(xOut, x, zInvSq)
        p256_mul(zInv, zInv, zInvSq)
        p256_mul(yOut, y, zInv)

    def p256_to_affine(self, x, y, z):
        xx, yy = [0] * p256Limbs, [0] * p256Limbs
        self.p256_point_to_affine(xx, yy, x, y, z)

        return self.p256_to_big(xx), self.p256_to_big(yy)

    def p256_to_big(self, in_):
        result = ctypes.c_int64(in_[p256Limbs - 1]).value
        for i in range(7, -1, -1):
            if (i & 1) == 0:
                result <<= 29
            else:
                result <<= 28
            tmp = ctypes.c_int64(in_[i]).value
            result += tmp

        result *= self.p256RInverse
        result %= self.P
        return result

    def p256_from_big(self, out, in_value):
        tmp = in_value << 257
        tmp = tmp % self.P
        i = 0
        while i < p256Limbs:
            bits = int_to_bits(tmp)
            if bits:
                out[i] = ctypes.c_uint32(bits[0]).value & bottom29Bits
            else:
                out[i] = 0
            tmp >>= 29

            i += 1
            if i == p256Limbs:
                break
            bits = int_to_bits(tmp)
            if len(bits) > 0:
                out[i] = ctypes.c_uint32(bits[0]).value & bottom28Bits
            else:
                out[i] = 0
            tmp >>= 28
            i += 1


P256 = p256Curve()
P256.P = int(
    "115792089210356248762697446949407573530086143415290314195533631308867097853951",
    10,
)
P256.N = int(
    "115792089210356248762697446949407573529996955224135760342422259061068512044369",
    10,
)
P256.B = int(
    "5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b",
    16,
)
P256.Gx = int(
    "6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296",
    16,
)
P256.Gy = int(
    "4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5",
    16,
)
P256.BitSize = 256

P256.p256RInverse = int(
    "7fffffff00000001fffffffe8000000100000000ffffffff0000000180000000", 16
)

k = int(
    "115792089210356248762697446949407573529996955224135760342422259061068512044368", 10
)
l = (k.bit_length() + 7) // 8

print(P256.is_on_curve(P256.Gx, P256.Gy))
gen_x, gen_y = P256.scalar_mult(
    int("6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296", 16),
    int("B01CBD1C01E58065711814B583F061E9D431CCA994CEA1313449BF97C840AE0A", 16),
    int.to_bytes(k, byteorder="big", length=l),
)
print(gen_x, gen_y)
P256Generic = CurveParams()
P256Generic.P = int(
    "115792089210356248762697446949407573530086143415290314195533631308867097853951",
    10,
)
P256Generic.N = int(
    "115792089210356248762697446949407573529996955224135760342422259061068512044369",
    10,
)
P256Generic.B = int(
    "5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b",
    16,
)
P256Generic.Gx = int(
    "6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296",
    16,
)
P256Generic.Gy = int(
    "4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5",
    16,
)
P256Generic.BitSize = 256
gen_x, gen_y = P256Generic.scalar_mult(
    int("6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296", 16),
    int("B01CBD1C01E58065711814B583F061E9D431CCA994CEA1313449BF97C840AE0A", 16),
    int.to_bytes(k, byteorder="big", length=l),
)
print(gen_x, gen_y)
