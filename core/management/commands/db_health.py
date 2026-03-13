"""
Commande de vérification de l'état de santé de la base de données.
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Vérifier l\'état de santé de la base de données'

    def handle(self, *args, **kwargs):
        try:
            db_engine = settings.DATABASES['default']['ENGINE']

            # Vérification de la connexion
            with connection.cursor() as cursor:
                if 'postgresql' in db_engine:
                    cursor.execute("SELECT version()")
                    version = cursor.fetchone()
                    self.stdout.write(self.style.SUCCESS(
                        f'[OK] Base de données connectée : {version[0]}'
                    ))

                    # Tailles des tables
                    cursor.execute("""
                        SELECT 
                            schemaname,
                            tablename,
                            pg_size_pretty(pg_total_relation_size(
                                schemaname || '.' || tablename
                            ))
                        FROM pg_tables 
                        WHERE schemaname = 'public'
                        ORDER BY pg_total_relation_size(
                            schemaname || '.' || tablename
                        ) DESC;
                    """)
                    tables = cursor.fetchall()

                    self.stdout.write('\n[STATS] Tailles des tables :')
                    for schema, table, size in tables:
                        self.stdout.write(f'  {table}: {size}')

                    # Nombre de connexions actives
                    cursor.execute(
                        "SELECT count(*) FROM pg_stat_activity "
                        "WHERE state = 'active';"
                    )
                    active = cursor.fetchone()[0]
                    self.stdout.write(f'\n[CONN] Connexions actives : {active}')

                else:
                    # SQLite
                    cursor.execute("SELECT sqlite_version()")
                    version = cursor.fetchone()
                    self.stdout.write(self.style.SUCCESS(
                        f'[OK] SQLite connectée : version {version[0]}'
                    ))

                    # Liste des tables
                    cursor.execute(
                        "SELECT name FROM sqlite_master "
                        "WHERE type='table' ORDER BY name;"
                    )
                    tables = cursor.fetchall()
                    self.stdout.write(f'\n[STATS] Tables ({len(tables)}) :')
                    for (table,) in tables:
                        cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
                        count = cursor.fetchone()[0]
                        self.stdout.write(f'  {table}: {count} enregistrements')

            # Infos de configuration
            self.stdout.write('\n[CONFIG] Configuration :')
            self.stdout.write(
                f'  Moteur : {db_engine.split(".")[-1]}'
            )
            self.stdout.write(
                f'  Base   : {settings.DATABASES["default"]["NAME"]}'
            )
            self.stdout.write(self.style.SUCCESS(
                '\n[DONE] Vérification de santé terminée avec succès !'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'[ERROR] Échec de la vérification : {str(e)}'
            ))
