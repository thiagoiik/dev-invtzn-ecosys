class TelemetryRouter:
    """
    A router to control all database operations on models in the
    telemetry application.
    """
    route_app_labels = {'telemetry'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'telemetry_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'telemetry_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Permitir relaciones si ambos están en telemetry_db,
        # o si uno está en telemetry_db y otro en default (ej. DeploymentMetric -> Deployment).
        # Aunque las relaciones ForeignKey entre diferentes DBs a nivel de base de datos no se soportan en Postgres (foreign keys cruzadas),
        # Django permite manejarlas lógicamente si se define on_delete=DO_NOTHING o similar, pero dado que usamos CASCADE,
        # puede causar problemas a nivel de DB si Django intenta crear el constraint.
        # Por seguridad y funcionalidad, permitimos la relación a nivel de router.
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'telemetry_db'
        
        # Para las demás apps, no migrar a telemetry_db
        if db == 'telemetry_db':
            return False
            
        return None
