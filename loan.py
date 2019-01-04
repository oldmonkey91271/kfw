#!/usr/bin/python3

import sys
import getopt
import math
import numpy
import matplotlib.pyplot as plt
import pandas as pd

# Define the MyLoans class
class MyLoans:

    # The constructor
    # Accepts a dataframe of loan descriptors
    def __init__(self,
                 ldf: object) -> object:

        (self.NumLoan, self.NumParm) = ldf.shape

        self.loans = []

        # Iterate on each loan & instantiate loan objects
        for n in range(self.NumLoan):
            # Append to list of loan objects
            self.loans.append(Loan(ldf.iloc[n]))



    # The user input handler function
    def uhandler(self,
                 uaction: object) -> object:
        switcher = {
            1: uhelp,
            2: ulist
        }

        if (uaction == 0):
            print("Goodbye!")
            sys.exit(0)
        else:
            # Get the handler function based on user input
            func = switcher.get(uaction)
            # Execute user handler function
            try:
                func(self.loans)
            except:
                print("Error! Exiting | " + str(uaction))
                sys.exit(1)

# Define generalized Loan class
class Loan:

    # The constructor
    # Accepts a dataframe loan descriptor
    def __init__(self,
                 ldf: object) -> object:

        self.ldf = ldf                                      # << loan dataframe

        self.Name = ldf['Name']                             # << Loan name

        r = ldf['AIR']                                      # << Annual interest rate
        self.r = r

        n_p = ldf['APF']                                    # << Annual payment frequency
        self.n_p = n_p

        n_r = ldf['ACF']                                    # << Annual compounding frequency
        self.n_r = n_r

        self.i = r                                          # << Effective interest rate

        # If compounding interest
        if (ldf['Type'] == 'Compound'):
            self.i = ((1 + (r / n_r)) ** (n_r / n_p)) - 1   # << Effective interest rate based on payment frequency

        print("\nLoan created >> " + self.Name)
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

            # Compute loan remainder
            p_remainder = self.GetLoanRemainder(P0, Pn, nn)
            P_remainder.append(p_remainder)

            # Compute principal paid
            p_paid = p_nn - p_remainder
            # Compute interest paid
            i_paid = Pn - p_paid

            # Accumulate principal and interest paid
            P_paid.append(P_paid[-1] + p_paid)
            I_paid.append(I_paid[-1] + i_paid)

            #print("Payment %d, Loan remainder is %2.2f, P,I is (%2.2f, %2.2f)" % (nn, p_remainder, p_paid, i_paid))

            # Update running principal balance
            p_nn = p_remainder

        return (P_remainder, P_paid, I_paid)

    # The loan comparison method
    # Input     starting principal balance (P0), regular payment (P1), regular payment (P2)
    # Output    cost savings between loan's 1 & 2
    def CompareLoan(self, P01, P1, P02, P2):

        # Compute the loand burn down for each loan
        P_remainder1, P_paid1, I_paid1 = self.GetLoanBurnDown(P01, P1)
        P_remainder2, P_paid2, I_paid2 = self.GetLoanBurnDown(P02, P2)

        # Compute the interest paid in each loan
        I1 = I_paid1[-1]
        I2 = I_paid2[-1]

        # Compute the number of payments in each loan
        Np1 = self.GetNumPymt(P01, P1)
        Np2 = self.GetNumPymt(P02, P2)

        print("\nLoan 1 of $%2.2f, interest rate %2.1f.\n" %(P01, (self.r*100)))
        print("Scenario 1: Payment $%2.2f, total payments %d, interest paid $%2.2f.\n" % (P1, Np1, I1))
        print("\nLoan 2 of $%2.2f, interest rate %2.1f.\n" %(P02, (self.r*100)))
        print("Scenario 2: Payment $%2.2f, total payments %d, interest paid $%2.2f.\n" % (P2, Np2, I2))

        print("Years saved is %2.1f (%2.2f), interest saved is $%2.2f\n" % (((Np2 - Np1) / self.n_p), (Np2 / self.n_p), (I2 - I1)))

        return

    # The loan burn down plotting method
    # Input     starting principal balance (P0), regular payment (Pn)
    # Output    lists containing principal remaining, principal paid, & interest paid
    def PlotLoanBurnDown(self, P0, Pn):

        # Obtain the loan burn down
        P_remainder, P_paid, I_paid = self.GetLoanBurnDown(P0, Pn)

        Np = len(P_remainder)

        plt.ion()
        plt.subplot(1,1,1)
        # Plot the loan burn down
        plt.plot(range(1, Np +1), P_remainder, '-b', label="Loan Balance")
        plt.plot(range(1, Np +1), P_paid, '-k', label="Principal Paid (P)")
        plt.plot(range(1, Np +1), I_paid, 'r', label="Cost of Borrowing (I)")
        plt.bar(range(1, Np +1), numpy.sum([P_paid, I_paid], axis=0), label='P+I')

        plt.legend(loc='best')
        plt.ylabel("Dollars ($)")
        plt.xlabel("Payment #")
        plt.title('Loan $%2.2f, Payment \$%2.2f, Rate %2.2f pct' % (P0, Pn, (self.r*100)))
        plt.grid(True, which='both')
        plt.show()

        return

    #  The loan name set/get methods
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

    # The loan interest rate compound frequency sTheet/get methods
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

