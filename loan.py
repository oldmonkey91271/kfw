#!usr/bin/python

import math

# Define generalized Loan class
class Loan:

    # The constructor
    # The loan class contains the following attributes:
    #   Name of the loan (Name)
    #   Annual interest rate of the loan (r)
    #   Number of times interest is compounded annually (n_r)
    #   Number of times payments are made annually (n_p)
    #   The effective interest rate of loan when compounded at payment frequency
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

        print("\nLoan created >> " + Name)
        print(" >> Interest rate is %1.2f percent, compounded %d times annually" % (r * 100, n_r))
        if (n_p == 12):
            PymtFrequency = "monthly"
        elif (n_p == 26):
            PymtFrequency = "bi-weekly"
        elif (n_p == 52):
            PymtFrequency = "weekly"
        else:
            raise ValueError("Unsupported annual loan payment frequency %d" % n_p)

        print(" >> Payments will be made " + PymtFrequency)
        print(" >> Effective interest rate is %1.4f percent\n" % (self.i * 100))

    # The payment calculator method
    # Input     principal loan amount (P0) & number of payments for loan repayment (n)
    # Output    regular payment amount
    def GetPymt(self, P0, n):
        # The compounded interest payment calculator
        # p = P0 * i * (1 + i)^n / ((1 + i)^n - 1)
        x = P0 * self.i * (1 + self.i) ** n
        y = ((1 + self.i) ** n) - 1
        return (x / y)

    # The number of payment calculator method
    # Input     principal loan amount (P0) & payment amount (Pn)
    # Output    number of payments until loan paid in full
    def GetNumPymt(self, P0, Pn):
        x = -1 * math.log10(1 - (P0 * self.i / Pn))
        y = math.log10(1 + self.i)
        return math.ceil(x / y)

    # The maximum loan calculator method
    # Input     maximum payment (Pn) & number of payments (Np)
    # Output    maximum loan amount that can be borrowed
    def GetMaxLoan(self, Pn, Np):
        return (Pn / self.i * (1 - (1 + self.i) ** -Np))

    # The remaining balance calculator method
    # Input     starting loan amount (P0), regular payment amount (Pn), number of payments (Np)
    # Output    remaining loan principal amount (Pr)
    def GetLoanRemainder(self, P0, Pn, Np):
        x = P0 * (1 +self.i) ** Np
        y = (Pn / self.i) * (((1 + self.i) ** Np) - 1)
        return (x - y)

    # The number of payment (partial) calculator method
    # Input     starting principal balance (P0), ending principal balance (P1), regular payment (Pn)
    # Output    number of payments to reach ending principal balance (P1)
    def GetNumPymtPartial(self, P0, P1, Pn):
        x1 = math.log10(1 - (P1 * self.i / Pn))
        x0 = math.log10(1 - (P0 * self.i / Pn))
        y = math.log10(1 + self.i)
        return math.ceil((x1 - x0) / y)

    # The loan burn down calculator method
    # Input     starting principal balance (P0), regular payment (Pn)
    # Output    lists containing principal remaining, principal paid, & interest paid
    def GetLoanBurnDown(self, P0, Pn):

        # First compute total payments to pay off loan
        Np = self.GetNumPymt(P0, Pn)

        # Initialize burn down lists
        P_remainder = [P0]
        P_paid      = [0]
        I_paid      = [0]

        # Initialize running loan principal
        p_nn        = P0
        for nn in range(1, Np+1):

            # Compute the loan remainder
            p_remainder = self.GetLoanRemainder(P0, Pn, nn)
            P_remainder.append(p_remainder)

            # Compute principal paid
            p_paid = p_nn - p_remainder
            P_paid.append(p_paid)

            # Compute interest paid
            i_paid = Pn - p_paid
            I_paid.append(i_paid)

            #print("Payment %d, Loan remainder is %2.2f, P,I is (%2.2f, %2.2f)" % (nn, p_remainder, p_paid, i_paid))

            # Update running principal balance
            p_nn = p_remainder


        return (P_remainder, P_paid, I_paid)


    # The loan name set/get methods
    def SetName(self, Name):
        self.Name = Name

    def GetName(self):
        return self.Name



    # The loan interest rate set/get methods
    def SetRate(self, r):
        self.r = r
        self.SetEffRate()

    def GetRate(self):
        return self.r

    # The loan interest rate compound frequency set/get methods
    def SetNr(self, n_r):
        self.n_r = n_r
        self.SetEffRate()

    def GetNr(self):
        return self.n_r

    # The loan payment frequency set/get methods
    def SetNp(self, n_p):
        self.n_p = n_p
        self.SetEffRate()

    def GetNp(self):
        return self.n_p


    # The loan effective rate set/get methods
    def SetEffRate(self):
        self.i = ((1 + (self.r / self.n_r)) ** (self.n_r / self.n_p)) - 1   # Effective interest rate

    def GetEffRate(self):
        return self.i

if (1):
    # Some unit test code to sanitize loan.py
    P0      = 255675    # Loan starting balance
    P1      = 100000    # Loan ending balance
    r       = 0.0229    # Annual interest rate
    n_r     = 2         # Interest compounds semi annually
    n_p     = 52        # Weekly payments
    NumPymt = 681

    # Instantiate the loan
    loan_1 = Loan('My Mortgage', r, n_r, n_p)

    # Obtain weekly payment amount of the loan given principal remaining and 681 weekly payments
    Pymt = loan_1.GetPymt(P0, NumPymt)
    print("The loan payment amount is $%1.2f" % Pymt)
    # Obtain number of payments given starting principal and computed weekly payment amount
    Np = loan_1.GetNumPymt(P0, Pymt)
    print("The number of payments is %1.0f, %1.2f years" % (Np, Np / loan_1.GetNp()))
    # Obtain the maximum loan amount given the interest rate, loan payment, and number of payments
    MaxLoan = loan_1.GetMaxLoan(Pymt, NumPymt)
    print("The maximum loan amount is $%1.2f" % MaxLoan)
    # Obtain the remaining loan after a number of payments
    RemLoan = loan_1.GetLoanRemainder(P0, Pymt, NumPymt)
    print("The loan remainder after %1.0f payments is $%1.2f" % (NumPymt, RemLoan))
    # Obtain number of payments to achieve an ending loan balance (P1)
    n1 = loan_1.GetNumPymtPartial(P0, P1, Pymt)
    print("The number of payments to reach $%1.2f balance is %1.0f (%1.1f years)" % (P1, n1, n1 / loan_1.GetNp()))

    # Obtain the loan burn down data
    P_remainder, P_paid, I_paid = loan_1.GetLoanBurnDown(P0, Pymt)
    # Determine total principal & interest paid (cost of borrowing)
    SumPrincipal = sum(P_paid)
    SumInterest = sum(I_paid)
    print("\nTotal principal paid is $%2.2f" % SumPrincipal)
    print("Total interest paid is $%2.2f" % SumInterest)

    # Plot loan burn down data