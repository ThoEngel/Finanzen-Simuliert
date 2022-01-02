class mDate:

    """ date class only with month and year

    Attributes:
        self.Month: Month of date
        self.Year: Year of dat

    """

    def __init__(self, Month, Year):
        self.Month = Month
        self.Year = Year

    def DateInc(self):
        if self.Month >= 12:
            self.Month = 1
            self.Year = self.Year + 1
        else:
            self.Month = self.Month + 1

    def DateDelta(self, FirstDate, SecDate):
        DeltaYear = SecDate.Year - FirstDate.Year
        DeltaMonth = SecDate.Month - FirstDate.Month

    def DatePrint(self):
        return (str(self.Month), str(self.Year))

    def DateGet(self):
        return self.Month, self.Year

    def DateGetNum(self):
        return self.Year * 12 + self.Month

    def __eq__(self, other):
        if (self.Year*12+self.Month) == (other.Year*12+other.Month):
            return True
        else:
            return False

    def __lt__(self, other):
        if (self.Year*12+self.Month) < (other.Year*12+other.Month):
            return True
        else:
            return False

    def __le__(self, other):
        if (self.Year*12+self.Month) <= (other.Year*12+other.Month):
            return True
        else:
            return False

    def __gt__(self, other):
        if (self.Year * 12 + self.Month) > (other.Year * 12 + other.Month):
            return True
        else:
            return False

    def __ge__(self, other):
        if (self.Year * 12 + self.Month) >= (other.Year * 12 + other.Month):
            return True
        else:
            return False