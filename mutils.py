#!usr/bin/python

# Define the Loan class
class Loan:

    # The constructor
    def __init__(self,
                 Name: object,
                 r: object,
                 n_r: object,
                 n_p: object) -> object:

        self.Name = Name                                # Name of the loan
        self.r = r                                      # r is the annual interest rate
        self.n_r = n_r                                  # n_r is frequency of interest compounding annually
        self.n_p = n_p                                  # n_p is the frequency of payment annually
        self.i = ((1 + (r / n_r)) ** (n_r / n_p)) - 1   # Effective interest rate based payment frequency

    # The payment calculator method
    def GetPymt(self, Po, n):
        # The compounded interest payment calculator
        # p = Po * i * (1 + i)^n / ((1 + i)^n - 1)
        x = Po * self.i * (1 + self.i) ** n
        y = ((1 + self.i) ** n) - 1
        return (x / y)

    # The amortization calculator method
    def GetAmort(self):
        pass

    # The number of payment calculator method
    def GetNp(self):
        pass



loan_1 = Loan('My Mortgage', 0.0229, 2, 52)
loan_2 = Loan('My Test', 0.02, 1, 1)

print("Hello World!")
print(loan_1)
print(loan_1.GetPymt(255675, 681))
print(loan_2.GetPymt(50000, 24))

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


x = apr(50000, 0.02, 24)
print(x)
