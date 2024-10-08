from models import Merchant, Admin, Clerk, Request, Product, Store, SalesReport
from config import app, Resource, api, make_response, request, db

from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, jwt_required, JWTManager

app.config["JWT_SECRET_KEY"] = "b'Y\xf1Xz\x01\xad|eQ\x80t \xca\x1a\x10K'"  
app.config['JWT_TOKEN_LOCATION'] = ['headers']


jwt = JWTManager(app)   
from flask import Flask,jsonify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail


mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
              


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
        token = request.json.get('token')
        data = request.get_json()
        name = data.get("full_name")
        password = data.get("password")
        phone_number = data.get("phone_number")
        profilePicture = data.get("profilePicture")

        try:
            email = serializer.loads(token, salt='email-invite', max_age=86400)  # 1-day expiration
        except:
            return make_response({'message': 'Invalid or expired token.'},400)
        

        user = Admin.query.filter_by(invitation_token=token).first() or Clerk.query.filter_by(invitation_token=token).first()


        if not user:
            return make_response({'message': 'Invalid or expired token.'},400)

        try:
            user.username = name
            user.account_status = "active"
            user.phone_number = phone_number
            user.password_hash = password
            user.profilePicture = profilePicture
                
            db.session.commit()

            access_token = create_access_token(identity=user)
            return make_response({"user": user.to_dict(), 'access_token': access_token}, 201)
        except Exception as e:
            return {"error": e.args}, 422
        

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
        clerk_id = data.get("clerk_id")
        total_price = data.get("total_price")

        product = Product.query.filter_by(product_name=item).first()
        if product and product.closing_stock >= quantity:
            try:
                selling_price = total_price if total_price else product.selling_price * quantity
                sale = SalesReport(
                    date=date,
                    product_name=product.product_name,
                    product_id=product.id,
                    quantity_sold=quantity,
                    quantity_in_hand=product.closing_stock - quantity,
                    store_id=store_id,
                    clerk_id=clerk_id,
                    profit=selling_price - (product.buying_price * quantity)
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
        brand_name = data.get("brand_name")

        store = Store.query.filter_by(id=store_id).first()

        if product:
            product_id = product.id

            newRequest = Request(
                quantity=quantity,
                product_id=product_id,
                clerk_id=clerk_id,
                store_id=store_id,
            )
            db.session.add(newRequest)
            db.session.commit()
            
            admin = Admin.query.filter_by(store_id=store_id).first()
            clerk = Clerk.query.filter_by(id=clerk_id).first()
            print(admin.username)
            msg = Message("Supply request", recipients=[admin.email])
            msg.body = f"{clerk.username} has made a supply request for {product.product_name}. Log in to accept or reject it: https://brianhilsden.github.io/MyDuka-FrontEnd"
            try:
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")


            return make_response(newRequest.to_dict(), 201)
        else:
            new_product = Product(
                product_name=data.get("product_name"),
                brand_name=brand_name,
                buying_price=float(price),
                selling_price=float(price)*1.5,
                closing_stock=0,
                received_items=0,
                spoilt_items=0,
                availability=True,
                payment_status="unpaid",
                store_id=store_id,
            )

            db.session.add(new_product)
            db.session.commit()


            newRequest = Request(
                quantity=quantity,
                product_id=new_product.id,
                clerk_id=clerk_id,
                store_id=store_id,
            )
            db.session.add(newRequest)
            db.session.commit()
            admin = Admin.query.filter_by(store_id=store_id).first()
            clerk = Clerk.query.filter_by(id=clerk_id).first()
            print(clerk.username)
            msg = Message("Supply request", recipients=[admin.email])
            msg.body = f"{clerk.username} has made a supply request for {new_product.product_name}. Log in to accept or reject it: https://brianhilsden.github.io/MyDuka-FrontEnd"
            try:
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")
           


            return make_response(newRequest.to_dict(), 201)


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
                payment_status="unpaid",  
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

class inviteAdmin(Resource):
   def post(self):
    admin_email = request.json.get('email')
    store_id = request.json.get("store_id")

    
    token = serializer.dumps(admin_email, salt='email-invite')
 

    # Create a new Admin entry (or find existing by email)
    
    admin = Admin.query.filter_by(email=admin_email).first()
    if admin:
        return make_response({"error": "Unauthorized"}, 401)

    
    if not admin:
        admin = Admin(email=admin_email)
        db.session.add(admin)

    admin.invitation_token = token
    admin.role = 'Admin'  # Set the role as admin
    admin.account_status = 'pending'  # Set account status as pending
    admin.store_id = store_id
    db.session.commit()

    # Send the invitation email to the admin
    invite_url = f"https://brianhilsden.github.io/MyDuka-FrontEnd/#/signup?token={token}"

    msg = Message('Admin Sign Up Invitation', recipients=[admin_email])
    msg.body = f"You've been invited to sign up as an admin. Please use the following link to sign up: {invite_url}"
    mail.send(msg)
    
    return make_response({'message': 'Invitation sent to admin!'},200)
   
api.add_resource(inviteAdmin,"/inviteAdmin")




class inviteClerk(Resource):
    def post(self):
        clerk_email = request.json.get('email')
        store_id = request.json.get("store_id")

        # Generate a token for the invitation
        token = serializer.dumps(clerk_email, salt='email-invite')
    

        # Create a new Clerk entry (or find existing by email)
        clerk = Admin.query.filter_by(email=clerk_email).first()
        if not clerk:
            clerk= Clerk(email=clerk_email)
            db.session.add(clerk)

        clerk.invitation_token = token
        clerk.role = 'Clerk'  # Set the role as clerk
        clerk.account_status = 'pending'  # Set account status as pending
        clerk.store_id = store_id
        db.session.commit()

        # Send the invitation email to the clerk
        invite_url = f"https://brianhilsden.github.io/MyDuka-FrontEnd/#/signup?token={token}"

        msg = Message('Clerk Sign Up Invitation', recipients=[clerk_email])
        msg.body = f"You've been invited to sign up as a clerk. Please use the following link to sign up: {invite_url}"
        mail.send(msg)
        
        return make_response({'message': 'Invitation sent to clerk!'},200)
   
api.add_resource(inviteClerk,"/inviteClerk")
   
   
class ValidateToken(Resource):
    def post(self):
        token = request.json.get('token')
        try:
            email = serializer.loads(token, salt='email-invite', max_age=86400)  
        except:
            return jsonify({'valid': False, 'message': 'Invalid or expired token.'}), 400

        # Find the user by token
        user = Admin.query.filter_by(invitation_token=token).first() or Clerk.query.filter_by(invitation_token=token).first()
        if user:
            return make_response({'valid': True, 'email': user.email},200)
        else:
            return make_response({'valid': False, 'message': 'Invalid or expired token.'},400)
        
api.add_resource(ValidateToken,"/validate-token")

        
class GetAllStores(Resource):
    def get(self):
        stores = Store.query.all()
        return make_response([store.to_dict() for store in stores], 200)

api.add_resource(GetAllStores, "/stores")

class editProduct(Resource):
    def patch(self, id):
        data = request.get_json()
        product = Product.query.filter_by(id=id).first()
        if product:
            if "buying_price" in data:
                product.buying_price = float(data["buying_price"])
            if "selling_price" in data:
                product.selling_price = float(data["selling_price"])

            if "spoilt_items" in data:
                product.spoilt_items = int(data["spoilt_items"])
            
            try:
                db.session.commit()
                return make_response(product.to_dict(), 200)
            except Exception as e:
                return make_response({"error": str(e)}, 500)
        return make_response({"error": "Product not found"}, 404)
    
api.add_resource(editProduct,"/updateProduct/<int:id>")


class addProduct(Resource):
    def post(self,store_id):
        data = request.get_json()
        brand_name = data.get("brand_name")
        product_name = data.get("product_name")
        payment_status = "unpaid"
        closing_stock = data.get("number_of_items")
        buying_price = data.get("buying_price")
        selling_price = data.get("selling_price")
        store_id = store_id
        

        product = Product(
                brand_name=brand_name,  
                product_name=product_name,  
                payment_status=payment_status,  
                received_items=closing_stock,
                closing_stock=closing_stock,
                spoilt_items=0,
                buying_price=buying_price,  
                selling_price=selling_price,  
                store_id=store_id
                )
        db.session.add(product)
            
        db.session.commit()
        response = make_response(product.to_dict(),201)
        return response

api.add_resource(addProduct,'/addProduct/<int:store_id>')

class editUser(Resource):
    def patch(self,id):
        data = request.get_json()
        if data.get("role") == "Merchant":
            user = Merchant.query.filter_by(id=id).first()
            print("A")
            
            for attr in data:
                setattr(user,attr,data[attr])
            db.session.add(user)
            db.session.commit()

            response = make_response(user.to_dict(),200,{"Content-Type":"application/json"})
            return response
        elif data.get("role") == "Admin":
            print("B")
            user = Admin.query.filter_by(id=id).first()
            for attr in data:
                setattr(user,attr,data[attr])
            db.session.add(user)
            db.session.commit()

            response = make_response(user.to_dict(),200,{"Content-Type":"application/json"})
            return response

        else:
            print("C")
            user = Clerk.query.filter_by(id=id).first()
            for attr in data:
                setattr(user,attr,data[attr])
            db.session.add(user)
            db.session.commit()

            response = make_response(user.to_dict(),200,{"Content-Type":"application/json"})
            return response


api.add_resource(editUser,"/editUser/<int:id>")


class addStore(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        location = data.get("location")
        merchant = Merchant.query.first()

        store = Store(
            name=name,
            location=location,
            merchant_id = merchant.id

        )
        db.session.add(store)
        db.session.commit()


        response = make_response(store.to_dict(),201)
        return response
    
api.add_resource(addStore,"/addStore")


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return email

@app.route('/api/reset_password_request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')
    role = data.get("role")
    user_class = {"Merchant": Merchant, "Admin": Admin, "Clerk": Clerk}.get(role)
    if not user_class:
        return make_response({"error": "Invalid role"}, 400)

    user = user_class.query.filter_by(email=email).first()
    if user:
        token = generate_reset_token(user.email)
        reset_url = f"https://brianhilsden.github.io/MyDuka-FrontEnd/#/reset-password/{token}"
        send_reset_email(user.email, reset_url)
        return jsonify({"message": "Check your email for the instructions to reset your password"}), 200
    return jsonify({"message": "No account found with that email"}), 404

# API endpoint to handle the password reset
@app.route('/api/reset_password/<token>', methods=['POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        return jsonify({"message": "The reset link is invalid or has expired."}), 400
    
    data = request.get_json()
    new_password = data.get('password')
    role = data.get("role")
    user_class = {"Merchant": Merchant, "Admin": Admin, "Clerk": Clerk}.get(role)
    if not user_class:
        return make_response({"error": "Invalid role"}, 400)

    user = user_class.query.filter_by(email=email).first()
   
    
    if user:
        user.password_hash = new_password
        db.session.commit()
        return jsonify({"message": "Your password has been updated."}), 200
    
    return jsonify({"message": "User not found."}), 404


def send_reset_email(to_email, reset_url):
    msg = Message("Password Reset Request", recipients=[to_email])
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)




if __name__ == "__main__":
    app.run(debug=True,port=5555)
