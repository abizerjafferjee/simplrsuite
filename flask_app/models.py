from app import db, ma
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.orm import relationship
from datetime import datetime
import marshmallow



class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Float())
    updated = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Procurement(db.Model):
    __tablename__ = 'procurement'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    unit_cost = db.Column(db.Float())
    quantity = db.Column(db.Float())
    total_cost = db.Column(db.Float())
    currency = db.Column(db.String())
    invoice = db.Column(db.String())
    paid = db.Column(db.String())
    additional_info = db.Column(db.String())
    location = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    amount = db.Column(db.Float())
    currency = db.Column(db.String())
    invoices = db.Column(db.String())
    additional_info = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}>'.format(self.id)

# def generateSKU(context):
#     params = context.get_current_parameters()
#     product = params['description']
#     category_id = params['category_id']
#     id = params['id']
#     return product + str(category_id) + "00" + str(id)

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.String())
    sku = db.Column(db.String())
    code = db.Column(db.String())
    product_type = db.Column(db.String())
    packing_type = db.Column(db.String())
    packing = db.Column(db.String())
    currency = db.Column(db.String())
    price = db.Column(db.Float())
    image_path = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    procurements = relationship("Procurement", backref='product')
    inventory = relationship("Inventory", backref='product')

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Supplier(db.Model):
    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String())
    contact_person = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    plus_code = db.Column(db.String())
    address = db.Column(db.String())
    additional_info = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    procurements = relationship("Procurement", backref='supplier') 

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    products = relationship("Product", backref='category')

    def __repr__(self):
        return '<id {}, category {}>'.format(self.id, self.name)

class MailList(db.Model):
    __tablename__ = 'maillist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    business = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    remark = db.Column(db.String())
    created = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return '<id {}, name {}, business {}, email {}, phone {}>'.format(self.id, self.name, self.business, self.email, self.phone)

class SupplierSchema(ma.ModelSchema):
    class Meta:
        model = Supplier

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
    supplier = ma.Nested(SupplierSchema)

class MailListSchema(ma.ModelSchema):
    class Meta:
        model = MailList

class PaymentSchema(ma.ModelSchema):
    class Meta:
        model = Payment

class OutstandingPaymentsSchema(ma.Schema):
    supplier_id = marshmallow.fields.Integer()
    total_cost = marshmallow.fields.Number()
    invoices = marshmallow.fields.List(marshmallow.fields.String())
    business_name = marshmallow.fields.String()