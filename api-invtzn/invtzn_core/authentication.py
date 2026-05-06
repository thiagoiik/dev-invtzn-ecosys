import jwt
import base64
from django.conf import settings
from rest_framework import authentication, exceptions

class MicroserviceJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # 1. Extraer y limpiar el token
            header_parts = auth_header.split()
            if len(header_parts) != 2 or header_parts[0].lower() != 'bearer':
                return None
            
            token = header_parts[1].strip()

            # 2. FIX DE PADDING: Asegurar que el token tenga longitud múltiplo de 4
            # Esto corrige el error 'Invalid crypto padding' si el token viene mocho
            missing_padding = len(token) % 4
            if missing_padding:
                token += '=' * (4 - missing_padding)

            # Agrega esto justo antes del jwt.decode
            prefix_key = str(settings.SECRET_KEY)[:10]
            print(f"--- COMPARACIÓN DE SEGURIDAD ---")
            print(f"Llave en INVTZN empieza con: {prefix_key}")
            print(f"Token recibido empieza con: {token[:10]}")

            # 3. Intento de decodificación (HS256 como en tu imagen de jwt.io)
            # Forzamos a que la llave sea tratada como string plano (UTF-8)
            payload = jwt.decode(
                token, 
                str(settings.SECRET_KEY), 
                algorithms=['HS256']
            )

            # 4. Extraer el User ID 8
            user_id = payload.get('user_id') or payload.get('id')
            if not user_id:
                raise exceptions.AuthenticationFailed('El token no tiene ID de usuario.')

            # Crear usuario ficticio para DRF
            user = type('RemoteUser', (object,), {'id': user_id, 'is_authenticated': True})()
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expirado.')
        except jwt.DecodeError as e:
            # Imprime en consola para que compares con lo que ves en jwt.io
            print(f"--- DEBUG ERROR ---")
            print(f"Error real: {str(e)}")
            print(f"Longitud del token: {len(token)}")
            print(f"SECRET_KEY en uso: {settings.SECRET_KEY[:5]}...")
            raise exceptions.AuthenticationFailed(f'Error de firma: {str(e)}. Revisa el secreto.')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Error inesperado: {str(e)}')