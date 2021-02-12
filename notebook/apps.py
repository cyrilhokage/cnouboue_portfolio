from django.apps import AppConfig


class NotebookappConfig(AppConfig):
    name = 'notebook'

    def ready(self):
        from . import signals