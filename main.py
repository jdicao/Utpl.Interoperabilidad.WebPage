from flask import Flask, render_template, request, redirect, url_for

import requests

app = Flask(__name__)

#Declarar el API KEY generado de wso2 api manager desde la aplicacion
API_KEY = 'eyJ4NXQiOiJPREUzWTJaaE1UQmpNRE00WlRCbU1qQXlZemxpWVRJMllqUmhZVFpsT0dJeVptVXhOV0UzWVE9PSIsImtpZCI6ImdhdGV3YXlfY2VydGlmaWNhdGVfYWxpYXMiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhZG1pbkBjYXJib24uc3VwZXIiLCJhcHBsaWNhdGlvbiI6eyJvd25lciI6ImFkbWluIiwidGllclF1b3RhVHlwZSI6bnVsbCwidGllciI6IlVubGltaXRlZCIsIm5hbWUiOiJhcHBfZmVsaXBlIiwiaWQiOjIsInV1aWQiOiI3ZjZkOWIwNi0yYTljLTQ5NDAtOGFmNi04ZTNhMzc2NWNjMmQifSwiaXNzIjoiaHR0cHM6XC9cL3V0cGx3c28yLnRrOjQ0M1wvYXBpbVwvb2F1dGgyXC90b2tlbiIsInRpZXJJbmZvIjp7IlVubGltaXRlZCI6eyJ0aWVyUXVvdGFUeXBlIjoicmVxdWVzdENvdW50IiwiZ3JhcGhRTE1heENvbXBsZXhpdHkiOjAsImdyYXBoUUxNYXhEZXB0aCI6MCwic3RvcE9uUXVvdGFSZWFjaCI6dHJ1ZSwic3Bpa2VBcnJlc3RMaW1pdCI6MCwic3Bpa2VBcnJlc3RVbml0IjpudWxsfX0sImtleXR5cGUiOiJQUk9EVUNUSU9OIiwicGVybWl0dGVkUmVmZXJlciI6IiIsInN1YnNjcmliZWRBUElzIjpbeyJzdWJzY3JpYmVyVGVuYW50RG9tYWluIjoiY2FyYm9uLnN1cGVyIiwibmFtZSI6IlV0cGxQZXJzb25hcyIsImNvbnRleHQiOiJcL2FwaXBlcnNvbmFcLzEuMCIsInB1Ymxpc2hlciI6ImFkbWluIiwidmVyc2lvbiI6IjEuMCIsInN1YnNjcmlwdGlvblRpZXIiOiJVbmxpbWl0ZWQifSx7InN1YnNjcmliZXJUZW5hbnREb21haW4iOiJjYXJib24uc3VwZXIiLCJuYW1lIjoiVXRwbFBlcnNvbmFzIiwiY29udGV4dCI6IlwvYXBpcGVyc29uYVwvMi4wIiwicHVibGlzaGVyIjoiYWRtaW4iLCJ2ZXJzaW9uIjoiMi4wIiwic3Vic2NyaXB0aW9uVGllciI6IlVubGltaXRlZCJ9LHsic3Vic2NyaWJlclRlbmFudERvbWFpbiI6ImNhcmJvbi5zdXBlciIsIm5hbWUiOiJVdHBsUGVyc29uYXMiLCJjb250ZXh0IjoiXC9hcGlwZXJzb25hXC8zLjAiLCJwdWJsaXNoZXIiOiJhZG1pbiIsInZlcnNpb24iOiIzLjAiLCJzdWJzY3JpcHRpb25UaWVyIjoiVW5saW1pdGVkIn1dLCJ0b2tlbl90eXBlIjoiYXBpS2V5IiwicGVybWl0dGVkSVAiOiIiLCJpYXQiOjE2ODk5NTU1MzQsImp0aSI6ImIzYTJkMjc1LTZhMTEtNDc4My1iMTRhLTMwNGU2ZGJhN2U5MCJ9.cNJlok5z2hJjoHlFcCVqR8UWJkEg_hlLjvmvIEGWiCMUWMAvQ7iWaB4uP5dLQ5vfDzFXp4hirbJmkI5eA8LtU_ebfVLCsDZ_9UnpK6-mS2Wlrvw0HyA9YU7bv-C2PvqWuG9IFB4_EqNRzmf2XuTD8QODEvjHkeei9lzwfaglHUURSrjkzF6Yq1VWgeJawbaVw-iljwBRY1JXvlDwpQAWEMKU_-WJZgfJwW5Aw4OQmozI0rQhAhuI6oaaek-1VaeNwdHSlzaBOU4eZQuueAzzbAMdWAHKPByuci1Ca4n6dfDIhQcGyALB_yIIUy_puDYrZZA4x70tFUpjuo_InvTaEQ=='
API_TOKEN = 'eyJ4NXQiOiJNV0l5TkRJNVlqRTJaV1kxT0RNd01XSTNOR1ptTVRZeU5UTTJOVFZoWlRnMU5UTTNaVE5oTldKbVpERTFPVEE0TldFMVlUaGxNak5sTldFellqSXlZUSIsImtpZCI6Ik1XSXlOREk1WWpFMlpXWTFPRE13TVdJM05HWm1NVFl5TlRNMk5UVmhaVGcxTlRNM1pUTmhOV0ptWkRFMU9UQTROV0UxWVRobE1qTmxOV0V6WWpJeVlRX1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJlMjkzYjRiNS0xNmFhLTQ5NTQtYTdiYi00NDU1NTIyMWU1MDciLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IjVRWTBJVEdfNFVWbXhjd2NBZ1FsZjV6YVU3Y2EiLCJuYmYiOjE2OTA3NzQ1MTMsImF6cCI6IjVRWTBJVEdfNFVWbXhjd2NBZ1FsZjV6YVU3Y2EiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczpcL1wvbG9jYWxob3N0Ojk0NDNcL29hdXRoMlwvdG9rZW4iLCJleHAiOjM3NjkwNzc0NTEzLCJpYXQiOjE2OTA3NzQ1MTMsImp0aSI6ImI5NTI5MGFhLTgzOTktNDYyNC1hODFiLWM1OGI4NWQ0OTgwMyIsImNsaWVudF9pZCI6IjVRWTBJVEdfNFVWbXhjd2NBZ1FsZjV6YVU3Y2EifQ.lcneS2Hb8GpiAO_je8RBz2cPBEqZqU9fdp0GY40MGifaocnReaqCXTAM5EC9lG0FRwIPyo20dWV4KJri38vJ-q3IatZ8aL0OwxFwYNvxjP_OFTBnV2t0_hrVIRlaoCzA_7OFM8xU3wAsf1NHqFs-iif-1IqkPMtg2zuFDwuc9TgGp1jULcQdRl8rSaXOxaUM9cPnUq5jVsFULZpmhjJRR537Twdv-rU4XpHEOW7VdomKv6LMRlm0dCX3CZja9l94iY2hLmR4EQJI2wyiKezXjeFYsQgxLgNYD5RjqtL5eyjDqfDzGw685fAXLinqfDIJfrVTxK-k10ZKz82y2g-MmQ'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/personas')
def personas():
    headers = {'apikey': API_KEY}
    response = requests.get('https://utplwso2.tk/apipersona/3.0/personas', headers=headers)
    print(response)
    return render_template('personas.html', personas=response.json())

