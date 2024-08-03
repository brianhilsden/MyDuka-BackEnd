from models import User,Request,Product,Store,SalesReport
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
        name = data.get("full_name")
        email = data.get("email")
        role = data.get("role")
        store_id = data.get("store_id")
        password = data.get("password")
        phone_number = data.get("phone_number")

        user = User.query.filter_by(email=email).first()

        if not user:
            try:
                user = User(
                    username = name,
                    email = email,
                    role = role,
                    store_id = store_id,
                    phone_number = phone_number

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
            username = data.get("full_name")
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



class GetItem(Resource):
    def get(self,store_id):
        products = Product.query.filter_by(store_id=store_id).all()
        response = make_response([product.to_dict() for product in products],200)
        return response
    
api.add_resource(GetItem,"/getItemssale/<int:store_id>")

class Sales(Resource):
    def get(self):
        sales = SalesReport.query.all()
        response = make_response({"sales":[sale.to_dict() for sale in sales]},200)
        return response
    
    def post(self):
        data = request.get_json()
        date = data.get("date")
        item = data.get("product_name")
        quantity = data.get("quantity")

        product = Product.query.filter_by(product_name = item).first()
        print(item)
        if product:
            if product.closing_stock >= quantity:
                try:
                    
                    sale = SalesReport(
                        date = date,
                        product_name = product.product_name,
                        product_id = product.id,
                        quantity_sold = quantity,
                        quantity_in_hand = product.closing_stock - quantity,
                        profit = (product.selling_price * quantity) - (product.buying_price * quantity)
                    )
                    product.closing_stock -= quantity
                    db.session.add(product)
                    db.session.add(sale)
                    db.session.commit()
                    return make_response({"message": "Sale recorded successfully", "product": product.to_dict(rules=("-salesReport",)),"salesReport":sale.to_dict()}, 200)
                except Exception as e:
                    db.session.rollback()
                    return make_response({"error": str(e)}, 500)
            else:
                return make_response({"error":"Insufficient stock"},404)
            
        else:
            return make_response({"error":"Product not found"},404)
        

api.add_resource(Sales,"/sales")

"""To be reviewed"""
class Requests(Resource):
    def get(self,store_id):
    
        requests = Request.query.filter_by(store_id = store_id)
        response = make_response([requestedItem.to_dict() for requestedItem in requests],200)
        return response
    
    def post(self,store_id):
        data = request.get_json()
        product = Product.query.filter_by(product_name= data.get("product_name")).first()
        quantity = data.get("stock")
        clerk_id = data.get("clerk_id")
        price = data.get("product_price")
        category = data.get("category")

        store= Store.query.filter_by(id=store_id).first()
        admin_id = store.admin_id
        if product:
            product_id = product.id
            
            newRequest = Request(
                quantity = quantity,
                product_id = product_id,
                clerk_id = clerk_id,
                admin_id = admin_id,
                store_id = store_id
            )
            db.session.add(newRequest)
            db.session.commit()
            response = make_response(newRequest.to_dict(),201)
            return response

        else:
            return make_response({"error":"The product does not exist"},404)
      

    
api.add_resource(Requests,"/request/<int:store_id>")



if __name__ == "__main__":
    app.run(port=5555,debug=True)