#-*- coding: utf8 -*-
import sys, urllib
import test_utils

# Script para hacer pruebas a la API de Componentes y Usuarios de PicBit, en conjunto (funcionalidades de alto nivel)
# (api/componentes y api/usuarios)
# Uso: python api_componentes_usuarios_tester.py [dashboard | dashboard_borrado | dashboard_predeterminados | dashboard_versionado | --help]
# El versionado estático/dinámico se prueba en dashboard_predeterminados
def main():
	components_basepath = "/api/componentes"
	users_basepath = "/api/usuarios"
	session1 = None
	session2 = None
	session_error = "session=session_error"
	user_id1 = "id_usuario_dashboard_1"
	user_id2 = "id_usuario_dashboard_2"

	# Sets the option param
	option = None
	if len(sys.argv) == 2:
		option = sys.argv[1]


	if option in ["dashboard", "dashboard_borrado", "dashboard_predeterminados", "dashboard_versionado"]:
		# We open the connection with the server
		test_utils.openConnection(False) # Realizamos pruebas en local (remote=False)

		# Iniciamos sesión con dos usuarios en el sistema
		token_id_login = "id_component_users_test_token"
		access_token_login = "googleTEST"
		token_id_login2 = "id_component_users_test_token2"
		access_token_login2 = "googleTEST2"
		session1 = test_utils.do_login_or_signup("googleplus", token_id_login, access_token_login, user_id1)
		session2 = test_utils.do_login_or_signup("googleplus", token_id_login2, access_token_login2, user_id2)

		# PRE-TESTs. Añadimos un componente, utilizado en las pruebas
		print "PRETEST 3: Subir un componente al sistema (para asegurarnos de que existe en el sistema)."
		print "Componente no predeterminado, con 2 versiones. Id: linkedin-timeline"
		print "Ignorar el status de salida de este TEST"
		print "Status esperado: 201 "
		versions_list = ["stable", "usability_defects", "accuracy_defects", "latency_defects"]
		params = urllib.urlencode({'url': 'https://github.com/JuanFryS/linkedin-timeline',
	            'component_id': 'linkedin-timeline',
	            'description': 'Web component to obtain the timeline of the social network Linkedin using Polymer',
	            'social_network': 'linkedin',
	            'input_type': 'None',
	            'output_type': 'posts',
	            'versions': versions_list,
	            'predetermined': 'False'
		}, doseq=True)
		test_utils.make_request("PUT", components_basepath, params, 201, None, preTest=True)


		# PRETEST
		print "PRETEST 4: Añadimos credenciales de linkedin al perfil de usuario 2"
		print "Status esperado: 201"
		request_uri = "/api/oauth/linkedin/credenciales"
		params = urllib.urlencode({'token_id': "token_linkedin", 'access_token': "access_token_linkedin"})
		test_utils.make_request("PUT", request_uri, params, 201, session2, preTest=True)

		if option == "dashboard":

			# TESTs relativos a la modificación de info de usuario (añadir un componente al usuario)
			# TEST 1
			print "TEST 1: Modificar info de usuario, caso añadir un componente al dashboard del usuario 1 (El componente no existe en el sistema)"
			print "Status esperado: 304 (El recurso no se modifica)"
			request_uri = users_basepath + "/" + user_id1
			params = urllib.urlencode({'component': 'componenteError'})
			test_utils.make_request("POST", request_uri, params, 304, session1)

			# TEST 2
			print "TEST 2: Modificar info de usuario, caso añadir un componente al dashboard del usuario 1 (Cookie de sesión correcta)"
			print "El usuario no tiene añadidas credenciales de linkedin, por lo que no se le añade el componente"
			print "Status esperado: 304"
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 304, session1)

			# TEST 3
			print "TEST 3: Modificar info de usuario, caso añadir un componente al dashboard del usuario 2 (Cookie de sesión correcta)"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id2
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 200, session2)

			# TESTs relativos a la obtención de componentes de usuario
			# TEST 4
			print "TEST 4: Obtener la lista de componentes del usuario1, proporcionando una cookie de sesion"
			print "(parámetro de filtrado por usuario)"
			print "Status esperado: 204 (El usuario no tiene componentes añadidos a su dashboard)"
			request_uri = components_basepath + "?filter=user"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 204, session1)

			# TEST 5
			print "TEST 5: Obtener la lista de componentes del usuario2, proporcionando una cookie de sesion"
			print "(parámetro de filtrado por usuario)"
			print "Status esperado: 200"
			request_uri = components_basepath + "?filter=user"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session2)

			# TEST 6
			print "TEST 6: Obtener la lista de componentes del usuario 2, proporcionando una cookie de sesion"
			print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista reducido)"
			print "Status esperado: 204 (El usuario no tiene componentes de la red social Twitter)"
			request_uri = components_basepath + "?social_network=twitter&filter=user&list_format=reduced"
			test_utils.make_request("GET", request_uri, params, 204, session1)

			# TEST 7
			print "TEST 7: Obtener la lista de componentes del usuario 2, proporcionando una cookie de sesion"
			print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista reducido)"
			print "En este caso obtenemos los componentes de linkedin del usuario"
			print "Status esperado: 200"
			request_uri = components_basepath + "?social_network=linkedin&filter=user&list_format=reduced"
			test_utils.make_request("GET", request_uri, params, 200, session2)

			# TEST 8
			print "TEST 8: Obtener la lista de componentes, proporcionando una cookie de sesion"
			print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista completo)"
			print "Status esperado: 204"
			request_uri = components_basepath + "?social_network=linkedin&filter=user&list_format=complete"
			test_utils.make_request("GET", request_uri, params, 204, session1)

			# TEST 9
			print "TEST 9: Obtener info de usuario 1"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id1
			test_utils.make_request("GET", request_uri, params, 200, session1)

			# TEST 10
			print "TEST 9: Obtener info de usuario 1, con formato de lista de componentes detallado"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id1 + "?component_info=detailed"
			test_utils.make_request("GET", request_uri, params, 200, session1)

		elif option == 'dashboard_borrado':
			component_rel_uri = "/linkedin-timeline"

			# PRETEST 5
			print "PRETEST 5: Añadimos el componente al dashboard de usuario 2, si no está añadido ya"
			print "Status esperado: 200 (Ignorar status de este caso)"
			request_uri = users_basepath + "/" + user_id2
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 200, session2, preTest=True)

			# PRETEST 6
			print "PRETEST 6: Obtenemos la info de usuario, con objeto de ver los componentes que tiene incluidos en su dashboard"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id2 + "?component_info=detailed"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session2, preTest=True)

			# TESTs relativos al borrado de componentes de usuario
			# Pruebas de casos de error
			# TEST 11
			print "TEST 11: Borrar el componente del usuario, sin cookie"
			print "Status esperado: 401"
			request_uri = components_basepath + component_rel_uri
			test_utils.make_request("DELETE", request_uri, params, 401, None)

			# TEST 12
			print "TEST 12: Borrar el componente del usuario, proporcionando una cookie incorrecta"
			print "Status esperado: 400"
			request_uri = components_basepath + component_rel_uri
			test_utils.make_request("DELETE", request_uri, params, 400, session_error, printHeaders=True)

			# printH 13
			print "TEST 13: Borrar el componente del usuario, a un componente que no existe"
			print "Status esperado: 400"
			request_uri = components_basepath + "/component_error"
			test_utils.make_request("DELETE", request_uri, params, 400, session_error)

			# Casos de éxito
			# TEST 14
			print "TEST 14: Eliminar componente del usuario 2, con cookie de sesión correcta"
			print "Status esperado: 200"
			request_uri = components_basepath + component_rel_uri
			test_utils.make_request("DELETE", request_uri, params, 200, session2)

			# TEST 15
			print "TEST 15: Obtener info de usuario 2"
			print "(No debe aparecer el componente eliminado en la lista de componentes de usuario)"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id2
			test_utils.make_request("GET", request_uri, params, 200, session2)

			# TEST 16
			print "TEST 16: Volver a añadir el componente"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id2
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 200, session2)

			# TEST 17
			print "TEST 17: Eliminar el componente del dashboard del usuario 1"
			print "Status esperado: 200"
			params = urllib.urlencode({})
			request_uri = components_basepath + component_rel_uri + "?scope=user"
			test_utils.make_request("DELETE", request_uri, params, 200, session2)

			# TEST 18
			print "TEST 18: Obtener lista filtrada de componentes (filter=user), proporcionando la cookie de sesión del usuario 1"
			print "(No debe aparecer el componente eliminado)"
			print "Status esperado: 204"
			request_uri = components_basepath + "?filter=user&list_format=complete"
			test_utils.make_request("GET", request_uri, params, 204, session2)

			# TEST 19
			print "TEST 19: Intentar eliminar el componente del dashboard del usuario 1, estando eliminado ya"
			print "Status esperado: 404"
			request_uri = components_basepath + component_rel_uri + "?scope=user"
			test_utils.make_request("DELETE", request_uri, params, 404, session2)

			# TEST 20
			print "TEST 20: Obtener info sobre el componente"
			print "(Para verificar que no se ha eliminado por error el componente general)"
			print "Status esperado: 200"
			request_uri = components_basepath + component_rel_uri
			test_utils.make_request("GET", request_uri, params, 200, session2)


		elif option == 'dashboard_predeterminados':
			user_id3 = "id_usuario3"
			user_id4 = "id_usuario4"
			user_id5 = "id_usuario5"
			session3 = None
			session4 = None
			session5 = None

			# PRETESTs 5 y 6: Añadimos los componentes que se van a añadir de forma predeterminada al dashboard de usuario (Si no están añadidos ya)
			print "PRETEST 5: Subir un componente predeterminado al sistema (insignia-fb-prededeterminada)."
			print "Status esperado: 201 "
			request_uri = "/api/componentes"
			version_list = ['stable', 'usability_defects', 'latency_defects']
			params = urllib.urlencode({'url': 'https://github.com/JuanFryS/insignia-fb-prededeterminada',
		            'component_id': 'insignia-fb-predetermined',
		            'description': 'Web component to show the user profile in Facebook using Polymer',
		            'social_network': 'facebook' ,
		            'input_type': 'None',
		            'output_type': 'post',
		            'versions': version_list,
		            'predetermined': "True"
			}, doseq=True)
			test_utils.make_request("PUT", request_uri, params, 201, None, preTest=True)

			print "PRETEST 6: Subir un componente predeterminado al sistema (fb-timeline)."
			print "Este componente tiene varias versiones definidas"
			print "Status esperado: 201 "
			params = urllib.urlencode({'url': 'https://github.com/JuanFryS/fb-timeline-predetermined',
		            'component_id': 'fb-timeline-predetermined',
		            'description': 'Web component to obtain the timeline of Facebook using Polymer',
		            'social_network': 'facebook' ,
		            'input_type': 'None',
		            'output_type': 'post',
		            'versions': version_list,
		            'predetermined': "True"
			}, doseq=True)
			test_utils.make_request("PUT", request_uri, params, 201, None, preTest=True)

			# PRETEST 7
			print "PRETEST 7: Añadimos un componente cualquiera al sistema (No predeterminado)"
			print "Status esperado: 201 "
			params = urllib.urlencode({'url': 'https://github.com/JuanFryS/fb-messages',
		            'component_id': 'fb-messages',
		            'description': 'Web component to obtain messages from your facebook account',
		            'social_network': 'facebook',
		            'input_type': 'None',
		            'output_type': 'text',
		            'versions': versions_list,
		            'predetermined': "False"
			}, doseq=True)
			test_utils.make_request("PUT", request_uri, params, 201, None, preTest=True)

			# PRETEST 21: Creamos un nuevo usuario en el sistema (Realizando login mediante facebook)
			request_uri = "/api/oauth/facebook/signup"
			print "PRETEST 21: Signup de usuario 3 en el sistema\n Ignorar el status de este caso"
			print "Probaremos que al añadir un nuevo usuario al sistema, se le añadan los componentes predeterminados"
			print "Ignorar el status de salida de este TEST"
			print "Status esperado: 201 "
			token_id_login = "id_user3_test_token"
			access_token_login = "googleTEST"
			params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
			 'user_identifier': user_id3 })
			session3 = test_utils.make_request("POST", request_uri, params, 201, None, True)


			# PRETEST 22: Creamos un nuevo usuario en el sistema (Realizando login mediante facebook)
			print "PRETEST 22: Signup de usuario 4 en el sistema\n Ignorar el status de este caso"
			print "Probaremos que al añadir un nuevo usuario al sistema, se le añadan los componentes predeterminados"
			print "Ignorar el status de salida de este TEST"
			print "Status esperado: 201 "
			token_id_login = "id_user4_test_token"
			access_token_login = "googleTEST"
			params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
			 'user_identifier': user_id4 })
			session4 = test_utils.make_request("POST", request_uri, params, 201, None, True)

			# PRETEST 23: Creamos un nuevo usuario en el sistema (Realizando login mediante googleplus)
			print "PRETEST 23: Signup de usuario 5 en el sistema\n Ignorar el status de este caso"
			print "Probaremos que al añadir un nuevo usuario al sistema, se le añadan los componentes predeterminados"
			print "Ignorar el status de salida de este TEST"
			print "Status esperado: 201 "
			token_id_login = "id_user5_test_token"
			access_token_login = "googleTEST"
			params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
			 'user_identifier': user_id5 })
			session5 = test_utils.make_request("POST", request_uri, params, 201, None, True)

			# TEST 24
			print "TEST 24: Intentamos añadir un componente predeterminado al usuario 3"
			print "Status esperado: 304 (Ya estaba añadido anteriormente)"
			request_uri = users_basepath + "/" + user_id3
			params = urllib.urlencode({'component': 'insignia-fb-prededetermined'})
			test_utils.make_request("POST", request_uri, params, 304, session3)

			# TEST 25: Añadimos un componente cualquiera al usuario
			print "TEST 25: Añadimos un componente cualquiera al usuario 3"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id3
			params = urllib.urlencode({'component': 'fb-messages'})
			test_utils.make_request("POST", request_uri, params, 200, session3, preTest=True)

			# Tests de obtención de componentes de usuario
			params = urllib.urlencode({})
			request_uri = components_basepath + "?filter=user&list_format=complete"

			# TEST 26
			print "TEST 26: Listamos los detalles sobre los componentes de usuario 3."
			print "(Deben aparecer los componentes predeterminados y el añadido)"
			print "Status esperado: 200"
			test_utils.make_request("GET", request_uri, params, 200, session3)

			# TEST 27
			print "TEST 27: Listamos los detalles sobre los componentes de usuario 4."
			print "(Deben aparecer los componentes predeterminados)"
			print "Status esperado: 200"
			test_utils.make_request("GET", request_uri, params, 200, session4)

			# TEST 28
			print "TEST 28: Listamos los detalles sobre los componentes de usuario 5."
			print "(Deben aparecer los componentes predeterminados)"
			print "Status esperado: 200"
			test_utils.make_request("GET", request_uri, params, 200, session5)

			# Cerramos las tres sesiones iniciadas en esta opcion de testeo
			test_utils.do_logout("googleplus", session3)
			test_utils.do_logout("googleplus", session4)
			test_utils.do_logout("googleplus", session5)

		# Opcion para probar el Round-Robin implementado para el versionado de componentes
		elif option == "dashboard_versionado":
			# Declaracion de variables auxiliares
			user_id3 = "id_usuario3"
			user_id4 = "id_usuario4"
			user_id5 = "id_usuario5"
			user_id6 = "id_usuario6"

			session3 = None
			session4 = None
			session5 = None
			session6 = None

			token_id_login3 = "id_component_users_test_token3"
			token_id_login4 = "id_component_users_test_token4"
			token_id_login5 = "id_component_users_test_token5"
			token_id_login6 = "id_component_users_test_token6"

			access_token_login3 = "googleTEST3"
			access_token_login4 = "googleTEST4"
			access_token_login5 = "googleTEST5"
			access_token_login6 = "googleTEST6"

			# Login / Sign-up en el sistema de los usuarios de prueba
			session3 = test_utils.do_login_or_signup("googleplus", token_id_login3, access_token_login3, user_id3)
			session4 = test_utils.do_login_or_signup("googleplus", token_id_login4, access_token_login4, user_id4)
			session5 = test_utils.do_login_or_signup("googleplus", token_id_login5, access_token_login5, user_id5)
			session6 = test_utils.do_login_or_signup("googleplus", token_id_login6, access_token_login6, user_id6)
			print "################### PRUEBAS VERSIONADO ######################"
			print "PRETEST: Añadimos un componente con tres versiones al sistema"
			version_list = ['stable', 'usability_defects', 'latency_defects']
			print "PRETEST 7: Añadimos un componente cualquiera al sistema (No predeterminado)"
			print "Status esperado: 201 "
			request_uri = "/api/componentes"
			params = urllib.urlencode({'url': 'https://github.com/JuanFryS/google-posts',
					'component_id': 'google-posts',
					'description': 'Web component to obtain your google plus timeline',
					'social_network': 'googleplus',
					'input_type': 'None',
					'output_type': 'text',
					'versions': version_list,
					'predetermined': "False"
			}, doseq=True)
			test_utils.make_request("PUT", request_uri, params, 201, None, preTest=True)

			print "TEST 29: Añadimos el componente al usuario 3"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id3
			params = urllib.urlencode({'component': 'google-posts'})
			test_utils.make_request("POST", request_uri, params, 200, session3, preTest=False)

			print "TEST 30: Añadimos el componente al usuario 4"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id4
			params = urllib.urlencode({'component': 'google-posts'})
			test_utils.make_request("POST", request_uri, params, 200, session4, preTest=False)

			print "TEST 31: Añadimos el componente al usuario 5"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id5
			params = urllib.urlencode({'component': 'google-posts'})
			test_utils.make_request("POST", request_uri, params, 200, session5, preTest=False)

			print "TEST 32: Añadimos el componente al usuario 6"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id6
			params = urllib.urlencode({'component': 'google-posts'})
			test_utils.make_request("POST", request_uri, params, 200, session6, preTest=False)

			print "TEST 33: Obtenemos la información sobre el usuario 3"
			print "Status esperado: 200 (Comprobar si se le ha asignado la versión correcta)"
			request_uri = users_basepath + "/" + user_id3 + "?component_info=detailed"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session3, preTest=False)

			print "TEST 34: Obtenemos la información sobre el usuario 4"
			print "Status esperado: 200 (Comprobar si se le ha asignado la versión correcta)"
			request_uri = users_basepath + "/" + user_id4 + "?component_info=detailed"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session4, preTest=False)

			print "TEST 35: Obtenemos la información sobre el usuario 5"
			print "Status esperado: 200 (Comprobar si se le ha asignado la versión correcta)"
			request_uri = users_basepath + "/" + user_id5 + "?component_info=detailed"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session5, preTest=False)

			print "TEST 36: Obtenemos la información sobre el usuario 6"
			print "Status esperado: 200 (Comprobar si se le ha asignado la versión correcta)"
			request_uri = users_basepath + "/" + user_id6 + "?component_info=detailed"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session6, preTest=False)

			# Cerramos las tres sesiones iniciadas en esta opcion de testeo
			test_utils.do_logout("googleplus", session3)
			test_utils.do_logout("googleplus", session4)
			test_utils.do_logout("googleplus", session5)
			test_utils.do_logout("googleplus", session6)

		# Cerramos todas las sesiones iniciadas en los tests
		test_utils.do_logout("googleplus", session1)
		test_utils.do_logout("googleplus", session2)

		# Cerramos conexión e imprimimos el ratio de test ok vs erróneos
		test_utils.closeConnection()
		test_utils.tests_status()

	elif option == "help":
		print "Script para hacer pruebas a la API de Componentes y Usuarios de PicBit, en conjunto (funcionalidades de alto nivel) "
		print "(api/componentes y api/usuarios)"
		print "Uso: python api_componentes_usuarios_tester.py [dashboard | dashboard_borrado | dashboard_predeterminados | dashboard_versionado | help]"
	else:
		print "ERROR: opción incorrecta"
		print "Uso: python api_componentes_usuarios_tester.py [dashboard | dashboard_borrado | dashboard_predeterminados | dashboard_versionado | help]"

if __name__ == "__main__":
	main()
