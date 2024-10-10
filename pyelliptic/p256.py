from pyelliptic.elliptic import CurveParams
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

p256_precomputed = [
    0x11522878,
    0xE730D41,
    0xDB60179,
    0x4AFE2FF,
    0x12883ADD,
    0xCADDD88,
    0x119E7EDC,
    0xD4A6EAB,
    0x3120BEE,
    0x1D2AAC15,
    0xF25357C,
    0x19E45CDD,
    0x5C721D0,
    0x1992C5A5,
    0xA237487,
    0x154BA21,
    0x14B10BB,
    0xAE3FE3,
    0xD41A576,
    0x922FC51,
    0x234994F,
    0x60B60D3,
    0x164586AE,
    0xCE95F18,
    0x1FE49073,
    0x3FA36CC,
    0x5EBCD2C,
    0xB402F2F,
    0x15C70BF,
    0x1561925C,
    0x5A26704,
    0xDA91E90,
    0xCDC1C7F,
    0x1EA12446,
    0xE1ADE1E,
    0xEC91F22,
    0x26F7778,
    0x566847E,
    0xA0BEC9E,
    0x234F453,
    0x1A31F21A,
    0xD85E75C,
    0x56C7109,
    0xA267A00,
    0xB57C050,
    0x98FB57,
    0xAA837CC,
    0x60C0792,
    0xCFA5E19,
    0x61BAB9E,
    0x589E39B,
    0xA324C5,
    0x7D6DEE7,
    0x2976E4B,
    0x1FC4124A,
    0xA8C244B,
    0x1CE86762,
    0xCD61C7E,
    0x1831C8E0,
    0x75774E1,
    0x1D96A5A9,
    0x843A649,
    0xC3AB0FA,
    0x6E2E7D5,
    0x7673A2A,
    0x178B65E8,
    0x4003E9B,
    0x1A1F11C2,
    0x7816EA,
    0xF643E11,
    0x58C43DF,
    0xF423FC2,
    0x19633FFA,
    0x891F2B2,
    0x123C231C,
    0x46ADD8C,
    0x54700DD,
    0x59E2B17,
    0x172DB40F,
    0x83E277D,
    0xB0DD609,
    0xFD1DA12,
    0x35C6E52,
    0x19EDE20C,
    0xD19E0C0,
    0x97D0F40,
    0xB015B19,
    0x449E3F5,
    0xE10C9E,
    0x33AB581,
    0x56A67AB,
    0x577734D,
    0x1DDDC062,
    0xC57B10D,
    0x149B39D,
    0x26A9E7B,
    0xC35DF9F,
    0x48764CD,
    0x76DBCCA,
    0xCA4B366,
    0xE9303AB,
    0x1A7480E7,
    0x57E9E81,
    0x1E13EB50,
    0xF466CF3,
    0x6F16B20,
    0x4BA3173,
    0xC168C33,
    0x15CB5439,
    0x6A38E11,
    0x73658BD,
    0xB29564F,
    0x3F6DC5B,
    0x53B97E,
    0x1322C4C0,
    0x65DD7FF,
    0x3A1E4F6,
    0x14E614AA,
    0x9246317,
    0x1BC83ACA,
    0xAD97EED,
    0xD38CE4A,
    0xF82B006,
    0x341F077,
    0xA6ADD89,
    0x4894ACD,
    0x9F162D5,
    0xF8410EF,
    0x1B266A56,
    0xD7F223,
    0x3E0CB92,
    0xE39B672,
    0x6A2901A,
    0x69A8556,
    0x7E7C0,
    0x9B7D8D3,
    0x309A80,
    0x1AD05F7F,
    0xC2FB5DD,
    0xCBFD41D,
    0x9CEB638,
    0x1051825C,
    0xDA0CF5B,
    0x812E881,
    0x6F35669,
    0x6A56F2C,
    0x1DF8D184,
    0x345820,
    0x1477D477,
    0x1645DB1,
    0xBE80C51,
    0xC22BE3E,
    0xE35E65A,
    0x1AEB7AA0,
    0xC375315,
    0xF67BC99,
    0x7FDD7B9,
    0x191FC1BE,
    0x61235D,
    0x2C184E9,
    0x1C5A839,
    0x47A1E26,
    0xB7CB456,
    0x93E225D,
    0x14F3C6ED,
    0xCCC1AC9,
    0x17FE37F3,
    0x4988989,
    0x1A90C502,
    0x2F32042,
    0xA17769B,
    0xAFD8C7C,
    0x8191C6E,
    0x1DCDB237,
    0x16200C0,
    0x107B32A1,
    0x66C08DB,
    0x10D06A02,
    0x3FC93,
    0x5620023,
    0x16722B27,
    0x68B5C59,
    0x270FCFC,
    0xFAD0ECC,
    0xE5DE1C2,
    0xEAB466B,
    0x2FC513C,
    0x407F75C,
    0xBAAB133,
    0x9705FE9,
    0xB88B8E7,
    0x734C993,
    0x1E1FF8F,
    0x19156970,
    0xABD0F00,
    0x10469EA7,
    0x3293AC0,
    0xCDC98AA,
    0x1D843FD,
    0xE14BFE8,
    0x15BE825F,
    0x8B5212,
    0xEB3FB67,
    0x81CBD29,
    0xBC62F16,
    0x2B6FCC7,
    0xF5A4E29,
    0x13560B66,
    0xC0B6AC2,
    0x51AE690,
    0xD41E271,
    0xF3E9BD4,
    0x1D70AAB,
    0x1029F72,
    0x73E1C35,
    0xEE70FBC,
    0xAD81BAF,
    0x9ECC49A,
    0x86C741E,
    0xFE6BE30,
    0x176752E7,
    0x23D416,
    0x1F83DE85,
    0x27DE188,
    0x66F70B8,
    0x181CD51F,
    0x96B6E4C,
    0x188F2335,
    0xA5DF759,
    0x17A77EB6,
    0xFEB0E73,
    0x154AE914,
    0x2F3EC51,
    0x3826B59,
    0xB91F17D,
    0x1C72949,
    0x1362BF0A,
    0xE23FDDF,
    0xA5614B0,
    0xF7D8F,
    0x79061,
    0x823D9D2,
    0x8213F39,
    0x1128AE0B,
    0xD095D05,
    0xB85C0C2,
    0x1ECB2EF,
    0x24DDC84,
    0xE35E901,
    0x18411A4A,
    0xF5DDC3D,
    0x3786689,
    0x52260E8,
    0x5AE3564,
    0x542B10D,
    0x8D93A45,
    0x19952AA4,
    0x996CC41,
    0x1051A729,
    0x4BE3499,
    0x52B23AA,
    0x109F307E,
    0x6F5B6BB,
    0x1F84E1E7,
    0x77A0CFA,
    0x10C4DF3F,
    0x25A02EA,
    0xB048035,
    0xE31DE66,
    0xC6ECAA3,
    0x28EA335,
    0x2886024,
    0x1372F020,
    0xF55D35,
    0x15E4684C,
    0xF2A9E17,
    0x1A4A7529,
    0xCB7BEB1,
    0xB2A78A1,
    0x1AB21F1F,
    0x6361CCF,
    0x6C9179D,
    0xB135627,
    0x1267B974,
    0x4408BAD,
    0x1CBFF658,
    0xE3D6511,
    0xC7D76F,
    0x1CC7A69,
    0xE7EE31B,
    0x54FAB4F,
    0x2B914F,
    0x1AD27A30,
    0xCD3579E,
    0xC50124C,
    0x50DAA90,
    0xB13F72,
    0xB06AA75,
    0x70F5CC6,
    0x1649E5AA,
    0x84A5312,
    0x329043C,
    0x41C4011,
    0x13D32411,
    0xB04A838,
    0xD760D2D,
    0x1713B532,
    0xBAA0C03,
    0x84022AB,
    0x6BCF5C1,
    0x2F45379,
    0x18AE070,
    0x18C9E11E,
    0x20BCA9A,
    0x66F496B,
    0x3EEF294,
    0x67500D2,
    0xD7F613C,
    0x2DBBEB,
    0xB741038,
    0xE04133F,
    0x1582968D,
    0xBE985F7,
    0x1ACBC1A,
    0x1A6A939F,
    0x33E50F6,
    0xD665ED4,
    0xB4B7BD6,
    0x1E5A3799,
    0x6B33847,
    0x17FA56FF,
    0x65EF930,
    0x21DC4A,
    0x2B37659,
    0x450FE17,
    0xB357B65,
    0xDF5EFAC,
    0x15397BEF,
    0x9D35A7F,
    0x112AC15F,
    0x624E62E,
    0xA90AE2F,
    0x107EECD2,
    0x1F69BBE,
    0x77D6BCE,
    0x5741394,
    0x13C684FC,
    0x950C910,
    0x725522B,
    0xDC78583,
    0x40EEABB,
    0x1FDE328A,
    0xBD61D96,
    0xD28C387,
    0x9E77D89,
    0x12550C40,
    0x759CB7D,
    0x367EF34,
    0xAE2A960,
    0x91B8BDC,
    0x93462A9,
    0xF469EF,
    0xB2E9AEF,
    0xD2CA771,
    0x54E1F42,
    0x7AAA49,
    0x6316ABB,
    0x2413C8E,
    0x5425BF9,
    0x1BED3E3A,
    0xF272274,
    0x1F5E7326,
    0x6416517,
    0xEA27072,
    0x9CEDEA7,
    0x6E7633,
    0x7C91952,
    0xD806DCE,
    0x8E2A7E1,
    0xE421E1A,
    0x418C9E1,
    0x1DBC890,
    0x1B395C36,
    0xA1DC175,
    0x1DC4EF73,
    0x8956F34,
    0xE4B5CF2,
    0x1B0D3A18,
    0x3194A36,
    0x6C2641F,
    0xE44124C,
    0xA2F4EAA,
    0xA8C25BA,
    0xF927ED7,
    0x627B614,
    0x7371CCA,
    0xBA16694,
    0x417BC03,
    0x7C0A7E3,
    0x9C35C19,
    0x1168A205,
    0x8B6B00D,
    0x10E3EDC9,
    0x9C19BF2,
    0x5882229,
    0x1B2B4162,
    0xA5CEF1A,
    0x1543622B,
    0x9BD433E,
    0x364E04D,
    0x7480792,
    0x5C9B5B3,
    0xE85FF25,
    0x408EF57,
    0x1814CFA4,
    0x121B41B,
    0xD248A0F,
    0x3B05222,
    0x39BB16A,
    0xC75966D,
    0xA038113,
    0xA4A1769,
    0x11FBC6C,
    0x917E50E,
    0xEEC3DA8,
    0x169D6EAC,
    0x10C1699,
    0xA416153,
    0xF724912,
    0x15CD60B7,
    0x4ACBAD9,
    0x5EFC5FA,
    0xF150ED7,
    0x122B51,
    0x1104B40A,
    0xCB7F442,
    0xFBB28FF,
    0x6AC53CA,
    0x196142CC,
    0x7BF0FA9,
    0x957651,
    0x4E0F215,
    0xED439F8,
    0x3F46BD5,
    0x5ACE82F,
    0x110916B6,
    0x6DB078,
    0xFFD7D57,
    0xF2ECAAC,
    0xCA86DEC,
    0x15D6B2DA,
    0x965ECC9,
    0x1C92B4C2,
    0x1F3811,
    0x1CB080F5,
    0x2D8B804,
    0x19D1C12D,
    0xF20BD46,
    0x1951FA7,
    0xA3656C3,
    0x523A425,
    0xFCD0692,
    0xD44DDC8,
    0x131F0F5B,
    0xAF80E4A,
    0xCD9FC74,
    0x99BB618,
    0x2DB944C,
    0xA673090,
    0x1C210E1,
    0x178C8D23,
    0x1474383,
    0x10B8743D,
    0x985A55B,
    0x2E74779,
    0x576138,
    0x9587927,
    0x133130FA,
    0xBE05516,
    0x9F4D619,
    0xBB62570,
    0x99EC591,
    0xD9468FE,
    0x1D07782D,
    0xFC72E0B,
    0x701B298,
    0x1863863B,
    0x85954B8,
    0x121A0C36,
    0x9E7FEDF,
    0xF64B429,
    0x9B9D71E,
    0x14E2F5D8,
    0xF858D3A,
    0x942EEA8,
    0xDA5B765,
    0x6EDAFFF,
    0xA9D18CC,
    0xC65E4BA,
    0x1C747E86,
    0xE4EA915,
    0x1981D7A1,
    0x8395659,
    0x52ED4E2,
    0x87D43B7,
    0x37AB11B,
    0x19D292CE,
    0xF8D4692,
    0x18C3053F,
    0x8863E13,
    0x4C146C0,
    0x6BDF55A,
    0x4E4457D,
    0x16152289,
    0xAC78EC2,
    0x1A59C5A2,
    0x2028B97,
    0x71C2D01,
    0x295851F,
    0x404747B,
    0x878558D,
    0x7D29AA4,
    0x13D8341F,
    0x8DAEFD7,
    0x139C972D,
    0x6B7EA75,
    0xD4A9DDE,
    0xFF163D8,
    0x81D55D7,
    0xA5BEF68,
    0xB7B30D8,
    0xBE73D6F,
    0xAA88141,
    0xD976C81,
    0x7E7A9CC,
    0x18BEB771,
    0xD773CBD,
    0x13F51951,
    0x9D0C177,
    0x1C49A78,
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

    def p256_get_scalar(self, out: bytearray, in_bytes: bytes) -> None:
        n = int.from_bytes(in_bytes, byteorder="big")
        scalar_bytes = bytearray()

        if n >= self.N:
            n %= self.N
            scalar_bytes = n.to_bytes((n.bit_length() + 7) // 8, byteorder="big")
        else:
            scalar_bytes = in_bytes

        for i, v in enumerate(scalar_bytes):
            out[len(scalar_bytes) - (1 + i)] = v

    def p256_get_bit(self, scalar, bit):
        return (scalar[bit >> 3] >> (bit & 7)) & 1

    def p256_select_affine_point(self, x_out, y_out, table, index):
        for i in range(len(x_out)):
            x_out[i] = 0
        for i in range(len(y_out)):
            y_out[i] = 0

        for i in range(1, 16):
            mask = i ^ index
            mask |= mask >> 2
            mask |= mask >> 1
            mask &= 1
            mask -= 1
            for j in range(len(x_out)):
                x_out[j] |= table[0] & mask
                table = table[1:]
            for j in range(len(y_out)):
                y_out[j] |= table[0] & mask
                table = table[1:]

    def p256_scalar_base_mult(self, x_out, y_out, z_out, scalar):
        n_is_infinity_mask = (1 << 32) - 1
        pIsNoninfiniteMask, mask, tableOffset = 0, 0, 0
        px, py, tx, ty, tz = (
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
            [0] * p256Limbs,
        )
        for i in range(len(x_out)):
            x_out[i] = 0
        for i in range(len(y_out)):
            y_out[i] = 0
        for i in range(len(z_out)):
            z_out[i] = 0

        for i in range(32):
            if i != 0:
                self.p256_point_double(x_out, y_out, z_out, x_out, y_out, z_out)
            table_offset = 0
            for j in range(0, 33, 32):
                bit0 = self.p256_get_bit(scalar, 31 - i + j)
                bit1 = self.p256_get_bit(scalar, 95 - i + j)
                bit2 = self.p256_get_bit(scalar, 159 - i + j)
                bit3 = self.p256_get_bit(scalar, 223 - i + j)
                index = bit0 | (bit1 << 1) | (bit2 << 2) | (bit3 << 3)

                self.p256_select_affine_point(
                    px, py, p256_precomputed[table_offset:], index
                )
                table_offset += 30 * p256Limbs

                self.p256_point_add_mixed(tx, ty, tz, x_out, y_out, z_out, px, py)
                p256_copy_conditional(x_out, px, n_is_infinity_mask)
                p256_copy_conditional(y_out, py, n_is_infinity_mask)
                p256_copy_conditional(z_out, p256One, n_is_infinity_mask)

                p_is_noninfinite_mask = non_zero_to_all_ones(index)
                mask = p_is_noninfinite_mask & ~n_is_infinity_mask
                p256_copy_conditional(x_out, tx, mask)
                p256_copy_conditional(y_out, ty, mask)
                p256_copy_conditional(z_out, tz, mask)
                n_is_infinity_mask &= ~p_is_noninfinite_mask

    def scalar_base_mult(self, scalar):
        scalar_reversed = bytearray(32)
        self.p256_get_scalar(scalar_reversed, scalar)

        x1, y1, z1 = [0] * p256Limbs, [0] * p256Limbs, [0] * p256Limbs
        self.p256_scalar_base_mult(x1, y1, z1, scalar_reversed)
        return self.p256_to_affine(x1, y1, z1)

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
