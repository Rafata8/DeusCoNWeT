""" Copyright 2014 Luis Ruiz Ruiz
	  Copyright 2014 Ana Isabel Lopera Martinez
	  Copyright 2014 Miguel Ortega Moreno
    Copyright 2014 Juan Francisco Salamanca Carmona

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from google.appengine.ext import ndb
import json
import webapp2
"""NDB Instances """
# class Tag(ndb.Model):
#   name_tag = ndb.StringProperty()
#   date_tag = ndb.StringProperty()
#   author = ndb.StringProperty()
#   zipball_url = ndb.StringProperty()
#   tarball_url = ndb.StringProperty()

# class Release(ndb.Model):
#   tag_name = ndb.StringProperty()
#   html_url = ndb.StringProperty()
#   name_release = ndb.StringProperty()
#   description = ndb.TextProperty()
#   publish_date = ndb.StringProperty()
#   zipball_url = ndb.StringProperty()
#   tarball_url = ndb.StringProperty()

# class Autor(ndb.Model):
#   login = ndb.StringProperty()
#   user_id = ndb.IntegerProperty()
#   html_url = ndb.StringProperty()
#   followers = ndb.IntegerProperty()
#   following = ndb.IntegerProperty()

# class Componente(ndb.Model):
#   full_name = ndb.StringProperty() # Format: ":author/:repo"
#   repo_id = ndb.IntegerProperty() # Id of the repo in Github
#   name_repo = ndb.StringProperty()
#   # ComponentID for the repo. It's the id for the repo managed by polymer_bricks
#   full_name_id = ndb.StringProperty() # Format: ":author_:repo"
#   autor = ndb.StructuredProperty(Autor)
#   html_url = ndb.StringProperty()
#   description = ndb.StringProperty()
#   stars = ndb.IntegerProperty()
#   forks = ndb.IntegerProperty()
#   languages = ndb.StringProperty(repeated=True)
#   #tags = ndb.StructuredProperty(Tag, repeated=True)
#   #releases = ndb.StructuredProperty(Release, repeated=True)  
#   # Reputation related fields
#   reputation = ndb.FloatProperty()
#   ratingsCount = ndb.IntegerProperty()
#   reputation_sum = ndb.FloatProperty()
#   # SHA-256 string that identifies the repo 
#   #repo_hash = ndb.StringProperty()
#   # Lowercased names in order to obtain a properly ordering in ndb queries
#   #name_repo_lower_case = ndb.StringProperty()
#   #full_name_repo_lower_case = ndb.StringProperty()

  #Returns the rounded value corresponding to the reputation of the repo
  # def roundReputation(self):
  #   repValue = float(self.reputation)
  #   roundRep = round(repValue, 2)
  #   decRep = roundRep - int(roundRep)
  #   if decRep < 0.26:
  #     roundRep = roundRep - decRep
  #   elif decRep >= 0.26 and decRep<= 0.76:
  #     roundRep = int(roundRep) + 0.5
  #   else:
  #     roundRep = float(int(roundRep) + 1)
  #   return roundRep

  # """Methods to generate RPC Messages returned by Polymer Bricks API"""
  # # type: basic/detailed
  # def toRPCMessage(self, type):
  #   if type=="basic":
  #     # We set the user rating to 0, then we will set the proper value (in getUserRating)
  #     return ComponentBasicInfo(name=self.name_repo, author=self.owner.login
  #               ,description=self.description, nStars=self.stars,
  #               starRate=self.roundReputation(), nForks=self.forks, userRating = 0.0, 
  #               componentId=self.full_name_id)
  #   elif type=="detailed":
  #     # We set the user rating to 0, then we will set the proper value (in getUserRating)
  #     return ComponentDetails(name=self.name_repo, author=self.owner.login
  #               ,description=self.description, nStars=self.stars,
  #               starRate=self.roundReputation(), nForks=self.forks, userRating = 0.0,
  #               componentId=self.full_name_id)

class Componente(ndb.Model):
  nombre = ndb.StringProperty(required=True)
  x = ndb.FloatProperty()
  y = ndb.FloatProperty()
  url = ndb.StringProperty()
  height = ndb.StringProperty()
  width = ndb.StringProperty()

class UserRating(ndb.Model):
  # google_user_id = ndb.StringProperty()
  full_name_id = ndb.StringProperty()
  rating_value = ndb.FloatProperty()


# Entidad Grupo
class Grupo(ndb.Model):
  nombre_grupo = ndb.StringProperty()
  lista_Usuarios = ndb.StringProperty()
  descripcion = ndb.StringProperty()
# Entidad Token
class Token(ndb.Model):
  identificador = ndb.StringProperty()
  token = ndb.StringProperty()
  nombre_rs = ndb.StringProperty()

# Entidad UsuarioSocial
class UsuarioSocial(ndb.Model):
  nombre_rs = ndb.StringProperty()
  siguiendo = ndb.IntegerProperty()
  seguidores = ndb.IntegerProperty()
  url_sig = ndb.StringProperty()
  url_seg = ndb.StringProperty()
  # Faltan las uris del resto de apis a consultar

# #Entidad Tarjeta
# class Tarjeta(ndb.Model):
#   id_tw = ndb.StringProperty()
#   id_fb = ndb.StringProperty()
#   id_sof = ndb.StringProperty()
#   id_li = ndb.StringProperty()
#   id_ins = ndb.StringProperty()
#   id_git = ndb.StringProperty()
#   id_google = ndb.StringProperty()

# Entidad usuario
class Usuario(ndb.Model):
  email = ndb.StringProperty()
  telefono = ndb.IntegerProperty()
  descripcion = ndb.TextProperty()
  imagen = ndb.StringProperty()
  tokens = ndb.StructuredProperty(Token, repeated=True)
  lista_Redes = ndb.StructuredProperty(Grupo, repeated=True)
  lista_Grupos = ndb.StructuredProperty(UsuarioSocial, repeated=True)
  valoracion = ndb.StructuredProperty(UserRating, repeated=True)
  componentes = ndb.StructuredProperty(Componente, repeated=True)
  #tarjeta = ndb.StructuredProperty(Tarjeta)

#####################################################################################
# Definicion de metodos para insertar, obtener o actualizar datos de la base de datos
#####################################################################################

def getToken(entity_key, rs):
  user = entity_key.get()
  tokens = user.tokens
  res = None
  for token in tokens:
    if token.get('nombre_rs') == rs:
      res = token

  return res

def buscaUsuario(entity_key):
  user = entity_key.get()
  usuario = {"nombre_usuario": user.nombre_usuario,
              "email": user.email,
              "telefono": user.telefono,
              "descripcion": user.descripcion,
              "grupos": user.lista_Grupos,
              "redes": user.lista_Redes}
  usuario = json.dumps(usuario)
  return usuario

@ndb.transactional
def insertaUsuario(rs, ide, token, datos=None):
  usuario = Usuario()
  token = Token(identificador=ide, token=token, nombre_rs=rs)
  usuario.tokens.append(token)
  if not datos == None:
    if datos["email"]:
      usuario.email = datos["email"]
    if datos["telefono"]:
      usuario.telefono = datos["telefono"]
    if datos["descripcion"]:
      usuario.descripcion = datos["descripcion"]
    if datos["imagen"]:
      usuario.imagen = datos["imagen"]

  user_key = usuario.put()

  return user_key

def actualizaUsuario(entity_key, datos):
  usuario = entity_key.get()
  if not datos == None:
    if datos["email"]:
      usuario.email = datos["email"]
    if datos["telefono"]:
      usuario.telefono = datos["telefono"]
    if datos["descripcion"]:
      usuario.descripcion = datos["descripcion"]
    if datos["imagen"]:
      usuario.imagen = datos["imagen"]

  usuario.put()

def insertaToken(entity_key, rs, token, id_usuario):
  user = entity_key.get()
  tok_aux = Token(identificador=id_usuario, token=token, nombre_rs=rs)
  user.tokens.append(tok_aux)
  user.put()

def insertaGrupo(entity_key, grupos=None):
  usuario = entity_key.get()
  if not grupos == None:
    for grupo in grupos:
      usuario.lista_Grupos.append(grupo)
  else:
    return "No se especifica ningun grupo que insertar"

def buscaGrupo(entity_key):
  user = entity_key.get()
  res = {}
  contador = 1
  if user.lista_Grupos:
    for grupo in user.lista_Grupos:
      res[contador] = grupo
      contador += 1

  return json.dumps(res)

def insertaRed(entity_key, redes=None):
  usuario = entity_key.get()
  if not redes == None:
    for red in redes:
      usuario.lista_Redes.append(red)

def buscaRed(entity_key):
  usuario = entity_key.get()
  res = {}
  contador = 1
  if usuario.lista_Redes:
    for red in usuario.lista_Redes:
      res[contador] = red
      contador += 1

  return json.dumps(res)

def insertarComponente(entity_key, nombre, coord_x=0, coord_y=0, url="", height="", width=""):
  usuario = entity_key.get()
  componente = Componente(nombre=nombre, x=coord_x, y=coord_y, url=url, height=height, width=width)
  usuario.componentes.append(componente)

  usuario.put()

def modificarComponente(entity_key, nombre, datos):
  usuario = entity_key.get()
  comp_aux = Componente(nombre=nombre)
  comp = Componente.query(usuario.componentes==comp_aux)
  if datos["x"]:
    comp.x = datos["x"]
  if datos["y"]:
    comp.y = datos["y"]
  if datos["url"]:
    comp.url = datos["url"]
  if datos["height"]:
    comp.height = datos["height"]
  if datos["width"]:
    comp.width = datos["width"]

  usuario.put()

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hago el get')
    datos = ["lruiz@conwet.com", 61472589, "Este es mi perfil personal", "www.example.com/mi-foto.jpg"]
    key = insertaUsuario("twitter", "lrr9204", "asdfghjklm159753", datos)

    tok = getToken(key, "twitter")
    self.response.write(tok)

    tok_err = getToken(key, "ins")
    self.response.write(tok_err)

app = webapp2.WSGIApplication([
      ('/', MainPage),
], debug=True)
