from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from project_manager.models import Project

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Initialise la création d'utilisateurs de test"

    def handle(self, *args, **options):
        confirmation = input("Voulez-vous vraiment exécuter la commande devel_init ? (Y/N): ")

        if confirmation.lower() != 'y' and 'Y':
            self.stdout.write(self.style.SUCCESS("Annulation de la commande devel_init."))
            return
        UserModel.objects.all().delete()

        admin = UserModel.objects.create_superuser('super_jojo',
                                                   'super_jojo@aa.devel',
                                                   'super_jojo',
                                                   age='36',
                                                   can_be_contacted=True,
                                                   can_data_be_shared=True)
        user1 = UserModel.objects.create_user('toto',
                                              'toto@aa.devel',
                                              'toto',
                                              age='15',
                                              can_be_contacted=False,
                                              can_data_be_shared=False)
        user2 = UserModel.objects.create_user('jojo',
                                              'jojo@aa.devel',
                                              'jojo',
                                              age='25',
                                              can_be_contacted=True,
                                              can_data_be_shared=False)

        test_project = Project.objects.create(
            title='Mon projet de test',
            description='Description de mon projet de test par l/utilisateur super_jojo',
            type='back-end',
            author=admin
        )
        test_project.contributors.add(admin, user1, user2)
        self.stdout.write(self.style.SUCCESS("La commande devel_init a été exécutée avec succès."))
