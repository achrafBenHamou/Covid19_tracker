from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/trackingCovid19'
app.config['JWT_SECRET_KEY']='cqewedsfddtwrerEEEEWWWvdjgvdjdvhdvk562552424hdvhdvdvdvKHSHFFAEAF'

jwt=JWTManager(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
key_app = 'elhakouni@benhamou@cherradi'
@app.route('/test', methods=['POST'])
def test():
    key = request.get_json()["key"]
    if key_app == key:
        return jsonify({"test":"succefull"})
    else:
        return jsonify({"error":"key incompatible"})

@app.route('/citoyens/register', methods=['POST'])
def register_citoyen():
    key = request.get_json()["key"]
    if key_app == key:
        from cors.use_cases import register_citoyen
        return jsonify(register_citoyen())
    else:
        return jsonify({"error":"key incompatible"})

@app.route('/citoyens/login', methods=['POST'])
def login_citoyen():
    key = request.get_json()["key"]
    if key_app == key:
        from cors.use_cases import login_citoyen
        return jsonify(login_citoyen())
    else:
        return jsonify({"error":"key incompatible"})

@app.route('/getAllCitoyens', methods=['GET'])
def get_all_citoyens():
   from data_providers.Document_db import getAllCitoyens
   return jsonify(getAllCitoyens())

@app.route('/getAllCitoyens/<region>', methods=['GET'])
def getCitoyenByRegion(region):
    from data_providers.Document_db import get_citoyen_ByRegion
    return jsonify(get_citoyen_ByRegion(region))

@app.route('/getAllCitoyens/province/<province>', methods=['GET'])
@jwt_required
def getCitoyenByProvince(province):
    from data_providers.Document_db import get_citoyen_ByProvince
    return jsonify(get_citoyen_ByProvince(province))

@app.route('/getAllCitoyens/hopital/<hopital>', methods=['GET'])
@jwt_required
def getCitoyenByHopital(hopital):
    from data_providers.Document_db import get_citoyen_ByHopital
    listCitoyens=get_citoyen_ByHopital(hopital)
    ##print(listCitoyens)
    return render_template('listOfCitoyens.html', allCitoyens = listCitoyens)

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['POST'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/hopital/login', methods=['POST'])
def login_hopital():
    from cors.use_cases import loginHopital
    return jsonify(loginHopital())

@app.route('/regions', methods=['POST'])
def get_all_regions():
    key = request.get_json()["key"]
    if key_app == key:
        from data_providers.Document_db import getAllRegions
        return jsonify(getAllRegions())
    else:
        return jsonify({"error":"key incompatible"})


@app.route('/provinces', methods=['POST'])
def get_provinces_region():
    key = request.get_json()["key"]
    if key_app == key:
        region = request.get_json()["region"]
        from data_providers.Document_db import getProvincesByRegion
        return jsonify(getProvincesByRegion(region))
    else:
        return jsonify({"error":"key incompatible"})

@app.route('/communautes', methods=['POST'])
def get_communautes():
    key = request.get_json()["key"]
    if key_app == key:
        region = request.get_json()["region"]
        province = request.get_json()["province"]
        from data_providers.Document_db import getCommunautes
        return jsonify(getCommunautes(region,province))
    else:
        return jsonify({"error": "key incompatible"})

@app.route('/boycotts', methods=['POST'])
def get_boycotts():
    key = request.get_json()["key"]
    if key_app == key:
        region = request.get_json()["region"]
        province = request.get_json()["province"]
        comunaute = request.get_json()["comunaute"]
        from data_providers.Document_db import getBoycotts
        return jsonify(getBoycotts(region,province,comunaute))
    else:
        return jsonify({"error": "key incompatible"})

@app.route('/authentication')
def auth():
    username = request.args.get('username')
    password = request.args.get('password')
    citoyens = mongo.db.citoyens
    output = []
    for c in citoyens.find():
        output.append({'nom' : c['nom'], 'prenom' : c['prenom'], 'email': c['email'], 'password': c['password'], 'CIN': c['CIN'], 'tel': c['tel'], 'region': c['region']})
    for k in range(len(output)):
        if output[k]['CIN'] == username and output[k]['password'] == password:
            msg = "your login and password is correct !!!"
            break
        else:
            msg = "your login or password is incorrect !!!"
    #print(msg)
    return "Authentication: {}".format(msg)



if __name__ == "__main__":
    app.run(debug=True)
