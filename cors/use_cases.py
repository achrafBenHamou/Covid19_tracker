from flask_jwt_extended import create_access_token

from app import bcrypt
from flask import request
#import app
from cors.Entities import Citoyen
from data_providers.Document_db import insert_new_citoyen, getCitoyenByCIN, getHopitalByEmail


def register_citoyen():
    nom = request.get_json()["nom"]
    prenom = request.get_json()["prenom"]
    email = request.get_json()["email"]
    password = bcrypt.generate_password_hash(request.get_json()["password"]).decode('utf-8')
    CIN = request.get_json()["CIN"]
    tel = request.get_json()["tel"]
    region = request.get_json()["region"]
    province = request.get_json()["province"]
    Communaute = request.get_json()["Communaute"]
    hopital = request.get_json()["hopital"]

    citoyen = getCitoyenByCIN(CIN)
    if citoyen:
        return {"error": "we have this CIN enrigistred"}
    else:
        new_citoyen = Citoyen(nom, prenom, email, password, CIN, tel, region, province, Communaute, hopital)
        creptage = bcrypt.generate_password_hash(CIN + '|#@&&%^' + nom + '|#@&&%^' + prenom).decode('utf-8')
        insertion_citoyen = insert_new_citoyen(new_citoyen, creptage)
        return {'citoyen_inserted':insertion_citoyen}

def login_citoyen():
    #request.headers.get('key')
    CIN = request.get_json()["CIN"]
    password = request.get_json()["password"]

    citoyen = getCitoyenByCIN(CIN)

    if citoyen:
        if bcrypt.check_password_hash(citoyen['password'], password):
            return {"succes": [citoyen['CIN'],citoyen['nom'],citoyen['prenom']]}
        else:
            return {"error": "invalid password"}
    else:
        return {"result": "No CIN found"}

def loginHopital():
    output = {}
    if request.method == "POST":
        email=request.get_json()["email"]
        pswd_user=request.get_json()["password"]
        hopital=getHopitalByEmail(email)
        print(hopital)
        if hopital:
            ## password hash bcrypt
            if hopital['password']== pswd_user:
                access_token = create_access_token(identity = {
                    'nom': hopital['nom'],
                    'email': hopital['email'],
                    'tel': hopital['tel']} )

                output = {"token" : access_token}
            else:
                output = {"error" : "invalid password"}
        else :
            output = {"result" : "No result foud"}
    return output