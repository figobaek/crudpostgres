# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker, relationship

from app import db, login_manager


student_interview = db.Table('student_interview', db.Model.metadata,
    db.Column('departments_id', db.Integer, db.ForeignKey('departments.id')),
    db.Column('employees_id', db.Integer, db.ForeignKey('employees.id'))
)


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    departments = relationship("Department", secondary=student_interview, backref="interviews")

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
# class Role(db.Model):
#     """
#     Create a Role table
#     """

#     __tablename__ = 'roles'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True)
#     description = db.Column(db.String(200))
#     employees = db.relationship('Employee', backref='role',
#                                 lazy='dynamic')

#     def __repr__(self):
#         return '<Role: {}>'.format(self.name)

# association_table = Table('association', Base.metadata,
#     Column('left_id', Integer, ForeignKey('left.id')),
#     Column('right_id', Integer, ForeignKey('right.id'))
# )

# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#     children = relationship(
#         "Child",
#         secondary=association_table,
#         back_populates="parents")

# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)
#     parents = relationship(
#         "Parent",
#         secondary=association_table,
#         back_populates="children")





# 부모 = 임플로이 
# 자식 = 디파트먼트
# 다대다 = 상담, 임플-디파 

# student_identifier = db.Table('student_identifier',
#     db.Column('class_id', db.Integer, db.ForeignKey('classes.class_id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('students.user_id'))
# )

# class Student(db.Model):
#     __tablename__ = 'students'
#     user_id = db.Column(db.Integer, primary_key=True)
#     user_fistName = db.Column(db.String(64))
#     user_lastName = db.Column(db.String(64))
#     user_email = db.Column(db.String(128), unique=True)


# class Class(db.Model):
#     __tablename__ = 'classes'
#     class_id = db.Column(db.Integer, primary_key=True)
#     class_name = db.Column(db.String(128), unique=True)
#     students = db.relationship("Student",
#                                secondary=student_identifier)

# s = Student()
# c = Class()
# c.students.append(s)
# db.session.add(c)
# db.session.commit()

