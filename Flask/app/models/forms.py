from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, RadioField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])

#INSERT INTO users (username, password,admin ) VALUES ("lucas", "123", 1)

class CallForm(FlaskForm):
    category = RadioField("category",choices = [("Impressora", "Impressora"), ("Software", "Instalação/Configuração de Software"), ("Otimização", "Otimização/Formatação de PC"), ("Rede", "Acesso à rede (Pastas ou Internet)")] , validators = [DataRequired()])
    category2 = RadioField("category2", choices = [("Papel Preso", "Papel preso"), ("Toner", "Toner baixo"), ("Outros", "Outro (Especifique)")], validators = [DataRequired()])
    category3 = RadioField("category3", choices = [("Atualização SW", "Atualização de Software"), ("Instalação SW", "Instalação de Programas"), ("Outros", "Outro (Especifique)")], validators = [DataRequired()])
    category4 = RadioField("category4", choices = [("Formatação", "Formatação"), ("Lentidão", "Sistema Lento"), ("Outros", "Outro (Especifique)")], validators = [DataRequired()])
    category5 = RadioField("category5", choices = [("Pastas", "Sem acesso as Pastas"), ("Internet", "Sem Internet"), ("Outros", "Outro (Especifique)")], validators = [DataRequired()])
    obs = TextAreaField("obs", validators= [DataRequired()])

class EditForm(FlaskForm):
    options = RadioField("options", choices = [(3, "Concluído"),(2, "Visualizado"),(1, "Não Atendido")], validators = [DataRequired()])
    form_id = IntegerField("id", validators = [DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])
    password2 = PasswordField("password2", validators = [DataRequired()])
    admin = BooleanField("admin", validators = [DataRequired()])
