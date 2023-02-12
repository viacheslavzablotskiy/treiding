from django.apps import AppConfig


class DockerAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'docker_admin'

    # def ready(self):
    #     from django.db.models.signals import post_save
    #
    #     from docker_admin.matrix import create_offer_, register_account
    #     from docker_admin.models import User
    #     post_save.connect(create_offer_, sender=User)
    #     post_save.connect(register_account, sender=User)
