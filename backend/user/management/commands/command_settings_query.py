from django.core.management.base import BaseCommand
from backend.const import CURRENCY, PAGINATION
from ...models import CommandPagination, CommandCurrency


class Command(BaseCommand):
    help = """
    Command that uploads constants that are needed for user settings
    """

    def handle(self, *args, **options):
        for currency_dict in CURRENCY:
            currency = currency_dict.get('currency')
            if not CommandCurrency.objects.filter(
                    pk=currency_dict.get('pk'),
                    currency=currency_dict.get('currency')
            ):
                currency_model = CommandCurrency(**currency_dict)
                currency_model.save()
                self.stdout.write(f'Currency "{currency}" added or changed.')
            else:
                self.stdout.write(f'Currency "{currency}" already exist.')

        for pagination_dict in PAGINATION:
            paginate_by = pagination_dict.get('paginate_by')
            if not CommandPagination.objects.filter(
                    pk=pagination_dict.get('pk'),
                    paginate_by=pagination_dict.get('paginate_by')
            ):
                paginate_by_model = CommandPagination(**pagination_dict)
                paginate_by_model.save()
                self.stdout.write(f'Pagination "{paginate_by}" added or changed.')
            else:
                self.stdout.write(f'Pagination "{paginate_by}" already exist.')

        return self.stdout.write(f'Command completed!')
