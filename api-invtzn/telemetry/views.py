from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .tasks import save_rrweb_session_task
import json

class RecordSessionView(APIView):
    # Permitir que los invitados sin cuenta o los testers autenticados envíen datos,
    # dependiendo de tus reglas. Para testers, usaremos IsAuthenticated.
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # Validar el payload
        events_payload = request.data.get('events')
        if not events_payload:
            return Response({"error": "No se enviaron eventos (events) en el payload."}, status=status.HTTP_400_BAD_REQUEST)
        
        window_width = request.data.get('window_width')
        window_height = request.data.get('window_height')
        
        # Obtener el user_agent desde los headers
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Obtener entorno desde variable
        import os
        environment = os.environ.get('VITE_APP_ENV', 'sandbox')
        
        # (Opcional) Validar que el rol sea TESTER u otro antes de aceptar
        # role = request.data.get('role') o usar el role asociado al usuario autenticado

        # Enviar tarea a Celery para procesamiento asíncrono
        save_rrweb_session_task.delay(
            user_id=user.id if user else None,
            role='TESTER', # Aquí idealmente se inyectaría el rol del usuario si está disponible
            environment=environment,
            user_agent=user_agent,
            window_width=window_width,
            window_height=window_height,
            events_payload=events_payload
        )
        
        return Response({"status": "Grabación de sesión encolada con éxito."}, status=status.HTTP_202_ACCEPTED)
