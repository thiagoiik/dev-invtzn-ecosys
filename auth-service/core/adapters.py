from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):

    # 1. Adaptador para Confirmación de Registro
    def get_email_confirmation_url(self, request, emailconfirmation):
        # Aquí se construye la URL que apunta a  VUE APP.
        # Cambia 'http://localhost:5173' por el dominio real del frontend.
        frontend_url = "http://front.auth.local/verify-email" 
        return f"{frontend_url}/{emailconfirmation.key}/"


    # 2. NUEVO: La trampa para la recuperación de contraseña
    def send_mail(self, template_prefix, email, context):
        # Si allauth está a punto de enviar el correo de contraseña...
        if template_prefix == 'account/email/password_reset_key':
            # Sacamos la URL que allauth generó hacia el backend
            url_backend = context['password_reset_url']
            # La reemplazamos a la fuerza por la de Vue
            url_frontend = url_backend.replace('api.auth.local', 'front.auth.local')
            # La guardamos de vuelta en el correo
            context['password_reset_url'] = url_frontend

        # Dejamos que allauth envíe el correo modificado
        super().send_mail(template_prefix, email, context)