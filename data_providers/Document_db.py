from bson import ObjectId

from app import mongo
from datetime import datetime

def insert_new_citoyen(new_citoyen, cryptage):
    citoyens = mongo.db.citoyens
    user_id = citoyens.insert({
    'nom' :new_citoyen.nom,
    'prenom':new_citoyen.prenom,
    'email' :new_citoyen.email,
    'password': new_citoyen.password,
    'CIN': new_citoyen.CIN,
    'tel' : new_citoyen.tel,
    'region' : new_citoyen.region,
    'province' : new_citoyen.province,
    'Communaute' : new_citoyen.Communaute,
    'hopital' : new_citoyen.hopital,
    'date_created': datetime.utcnow(),
    'key' :cryptage
    })
    citoyen = citoyens.find_one({'_id': user_id})
    return citoyen["key"]

def getCitoyenByCIN(CIN):
    citoyens = mongo.db.citoyens
    citoyen = citoyens.find_one({'CIN': CIN})
    return  citoyen

def getAllCitoyens():
    citoyens = mongo.db.citoyens
    output = []
    for c in citoyens.find():
        output.append({'nom' : c['nom'], 'prenom' : c['prenom'], 'email': c['email'], 'password': c['password'], 'CIN': c['CIN'], 'tel': c['tel'], 'region': c['region']})
    return {'result' : output}

def get_citoyen_ByRegion(region):
    citoyens = mongo.db.citoyens
    output = []
    for c in citoyens.find({'region': region}):
        output.append({'region': c['region'], 'province': c['province']})
    return {'result' : output}

def get_citoyen_ByProvince(province):
    citoyens = mongo.db.citoyens
    output = []
    for c in citoyens.find({'province': province}):
        output.append({'province': c['province'], 'region': c['region']})
    return {'result' : output}
def get_citoyen_ByHopital(hopital):
    citoyens = mongo.db.citoyens
    output = []
    for c in citoyens.find({'hopital': hopital}):
        output.append({'nom' : c['nom'], 'prenom' : c['prenom'], 'email': c['email'], 'password': c['password'], 'CIN': c['CIN'], 'tel': c['tel'], 'region': c['region']})
    print(output)
    return output

def getAllRegions():
    regions = mongo.db.regions
    for c in regions.find():
        output = []
        for k in c.keys():
            output.append(k)
    return {'result': output[1:]}

def getProvincesByRegion(Region):
    region = mongo.db.regions.find_one(ObjectId("5ea995e2260bd649c215dd7c"))
    provinces=region[Region]['provinces']
    output = []
    for key in provinces.keys():
        output.append(key)
    return {'result':output}

def getCommunautes(Region,province):
    region = mongo.db.regions.find_one(ObjectId("5ea995e2260bd649c215dd7c"))
    Communautes = region[Region]['provinces'][province]["comunautes"]
    output = []
    for key in Communautes.keys():
        output.append(key)
    return {'result':output}

def getBoycotts (Region,province,comunaute):
    region = mongo.db.regions.find_one(ObjectId("5ea995e2260bd649c215dd7c"))
    Boycotts = region[Region]['provinces'][province]["comunautes"][comunaute]["mo9ata3at"]
    return {'result':Boycotts}


def get_citoyen_ByRegion(region):
    citoyens = mongo.db.citoyens
    output = []
    for c in citoyens.find({'region': region}):
        output.append({'region': c['region'], 'province': c['province']})
    return {'result' : output}