@app.route('/personas/delete/<idpersona>')
def delete_personas(idpersona):
    headers = {'apikey': API_KEY}
    response = requests.delete('https://utplwso2.tk/apipersona/3.0/personas/'+idpersona, headers=headers)
    print(response)
    return redirect(url_for('personas'))

@app.route('/personas', methods=['POST'])
def add():
    print("llego por aqui a guardar")
    nombre = request.form.get('nombre')
    identificacion = request.form.get('identificacion')
    edad = int(request.form.get('edad'))
    ciudad = request.form.get('ciudad')


    person_data = {"nombre": nombre, "edad": edad, "ciudad": ciudad, "identificacion": identificacion}

    headers = {'apikey': API_KEY}
    responseHabitacionesS = requests.post('https://utplwso2.tk/apipersona/3.0/personas', json=person_data, headers=headers)

    return redirect(url_for('personas'))

@app.route('/huespedes')
def huespedes():
    responseHabitaciones = requests.get('https://utpl-interoperabilidad-ejercicio1.onrender.com/v1_0/huesped')
    return render_template('huespedes.html', huespedesl=responseHabitaciones.json())

@app.route('/huespedes', methods=['POST'])
def addHuesped():
    print("llego por aqui a guardar huespedes")

    nombreValue = request.form.get('nombre')
    ciudad = request.form.get('ciudad')
    edad = int(request.form.get('edad'))
    hab = int(request.form.get('hab'))

    room_data = {
        "nombre": nombreValue,
        "ciudad": ciudad,
        "edad": edad,
        "hab": hab
    }

    responseHabitacionesS = requests.post('https://utpl-interoperabilidad-ejercicio1.onrender.com/v1_0/huesped', json=room_data)
    return redirect(url_for('huespedes'))

@app.route('/vehiculos')
def vehiculos():
    #headers = {'apikey': API_KEY}
    print('Buscando vehiculos')
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get('https://utplwso2.tk/apivehiculo/1.0/vehiculos', headers=headers)
    
    print(response.json())
    return render_template('vehiculos.html', listavehiculos=response.json())

@app.route('/vehiculos', methods=['POST'])
def addVehiculo():
    print("Guardando vehiculo")
    tipo = request.form.get('tipo')
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    anio = request.form.get('anio')
    color = request.form.get('color')
    descripcion = request.form.get('descripcion')

    vehiculo_data = {"tipo": tipo, "marca": marca, "modelo": modelo, "anio": anio, "color": color, "descripcion": descripcion}

    #headers = {'apikey': API_KEY}
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    responseVehiculosS = requests.post('https://utplwso2.tk/apivehiculo/1.0/vehiculos', json=vehiculo_data, headers=headers)

    return redirect(url_for('vehiculos'))


if __name__ == '__main__':
    app.run(debug=True)