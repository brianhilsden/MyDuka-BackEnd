from models import User,Request,Product,Store
from config import app,Resource,api,make_response,request,db


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity,current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app.config["JWT_SECRET_KEY"] = "b'Y\xf1Xz\x01\xad|eQ\x80t \xca\x1a\x10K'"  
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        role = data.get("role")
        store_id = data.get("store_id")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            try:
                user = User(
                    username = name,
                    email = email,
                    role = role,
                    store_id = store_id

                )
                user.password_hash = password

                db.session.add(user)
                db.session.commit()

                access_token = create_access_token(identity=user)

                return make_response({"user":user.to_dict(),'access_token': access_token},201)
            except Exception as e:
                return {"error":e.args},422
            
        else:
            return make_response({"error":"Email already registered, kindly log in"},401)
        
api.add_resource(SignUp,"/signup")


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email = data.get("email")).first()
        if user:
            if user.verify_password(data.get("password")):
                access_token = create_access_token(identity=user)
                response = make_response({"user":user.to_dict(),"access_token":access_token},201)
                return response
            
            else:
                return make_response({"error":"Incorrect password"},401)
            
        else:
            return make_response({"error":"Unauthorized"},401)

api.add_resource(Login,"/login")

class CheckSession(Resource):
     @jwt_required()
     def get(self):
        return make_response(current_user.to_dict(),200)
api.add_resource(CheckSession,'/check_session',endpoint="check_session")






if __name__ == "__main__":
    app.run(port=5555,debug=True)