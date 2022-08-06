from flask import Flask, request


app = Flask(__name__)

def get_data(nama='Marwan'):
    data = {'nama' : nama,
            'usia' : 23,
            'profesi' : 'Instruktur hacktive'}
    return data

# halaman home
@app.route("/")
def homepage():
    return "<h1> Halo dari Flask!</h1>"

# halaman info
@app.route("/info")
def infopage():
    data = get_data()
    return data

# halaman info
@app.route("/gantinama", methods=['POST'])
def gantinama():
    content = request.json
    data = get_data(nama=content['nama'])
    return data

# run app di local
# Jika deploy heroku komen baris dibawah
app.run(debug=True) 