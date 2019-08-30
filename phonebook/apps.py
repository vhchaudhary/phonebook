from django.apps import AppConfig


class PhonebookConfig(AppConfig):
    name = 'phonebook'

    def ready(self):
        import phonebook.signals
