import streamlit as st

def add_vertical_space(num_lines: int = 1):
    """Add vertical space to your Streamlit app."""
    for _ in range(num_lines):
        st.write("")

class MortgageProduct:
  """A parent class for capturing mortgage product information fixed rates."""
  NORMALISATION = 1e5

  def __init__(self, loan, term, rate, discount_rate):
    """Initialise a MortgageProduct.
      Args:
        loan: mortgage loan amount in the currency (GBP, USD).
        term: term of mortgage in years.
        rate: fixed rate for the mortgage in %.
        discount_rate: rate used to discount future cashflows in %.
    """
    self.set_loan(loan)
    self.set_term(term)
    self.set_rate(rate)
    self.set_discount_rate(discount_rate)
  
  def set_loan(self, value):
    self._loan = value
  def get_loan(self):
    return self._loan
  
  def set_term(self, value):
    self._term = value
  def get_term(self):
    return self._term
  
  def set_rate(self, value):
    self._rate = value
  def get_rate(self):
    return self._rate
  
  def set_discount_rate(self, value):
    self._discount_rate = value
  def get_discount_rate(self):
    return self._discount_rate
    
  def monthly_payments(self):
    for payment in range(60,800):
      normPV = self.NORMALISATION
      for month in range(self._term*12):
        normPV *= (1+ self._rate/1200)
        normPV -= payment
      if normPV < 0: break
    return payment * self._loan/self.NORMALISATION
  
  def total_cashflows(self):
    return self.monthly_payments()* self._term * 12
  
  def total_discounted_cashflows(self):
    discount_factor = 1/(1+self._discount_rate/1200)
    return self.monthly_payments()*(1-pow(discount_factor,self._term*12))/(1-discount_factor)

st.title("Simple Mortgage Pricer")

loan = st.slider('Mortgage loan amount:', 1e5, 2e6, 5e5,1e5, format="£%d")
term = st.slider('Mortgage term:', 10, 35, 20,1, format="%d years")
rate = st.slider('Mortgage rate:', 0.2, 9.9, 4.5,0.1, format="%f%%")
discount_rate = st.slider('Discounting rate:', 0.2, 9.9, 4.5,0.1, format="%f%%")

n1 = MortgageProduct(loan, term, rate, discount_rate)

st.subheader(f"With a loan of £{round(n1.get_loan()):,},")
st.subheader(f"paying over {n1.get_term()} years at {n1.get_rate():.1f}% fixed interest,")
st.subheader(f"the monthly payment is £{int(n1.monthly_payments()):,} (total amount paid: £{int(n1.total_cashflows()):,})")
st.subheader(f"Assuming a constant discount rate of {n1.get_discount_rate():.1f}%,")
st.subheader(f"Total discounted payment is £{int(n1.total_discounted_cashflows()):,}")

st.subheader(f"Value of mortgage product is £{int(n1.total_discounted_cashflows())-round(n1.get_loan()):,}")

