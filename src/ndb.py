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

class Autor(ndb.Model):
  login = ndb.StringProperty()
  user_id = ndb.IntegerProperty()
  html_url = ndb.StringProperty()
  followers = ndb.IntegerProperty()
  following = ndb.IntegerProperty()

class Componente(ndb.Model):
  full_name = ndb.StringProperty() # Format: ":author/:repo"
  repo_id = ndb.IntegerProperty() # Id of the repo in Github
  name_repo = ndb.StringProperty()
  # ComponentID for the repo. It's the id for the repo managed by polymer_bricks
  full_name_id = ndb.StringProperty() # Format: ":author_:repo"
  autor = ndb.StructuredProperty(Autor)
  html_url = ndb.StringProperty()
  description = ndb.StringProperty()
  stars = ndb.IntegerProperty()
  forks = ndb.IntegerProperty()
  languages = ndb.StringProperty(repeated=True)
  #tags = ndb.StructuredProperty(Tag, repeated=True)
  #releases = ndb.StructuredProperty(Release, repeated=True)  
  # Reputation related fields
  reputation = ndb.FloatProperty()
  ratingsCount = ndb.IntegerProperty()
  reputation_sum = ndb.FloatProperty()
  # SHA-256 string that identifies the repo 
  #repo_hash = ndb.StringProperty()
  # Lowercased names in order to obtain a properly ordering in ndb queries
  #name_repo_lower_case = ndb.StringProperty()
  #full_name_repo_lower_case = ndb.StringProperty()

  #Returns the rounded value corresponding to the reputation of the repo
  def roundReputation(self):
    repValue = float(self.reputation)
    roundRep = round(repValue, 2)
    decRep = roundRep - int(roundRep)
    if decRep < 0.26:
      roundRep = roundRep - decRep
    elif decRep >= 0.26 and decRep<= 0.76:
      roundRep = int(roundRep) + 0.5
    else:
      roundRep = float(int(roundRep) + 1)
    return roundRep

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

class UserRating(ndb.Model):
  # google_user_id = ndb.StringProperty()
  full_name_id = ndb.StringProperty()
  rating_value = ndb.FloatProperty()


# Entidad Grupo
class Grupo(ndb.Model):
  nombre_grupo = ndb.StringProperty()
  lista_Usuarios = ndb.StringProperty(repeated=True)
  descripcion = ndb.StringProperty()
# Entidad Token
class Token(ndb.Model):
  id_fb = ndb.StringProperty()
  token_fb = ndb.StringProperty()
  id_tw = ndb.StringProperty()
  token_tw = ndb.StringProperty()
  id_sof = ndb.StringProperty()
  token_sof = ndb.StringProperty()
  id_li = ndb.StringProperty()
  token_li = ndb.StringProperty()
  id_ins = ndb.StringProperty()
  token_ins = ndb.StringProperty()
  id_git = ndb.StringProperty()
  token_git = ndb.StringProperty()
  id_google = ndb.StringProperty()
  token_google = ndb.StringProperty()

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
  nombre_usuario = ndb.StringProperty(required=True) # Valor creado por nosotros mismos al detectar un usuario nuevo 
  email = ndb.StringProperty()
  telefono = ndb.IntegerProperty()
  descripcion = ndb.TextProperty()
  lista_Redes = ndb.StringProperty(Grupo, repeated=True)
  lista_Grupos = ndb.StringProperty(UsuarioSocial, repeated=True)
  valoracion = ndb.StructuredProperty(UserRating, repeated=True)
  componentes = ndb.StructuredProperty(Componente, repeated=True)
  token = ndb.StructuredProperty(Token)
  #tarjeta = ndb.StructuredProperty(Tarjeta)



# Definición de métodos para insertar, obtener o actualizar datos de la base de datos

