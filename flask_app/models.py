from app import db, ma
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
import marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    created = db.Column(db.DateTime(), default=datetime.now())

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None
        
        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None
        
        return user
    
    def to_dict(self):
        return dict(id=self.id, name=self.name, email=self.email)


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Float())
    updated = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Procurement(db.Model):
    __tablename__ = 'procurement'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    currency = db.Column(db.String())
    unit_cost = db.Column(db.Float())
    unit_tax = db.Column(db.Float())
    quantity = db.Column(db.Float())
    total_cost = db.Column(db.Float())
    created = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    invoice_number = db.Column(db.String())
    currency = db.Column(db.String())
    total_tax = db.Column(db.Float())
    total_cost = db.Column(db.Float())
    date = db.Column(db.String())
    paid = db.Column(db.Boolean, default=False)
    terms = db.Column(db.Integer, default=30)
    delivery_number = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    items = relationship("Procurement", backref='invoice')
    payment = relationship("Payment", backref='payment')

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    payment_type = db.Column(db.String())
    cheque = db.Column(db.String())
    bank_transfer = db.Column(db.String())
    receipt = db.Column(db.String())
    date = db.Column(db.String())
    reason = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Supplier(db.Model):
    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    business_name = db.Column(db.String())
    contact_person = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    plus_code = db.Column(db.String())
    address = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    invoices = relationship("Invoice", backref='supplier')
    payments = relationship("Payment", backref='supplier') 

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.String(), nullable=False)
    sku = db.Column(db.String())
    code = db.Column(db.String())
    packing_type = db.Column(db.String())
    packing = db.Column(db.String())
    currency = db.Column(db.String())
    price = db.Column(db.Float())
    image_path = db.Column(db.String())
    additional_info = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    procurements = relationship("Procurement", backref='product')
    inventory = relationship("Inventory", backref='product')

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now())
    products = relationship("Product", backref='category')

    def __repr__(self):
        return '<id {}, category {}>'.format(self.id, self.name)

class MailList(db.Model):
    __tablename__ = 'maillist'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String())
    business = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    remark = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}, name {}, business {}, email {}, phone {}>'.format(self.id, self.name, self.business, self.email, self.phone)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category

class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
    category = ma.Nested(CategorySchema)

class InventorySchema(ma.ModelSchema):
    class Meta:
        model = Inventory

class ProcurementSchema(ma.ModelSchema):
    class Meta:
        model = Procurement
    product = ma.Nested(ProductSchema)

class SupplierSchema(ma.ModelSchema):
    class Meta:
        model = Supplier

class InvoiceSchema(ma.ModelSchema):
    class Meta:
        model = Invoice
    items = marshmallow.fields.List(ma.Nested(ProcurementSchema))
    supplier = ma.Nested(SupplierSchema)

class PaymentSchema(ma.ModelSchema):
    class Meta:
        model = Payment
    payment = ma.Nested(InvoiceSchema)

class MailListSchema(ma.ModelSchema):
    class Meta:
        model = MailList