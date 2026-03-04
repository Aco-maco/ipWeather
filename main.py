from flask import Flask, render_template, request
from tinydb import TinyDB, Query

@app.route('/') 
def  index():   
# Pridobi IP naslov obiskovalca 
	if request.headers.get('X-Forwarded-For'): 
		ip = request.headers.get('X-Forwarded-For').split(',')[0] 
	else:
		ip = request.remote_addr  
	print(ip)  # Za debugging return  f"Vaš IP je: {ip}"`

ipapi="https://freeipapi.com/api/json/{ip}"
weather="https://api.openweathermap.org"


# Inicializacija baze 
db = TinyDB('visitors.json')   
# Vstavljanje podatkov 
db.insert({'ime':  'Janez',  'starost':  25})   
# Poizvedovanje 
User = Query() 
rezultati = db.search(User.ime ==  'Janez')  
# Lahko bi tudi rezultati = db.search(Query().ime ==  'Janez')  
# Pridobivanje vseh zapisov 
vsi_zapisi = db.all()   
# Primer uporabe v Flask aplikaciji 
@app.route('/obiskovalci') 
def  obiskovalci():   
	vsi_obiskovalci = db.all() 
	return render_template('obiskovalci.html', obiskovalci=vsi_obiskovalci)