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
