#!usr/bin/env python

# The compounded interest payment calculator
#
# p = Po * r * (1 + r)^n / ((1 + r)^n - 1)
#
# where :   p = payment amount
#           Po is the loan principal
#           r is the interest rate
#           n is the number of payments

def apr(Po, r, n):
    x = Po * r * (1 + r) ** n;
    y = ((1 + r) ** n) - 1;
    return (x / y);



