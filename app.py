from models import Merchant, Admin, Clerk, Request, Product, Store, SalesReport
from config import app, Resource, api, make_response, request, db

from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, jwt_required, JWTManager

app.config["JWT_SECRET_KEY"] = "b'Y\xf1Xz\x01\xad|eQ\x80t \xca\x1a\x10K'"  
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"id": user.id, "role": user.__class__.__name__} 

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user_id = identity["id"]
    role = identity["role"]
    
    if role == "Merchant":
        return Merchant.query.filter_by(id=user_id).one_or_none()
    elif role == "Admin":
        return Admin.query.filter_by(id=user_id).one_or_none()
    elif role == "Clerk":
        return Clerk.query.filter_by(id=user_id).one_or_none()
    else:
        return None

class SignUp(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("full_name")
        email = data.get("email")
        role = data.get("role")
        store_id = data.get("store_id")
        password = data.get("password")
        phone_number = data.get("phone_number")

        user_class = {"Merchant": Merchant, "Admin": Admin, "Clerk": Clerk}.get(role)
        if not user_class:
            return make_response({"error": "Invalid role"}, 400)

        user = user_class.query.filter_by(email=email).first()

        if not user:
            try:
                user = user_class(
                    username=name,
                    email=email,
                    store_id=store_id,
                )
                user.password_hash = password
                
                db.session.add(user)
                db.session.commit()

                access_token = create_access_token(identity=user)
                return make_response({"user": user.to_dict(), 'access_token': access_token}, 201)
            except Exception as e:
                return {"error": e.args}, 422
        else:
            return make_response({"error": "Email already registered, kindly log in"}, 401)

api.add_resource(SignUp, "/signup")

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        user_class = {"Merchant": Merchant, "Admin": Admin, "Clerk": Clerk}.get(role)
        if not user_class:
            return make_response({"error": "Invalid role"}, 400)

        user = user_class.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            access_token = create_access_token(identity=user)
            return make_response({"user": user.to_dict(), "access_token": access_token}, 201)
        else:
            return make_response({"error": "Unauthorized"}, 401)

api.add_resource(Login, "/login")

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        return make_response(current_user.to_dict(), 200)

api.add_resource(CheckSession, '/check_session', endpoint="check_session")

class GetSpecificStoreProducts(Resource):
    def get(self, store_id):
        products = Product.query.filter_by(store_id=store_id).all()
        print(products)
        return make_response([product.to_dict() for product in products], 200)

api.add_resource(GetSpecificStoreProducts, "/getProducts/<int:store_id>")

class Sales(Resource):
    def get(self, store_id):
        sales = SalesReport.query.filter_by(store_id=store_id).order_by(SalesReport.date.desc()).all()
        return make_response({"sales": [sale.to_dict() for sale in sales]}, 200)
    
    def post(self, store_id):
        data = request.get_json()
        date = data.get("date")
        item = data.get("product_name")
        quantity = data.get("quantity")
        total_price = data.get("total_price")

        product = Product.query.filter_by(product_name=item).first()
        if product and product.closing_stock >= quantity:
            try:
                sale = SalesReport(
                    date=date,
                    product_name=product.product_name,
                    product_id=product.id,
                    quantity_sold=quantity,
                    quantity_in_hand=product.closing_stock - quantity,
                    store_id=store_id,
                    profit=(product.selling_price * quantity) - (product.buying_price * quantity)
                )
                product.closing_stock -= quantity
                db.session.add(product)
                db.session.add(sale)
                db.session.commit()
                return make_response({"message": "Sale recorded successfully", "product": product.to_dict(rules=("-salesReport",)), "salesReport": sale.to_dict()}, 200)
            except Exception as e:
                db.session.rollback()
                return make_response({"error": str(e)}, 500)
        elif product:
            return make_response({"error": "Insufficient stock"}, 404)
        else:
            return make_response({"error": "Product not found"}, 404)

api.add_resource(Sales, "/sales/<int:store_id>")

class Requests(Resource):
    def get(self, store_id):
        requests = Request.query.filter_by(store_id=store_id).all()
        return make_response([requestedItem.to_dict() for requestedItem in requests], 200)
    
    def post(self, store_id):
        data = request.get_json()
        product = Product.query.filter_by(product_name=data.get("product_name")).first()
        quantity = data.get("stock")
        clerk_id = data.get("clerk_id")
        price = data.get("product_price")
        category = data.get("category")

        store = Store.query.filter_by(id=store_id).first()
        

        if product:
            product_id = product.id

            newRequest = Request(
                quantity=quantity,
                product_id=product_id,
                clerk_id=clerk_id,
                store_id=store_id
            )
            db.session.add(newRequest)
            db.session.commit()
            return make_response(newRequest.to_dict(), 201)
        else:
            return make_response({"error": "The product does not exist"}, 404)

api.add_resource(Requests, "/requests/<int:store_id>")

class PaymentStatus(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            product.payment_status = "paid"
            db.session.commit() 
            return make_response(product.to_dict(), 200)
        return make_response({"error": "Product not found"}, 404)

api.add_resource(PaymentStatus, "/paymentStatus/<int:id>")


class ClerkAccountStatus(Resource):

    def get(self, id):
        user = Clerk.query.filter_by(id=id).first()
        if user:
            user.account_status = "inactive" if user.account_status == "active" else "active"
            db.session.commit()
            return make_response({"message": f'Status changed to {user.account_status}'}, 200)
        return make_response({"error": "User not found"}, 404)
    
    def delete(self, id):
        user = Clerk.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit() 
            return make_response({"message": "User deleted successfully"}, 200)
        return make_response({"error": "User not found"}, 404)

api.add_resource(ClerkAccountStatus, "/clerkAccountStatus/<int:id>")

class AdminAccountStatus(Resource):

    def get(self, id):
        user = Admin.query.filter_by(id=id).first()
        if user:
            user.account_status = "inactive" if user.account_status == "active" else "active"
            db.session.commit()
            return make_response({"status":user.account_status}, 200)
        return make_response({"error": "User not found"}, 404)
    
    def delete(self, id):
        user = Admin.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit() 
            return make_response({"message": "User deleted successfully"}, 200)
        return make_response({"error": "User not found"}, 404)

api.add_resource(AdminAccountStatus, "/adminAccountStatus/<int:id>")


class GetClerk(Resource):
    def get(self, store_id):
        store = Store.query.filter_by(id=store_id).first()
        clerks= store.clerks
     
        if clerks[0]:
            return make_response([clerk.to_dict(rules=("-store",)) for clerk in clerks], 200)
        return make_response({"error": "Clerk not found"}, 404)

api.add_resource(GetClerk, "/getClerk/<int:store_id>")


class AcceptRequests(Resource):
    def get(self, id):
        request = Request.query.filter_by(id=id).first() 
        if not request:
            return make_response({"message": "No such requests found"}, 404)
        
        
        product = Product.query.filter_by(id=request.product_id).first()
        if product:
            product.closing_stock += request.quantity
            request.status = "approved"
            db.session.commit()
        else:
            product = Product(
                id=request.product_id,
                brand_name="Unknown",  
                product_name="Unknown",  
                availability=True,
                payment_status="Not Paid",  
                received_items=request.quantity,
                closing_stock=request.quantity,
                spoilt_items=0,
                buying_price=0.0,  
                selling_price=0.0,  
                store_id=request.store_id
                )
            db.session.add(product)
            
            db.session.commit()
        
        Request.query.filter_by(id=id).delete()
        db.session.commit()
        
        return make_response({"message": "Request has been accepted and processed"}, 200)
    
    def delete(self, id):
        deleted_request = Request.query.filter_by(id=id).delete()
        deleted_request.status = "declined"
        db.session.commit()
        
        return make_response({"message": f"Deleted {deleted_request} request for the product"}, 200)
    
api.add_resource(AcceptRequests,"/acceptRequests/<int:id>")


class getAdmins(Resource):
    def get(self):
        admins = Admin.query.all()
        response = make_response([admin.to_dict(rules=("-requests","-store")) for admin in admins],200)
        return response
    

api.add_resource(getAdmins,"/getAdmins")






if __name__ == "__main__":
    app.run(port=5555, debug=True)