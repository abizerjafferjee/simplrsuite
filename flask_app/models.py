from app import db, ma
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.orm import relationship



class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Float())

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
    invoice = db.Column(db.String())
    additional_info = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id) 

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.String())
    code = db.Column(db.String())
    packing = db.Column(db.String())
    price = db.Column(db.Float())
    image_path = db.Column(db.String())
    created = db.Column(db.DateTime())

    procurements = relationship("Procurement", backref='product')
    inventory = relationship("Inventory", backref='product')

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

    def __repr__(self):
        return '<id {}, name {}, business {}, email {}, phone {}>'.format(self.id, self.name, self.business, self.email, self.phone)

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

    procurements = relationship("Procurement", backref='supplier') 

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String())
    contact_person = db.Column(db.String())
    email_one = db.Column(db.String())
    email_two = db.Column(db.String())
    phone_one = db.Column(db.String())
    phone_two = db.Column(db.String())
    plus_code = db.Column(db.String())
    additional_info = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)

class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Customer

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

class MailListSchema(ma.ModelSchema):
    class Meta:
        model = MailList

class InventorySchema(ma.ModelSchema):
    class Meta:
        model = Inventory

class ProcurementSchema(ma.ModelSchema):
    class Meta:
        model = Procurement

    product = ma.Nested(ProductSchema)
    supplier = ma.Nested(SupplierSchema)