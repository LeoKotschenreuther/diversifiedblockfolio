from pytest import approx


def holdings_equal(A, B):
    if len(A) != len(B):
        return False
    A.sort(key=lambda holding: holding['symbol'])
    B.sort(key=lambda holding: holding['symbol'])
    for index, holdingA in enumerate(A):
        holdingB = B[index]
        if holdingA.keys() != holdingB.keys():
            return False
        for key in holdingA.keys():
            if ((type(holdingA[key]) == float or
                    type(holdingB[key] == float)) and
                    holdingA[key] != approx(holdingB[key]) or
                    type(holdingA[key]) != float and
                    holdingA[key] != holdingB[key]):
                return False
    return True


def buys_equal(A, B):
    if len(A) != len(B):
        return False
    A.sort()
    B.sort()
    for index, buyA in enumerate(A):
        buyB = B[index]
        if buyA[0] != buyB[0]:
            return False
        if buyA[1] != buyB[1]:
            return False
        if buyA[2] != approx(buyB[2]):
            return False
    return True