def getToken(self, nombre_usuario, rs):
  user = Usuario.query(Usuario.nombre_usuario == nombre_usuario).get()
  res = ''
  if rs == "facebook":
    res = user.token.token_fb
  elif rs == "twitter":
    res = user.token.token_tw
  elif rs == "stack-overflow":
    res = user.token.token_sof
  elif rs == "linkedin":
    res = user.token.token_li
  elif rs == "instagram":
    res = user.token.token_ins
  elif rs == "github":
    res = user.token.token_git
  elif rs == "google":
    res = user.token.token_google
  else:
    print "La red social solicitada no esta contemplada"
  return res

def getIdRS(self, nombre_usuario, rs):
  user = Usuario.query(Usuario.nombre_usuario=nombre_usuario).get()
  identificador = ''
  if rs == "facebook":
    identificador = user.id_fb
  elif rs == "twitter":
    identificador = user.id_tw
  elif rs == "stack-overflow":
    identificador = user.id_sof
  elif rs == "linkedin":
    identificador = user.id_li
  elif rs == "instagram":
    identificador = user.id_ins
  elif rs == "github":
    identificador = user.id_git
  elif rs == "google":
    identificador = user.id_google
  else:
    print "La red social solicitada no esta contemplada"
  return identificador

 def buscaUsuario(self, nombre_usuario):
  user = Usuario.query(Usuario.nombre_usuario=nombre_usuario).get()
  usuario = {"nombre_usuario": user.nombre_usuario,
              "email": user.email,
              "telefono": user.telefono,
              "descripcion": user.descripcion,
              "grupos": user.lista_Grupos,
              "redes": user.lista_Redes}
  usuario = json.dumps(usuario)
  return usuario

@ndb.transactional
def insertaUsuario(self, nombre_usuario, datos=None):
  if nombre_usuario == None:
    return "Error. El campo nombre usuario es obligatorio"
  else:
    usuario = Usuario(nombre_usuario=nombre_usuario)
  if not datos == None:
    if datos.email:
      usuario.email = datos.email
    if datos.telefono:
      usuario.telefono = datos.telefono
    if datos.descripcion:
      usuario.descripcion = datos.descripcion

  user_key = usuario.put()

  user_aux = user_key.get()
  user_aux.nombre_usuario = user_key
  user_aux.put()

  return user_key

def actualizaUsuario(self, nombre_usuario, datos):
  usuario = Usuario.query(nombre_usuario==nombre_usuario).get()
  if not datos == None:
    if datos.email:
      usuario.email = datos.email
    if datos.telefono:
      usuario.telefono = datos.telefono
    if datos.descripcion:
      usuario.descripcion = datos.descripcion

  usuario.put()

def insertaToken(self, nombre_usuario, rs, token, id_usuario):
  user = Usuario.query(nombre_usuario==nombre_usuario).get()
  if rs == "facebook":
    user.token_fb = token
    user.id_fb = id_usuario
  elif rs == "twitter":
    user.token_tw = token
    user.id_tw = id_usuario
  elif rs == "instagram":
    user.token_ins = token
    user.id_ins = id_usuario
  elif rs == "github":
    user.token_git = token
    user.id_git = id_usuario
  elif rs == "stack-overflow":
    user.token_sof = token
    user.id_sof = id_usuario
  elif rs == "linkedin":
    user.token_li = token
    user.id_li = id_usuario
  elif rs == "google":
    user.token_google = token
    user.id_google = id_usuario

  user.put()

def insertaGrupo(self, nombre_usuario, grupos=None):
  usuario = Usuario.query(nombre_usuario=nombre_usuario).get()
  if not grupos == None:
    for grupo in grupos:
      usuario.lista_Grupos = usuario.lista_Grupos.append(grupo)
  else:
    return "No se especifica ningun grupo que añadir"

def insertaRed(self, nombre_usuario, redes=None):
  usuario = Usuario.query(nombre_usuario==nombre_usuario).get()
  if not redes == None:
    for red in redes:
      usuario.lista_Redes == usuario.lista_Redes.append(red)