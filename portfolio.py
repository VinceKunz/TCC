# Import Flask

import flask
app = flask.Flask("portfolio")

# Import modules from the Python Standard Library

import datetime

import csv

# CLASSES

# Class 1: Class definition

class Crypto:
    
    def __init__(self, name, symbol, price, one_month, amount):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.one_month = one_month
        self.amount = amount

    def perform(self):
        if self.one_month > 0:
            performance = self.name + " has seen an increase of " + str(self.one_month) + "% in its price over the last month."
            return performance
        elif self.one_month < 0:
            performance = self.name + " has seen a decrease of " + str(self.one_month).strip("-") + "% in its price over the last month."
            return performance
        else:
            performance = self.name + "has stayed even since one month."
            return performance    

# Class 1: Objects

bitcoin = Crypto("Bitcoin", "BTC", 18740, 38.13, 0.25)
ethereum = Crypto("Ethereum", "ETH", 576.52, 50.83, 12)
monero = Crypto("Monero", "XMR", 122.18, -1.41, 5.31)

# Class 2: Class definition

class NasdaqStock:
    def __init__(self, name, ticker, price, amount):
        self.name = name
        self.ticker = ticker
        self.price = price
        self.amount = amount
    
    def count(self):
        value = "${:,.2f}".format(self.amount * self.price)
        equity = "You are holding " + str(self.amount) + " stocks of " + self.name + " (" + self.ticker + "), for a total of " + str(value) + "."
        return equity

# Class 2: Objects

microsoft = NasdaqStock("Microsoft", "MSFT", 214.07, 15)
apple = NasdaqStock("Apple", "AAPL", 119.05, 43)
starbucks = NasdaqStock("Starbucks", "SBUX", 98.02, 80)

# FUNCTIONS

def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content

def get_assets():
    assets = open("data/assets.csv")
    content = assets.read()
    assets.close()
    assetsarr = content.split("\n")
    return assetsarr

def load_assets():
    with open("data/assets.csv", newline="", encoding="utf-8-sig") as file:
        data = list(csv.reader(file))
        table_content = "<table>"
        for row in data:
            row.append("</tr>")
            row.insert(0, "<tr>")
            for cell in row:
                if cell != "<tr>" and cell != "</tr>":
                    cell = "<td>" + cell + "</td>"
                table_content += cell
        table_content += "</table>"
        return table_content

def nyse_time():
    now = datetime.datetime.utcnow()
    today1430 = now.replace(hour=14, minute=30, second=0, microsecond=0)
    today21 = now.replace(hour=21, minute=0, second=0, microsecond=0)
    nyse = "The NYSE stock exchange is "
    if now < today1430 or now > today21:
        closed = nyse + "closed."
        return closed
    else:
        open = nyse + "open."
        return open

# ROUTES

# Homepage

@app.route("/")
def home():
    html_page = get_html("index")
    
    assets = load_assets()
    temp1 = ""
    for asset in assets:
        temp1 += asset

    time = nyse_time()
    temp2 = ""
    for clock in time:
        temp2 += clock

    cryptos = "<p>" + bitcoin.perform() + "</p><p>" + ethereum.perform() + "</p>"
    temp3 = ""
    for crypto in cryptos:
        temp3 += crypto

    stocks = "<p>" + microsoft.count() + "</p><p>" + starbucks.count() + "</p>"
    temp4 = ""
    for stock in stocks:
        temp4 += stock

    return html_page.replace("$$ASSETS$$", temp1).replace("$$CLOCK$$", temp2).replace("$$MOVES$$", temp3).replace("$$VALUE$$", temp4)

# Add an asset

@app.route("/add")
def add():
    return get_html("add")

@app.route("/result")
def result():
    html_page = get_html("result")
    elem1 = flask.request.args.get("elem1")
    elem2 = flask.request.args.get("elem2")
    elem3 = flask.request.args.get("elem3")
    assets = open("data/assets.csv", "a")
    if elem1 == "" or elem2 == "" or elem3 == "":
        return html_page.replace("$$ITEM$$", "Please complete all the fields.")
    else:
        assets.write("\n" + elem1)
        assets.write("<td>" + elem2 + "</td>")
        assets.write("<td>$" + elem3 + "</td>")
        amount = str(round(float(elem2) * float(elem3), 2))
        assets.write("<td>$" + amount + "</td>")
        assets.close()
        return html_page.replace("$$ITEM$$", "The asset was added successfully.")  

# Remove an asset

@app.route("/delete")
def delete():
    return get_html("delete")

@app.route("/removed")
def removed():
    html_page = get_html("result")
    element = flask.request.args.get("element")
    f = open("data/assets.csv", "r")
    lines = f.readlines()
    f = open("data/assets.csv", "w")
    if len(element) > 0:
        if any(element in str for str in lines):
            for line in lines:
                if line.find(element) == -1:
                    f.write(line)               
            f.close()
            return html_page.replace("$$ITEM$$", "The asset was removed successfully.")
        else:
            for line in lines:
                f.write(line)
            f.close()
            return html_page.replace("$$ITEM$$", "The asset was not found.")
    else:
        for line in lines:
            f.write(line)
        f.close()
        return html_page.replace("$$ITEM$$", "Please type an asset name in the textbox.")

# Search an asset

@app.route("/search")
def search():
    return get_html("search")

@app.route("/search_results")
def search_results():
    html_page = get_html("result")
    query = flask.request.args.get("q")
    assets = get_assets()
    if len(query) > 0:
        result = ""
        for asset in assets:
            if asset.lower().find(query.lower()) != -1:
                result += "<p>" + query + " has been found in your portfolio.</p>"
        if result == "":
            result = "<p>This asset has not been found.</p>"
        return html_page.replace("$$ITEM$$", result)
    else:
        return html_page.replace("$$ITEM$$", "Please enter a value in the textbox.")