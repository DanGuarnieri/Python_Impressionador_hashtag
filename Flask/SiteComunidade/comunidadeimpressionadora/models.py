from comunidadeimpressionadora import database, login_manager
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy.orm import validates
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    @validates('email')
    def convert_lower(self, key, valor):
        return valor.strip().lower()

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc))
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    def data_formatada(self, fuso_usuario="America/Sao_Paulo"):
        return self.data_criacao.astimezone(ZoneInfo(fuso_usuario))