# The user help handler
def uhelp(loans: object) -> object:
    print("You selected help!")
    return 0

# The user list handler
def ulist(loans: object) -> object:
    print("You selected list!")
    print(str(loans))
    return 0

if (0):
    # Some unit test code to sanitize loan.py
    P0      = 253089     # Loan starting balance
    P1      = 0         # Loan ending balance
    r       = 0.0229    # Annual interest rate
    n_r     = 2         # Interest compounds semi annually
    n_p     = 52        # Monthly payments
    NumPymt = 673

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
    SumPrincipal = P_paid[-1]
    SumInterest  = I_paid[-1]
    print("\nTotal principal paid is $%2.2f" % SumPrincipal)
    print("Total interest paid is $%2.2f" % SumInterest)

    # Compare how the loan changes by adjusting payment
    loan_1.CompareLoan(P0, Pymt, P0, Pymt+100)

    # Plot loan burn down data
    loan_1.PlotLoanBurnDown(P0, Pymt)

    wait = input("\nPress a key to continue.")

    print('\nWe\'re done!')
else:

    def main(argv):
        # Process the commandline arguments
        #print('Number of arguments: ', len(argv))
        #print('The arguments are: ', str(argv))

        # Initialize the input loan files
        loanfile1 = ''
        loanfile2 = ''

        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print ('usage: kloan -i <loanfile1> -o <loanfile2>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print ('usage: kloan -i <loanfile1> -o <loanfile2>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                loanfile1 = arg
            elif opt in ("-o", "--ofile"):
                loanfile2 = arg

        # Read the input loan parameter file
        print('\nReading input loan file... ', loanfile1)
        l1df = pd.read_csv(loanfile1)

        # Instantiate MyLoans object
        my_loans = MyLoans(l1df)

        # Handle use input
        while True:
            # Provide input options to the user
            print("\n-----------------------------------------")
            print("<< 0 >> quit")
            print("<< 1 >> help")
            print("<< 2 >> list loans")
            print("<< 3 >> loan analysis 1")
            print("<< 4 >> loan analysis 2")
            print("-----------------------------------------")
            # Poll the user for input
            try:
                uaction = int(input("\tPlease choose your action. "))

                # Run the user input handler
                my_loans.uhandler(uaction)

            except ValueError:
                print("Oops!  That wasn't valid.  Please retry...")


    if __name__ == '__main__':
        main(sys.argv[1:])
