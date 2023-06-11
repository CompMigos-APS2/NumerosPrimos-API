from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from peewee import *
import math

pg_db = PostgresqlDatabase('numerosprimos', user='postgres', password='admin', host='localhost', port=5432)
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/": {"origins": "*"}})

def crivo(n):
    lim = int(2 * n * math.log(n))
    r = [True] * lim
    r[0] = r[1] = False
    primes = []
    for i in range(2, lim):
        if r[i]:
            primes.append(i)

            if len(primes) == n:
                return primes

            for j in range(i * i, lim, i):
                r[j] = False
    return primes


class Products(Model):
    factor1 = DoubleField()
    factor2 = DoubleField()
    product = DoubleField(unique=True, primary_key=True)

    class Meta:
        database = pg_db
        db_table = 'produtos'


pg_db.connect()
pg_db.create_tables([Products])

escolha = 1

while (escolha != 0):

    escolha = int(input("Você deseja gerar novos produtos no banco? 0 - NÃO / 1 - SIM - "))

    if escolha == 1:
        n = int(input("Quantos primos você quer gerar? - "))

        primos = crivo(n)
        print(primos)

        for i in range(0, len(primos)):
            for j in range(i + 1, len(primos)):
                try:
                    Products.create(factor1=primos[i], factor2=primos[j], product=primos[i] * primos[j])
                except:
                    print("Chave duplicada")


@app.route("/", methods=['GET'])
def getFromKey():
    args = request.args
    key = args.get('key')
    prods = Products.select().where(Products.product == key)
    if len(prods) > 0:
        prod = prods.first()
        return jsonify({"factor1": prod.factor1, "factor2": prod.factor2})
    else:
        return Response("Key not found", status=400)

app.run()