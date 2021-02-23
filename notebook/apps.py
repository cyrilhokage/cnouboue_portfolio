from django.apps import AppConfig


class NotebookConfig(AppConfig):
    name = "notebook"

    def ready(self):
        import notebook.signals  # noqa
