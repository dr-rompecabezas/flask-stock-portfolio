import os

from flask import Flask, render_template, request, session, redirect, url_for
from pydantic import BaseModel, validator

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')


class Stock(BaseModel):
    """Parse stock information from form submission"""

    symbol: str
    shares: int
    price: float

    @validator('symbol')
    def symbol_must_be_valid(cls, v):
        if not v.isalpha() or len(v) > 5:
            raise ValueError('Symbol must be less than 5 characters')
        return v.upper()

    @validator('shares')
    def shares_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Shares must be positive')
        return v

    @validator('price')
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Price must be positive')
        return v


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/stocks/')
def list_stocks():
    return render_template('stocks.html', title='List Stocks')


@app.route('/stocks/add', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(f'{key}: {value}')
        try:
            stock = Stock(
                symbol=request.form['symbol'],
                shares=int(request.form['shares']),
                price=float(request.form['price'])
            )
            print(stock)
            session['symbol'] = stock.symbol
            session['shares'] = stock.shares
            session['price'] = stock.price
            return redirect(url_for('list_stocks'))
        except ValueError as e:
            print(e)
    return render_template('add_stock.html', title='Add Stock')
