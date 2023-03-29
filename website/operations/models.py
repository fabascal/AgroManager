# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - Present Felix Abascal
"""
from flask_login import UserMixin
from website import db , login_manager, ma
from website.authentication.utils import hash_pass
from sqlalchemy.sql import func
from sqlalchemy import event
import sys, os, json
import enum

class TipoPredio(enum.Enum):
    PROPIO = 'Propio'
    RENTADO = 'Rentado'
    
class Predio(db.Model):
    __tablename__='predios'
    PROPIO = 'PROPIO'
    RENTADO = 'RENTADO'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    id_ciclo = db.Column(db.Integer, db.ForeignKey('ciclos.id'), nullable=True, index=True)
    tipo_predio = db.Column(db.Enum(TipoPredio))
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=True, index=True)
    id_municipio = db.Column(db.Integer, db.ForeignKey('municipios.id'), nullable=True, index=True)
    potrero = db.Column(db.String(50))
    ejido = db.Column(db.String(100))
    certificado_parcelario = db.Column(db.String(20))
    no_parcela = db.Column(db.String(20))
    superficie = db.Column(db.Float)
    propietario = db.relationship('Propietario', backref='propietario', passive_deletes=True)
    renta = db.Column(db.Float)
    inicio_renta = db.Column(db.Date)
    fin_renta = db.Column(db.Date)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
class Propietario(db.Model):
    __tablename__ = 'propietarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    id_predio = db.Column(db.Integer, db.ForeignKey('predios.id'), nullable=True, index=True)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
class Ciclo(db.Model):
    __tablename__='ciclos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(1), unique=True, nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)

class Estado(db.Model):
    __tablename__='estados'
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(3), unique=True, nullable=False)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
class Municipio(db.Model):
    __tablename__='municipios'
    id = db.Column(db.Integer, primary_key=True)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=True, index=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    creado_en = db.Column(db.DateTime(timezone=False),default=func.now())
    creado_por = db.Column(db.Integer)
    escrito_en = db.Column(db.DateTime(timezone=False), onupdate=func.now())
    escrito_por = db.Column(db.Integer)
    
@event.listens_for(Estado.__table__,'after_create')
def create_estados(*args, **kwargs):
    f = open(os.path.join(sys.path[0] + '/operations/addons/json-estados-municipios-mexico','estados.json'))
    estados = json.load(f)
    for estado in estados:
        estadoObj = Estado(clave=estado.get('clave'),nombre=estado.get('nombre'))
        db.add(estadoObj)
    db.commit()
    

@event.listens_for(Municipio.__table__,'after_create')
def create_municipios(*args, **kwargs):
    estados_obj = Estado.query.all()
    municipios = open(os.path.join(sys.path[0] + '/operations/addons/json-estados-municipios-mexico','estados-municipios.json'))
    municipios_data = json.load(municipios)
    for estado in estados_obj:
        index = list(municipios_data).index(str(estado.nombre).title())
        mun = list(municipios_data.values())[index]
        for m in mun:
            municipioObj = Municipio(id_estado=estado.id,nombre=m)
            db.session.add(municipioObj)
    db.session.commit()
    
@event.listens_for(Ciclo.__table__,'after_create')
def create_ciclos(*args, **kwargs):
    ciclos = ['0','1','2','3','4','5','6']
    for ciclo in ciclos:
        cicloObj = Ciclo(nombre=ciclo)
        db.session.add(cicloObj)
    db.session.commit()
    