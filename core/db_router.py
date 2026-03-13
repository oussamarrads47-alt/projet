"""
Database router pour TRANS-GEST.
Permet la configuration multi-bases de données si nécessaire.
"""


class TransgestRouter:
    """
    Router de base de données pour l'application TRANS-GEST.
    Route toutes les opérations de l'app 'core' vers la base par défaut.
    """

    app_label = 'core'

    def db_for_read(self, model, **hints):
        """Dirige les lectures vers la base par défaut."""
        if model._meta.app_label == self.app_label:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """Dirige les écritures vers la base par défaut."""
        if model._meta.app_label == self.app_label:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Autorise les relations entre objets de l'app core."""
        if (
            obj1._meta.app_label == self.app_label
            or obj2._meta.app_label == self.app_label
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Autorise les migrations pour l'app core sur la base par défaut."""
        if app_label == self.app_label:
            return db == 'default'
        return None
