from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

# Define the base model that your classes will extend
Base = declarative_base()

# Association table for the many-to-many relationship between User and ParameterVersion
user_parameter_versions_table = Table('user_parameter_versions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('version_id', Integer, ForeignKey('parameter_versions.id')),
    Column('modification_date', DateTime, default=datetime.datetime.utcnow)
)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    # Relationship with ParameterVersion
    parameter_versions = relationship('ParameterVersion', back_populates='project')

class Parameter(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data_type = Column(String)
    default_value = Column(String)
    description = Column(String)
    # Relationship with ParameterVersion
    versions = relationship('ParameterVersion', back_populates='parameter')

class ParameterVersion(Base):
    __tablename__ = 'parameter_versions'
    id = Column(Integer, primary_key=True)
    parameter_id = Column(Integer, ForeignKey('parameters.id'))
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    custom_value = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    # Relationships with Project and Parameter
    project = relationship('Project', back_populates='parameter_versions')
    parameter = relationship('Parameter', back_populates='versions')
    # Many-to-many relationship with User
    modified_by = relationship('User', secondary=user_parameter_versions_table, back_populates='parameter_versions')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True)
    last_login = Column(DateTime)
    role_id = Column(Integer, ForeignKey('roles.id'))
    # Relationships
    parameter_versions = relationship('ParameterVersion', secondary=user_parameter_versions_table, back_populates='modified_by')
    role = relationship('Role', back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role_name = Column(String, unique=True, nullable=False)
    # Relationship with User
    users = relationship('User', back_populates='role')

# Create the engine to connect to the database
engine = create_engine('sqlite:///revit_parameters.db', echo=True)

# Bind the engine to the metadata of the Base class
Base.metadata.bind = engine

# Create a DBSession class
DBSession = sessionmaker(bind=engine)

# Create all tables in the database
Base.metadata.create_all(engine)

# Populate the tables with some initial data
session = DBSession()

# Add sample roles
admin_role = Role(role_name='Admin')
user_role = Role(role_name='User')
session.add(admin_role)
session.add(user_role)
session.commit()

# Add sample users
admin_user = User(username='admin', password_hash='admin_hashed_password', email='admin@example.com', role=admin_role)
regular_user = User(username='johndoe', password_hash='johndoe_hashed_password', email='john.doe@example.com', role=user_role)
session.add(admin_user)
session.add(regular_user)
session.commit()

# Add sample projects
sample_project = Project(name='Sample Project 1', description='This is a sample project.')
session.add(sample_project)
session.commit()

# Add sample parameters
sample_parameter = Parameter(name='Wall Thickness', data_type='Integer', default_value='200', description='Thickness of the wall in mm')
session.add(sample_parameter)
session.commit()

# Add parameter versions
sample_version = ParameterVersion(parameter=sample_parameter, custom_value='180', project=sample_project, is_active=True)
session.add(sample_version)
session.commit()

# Assign users to parameter version via the association table
sample_version.modified_by.append(admin_user)
sample_version.modified_by.append(regular_user)
session.commit()

# Commit and close the session
session.close()