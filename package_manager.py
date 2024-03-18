class PackageManager:
    def __init__(self):
        self.package_list_file = 'mailman_packages.csv'
        self.basedir = '.' # '~/.config/mailman'
        self.package_list = self.load_package_list()
        self.list_changed = False

    def package_list_file_path(self):
        return f"{self.basedir}/{self.package_list_file}"

    def add_package(self, code, label=''):
        if not self.is_valid(code):
            raise ValueError(f'Invalid Tracking code [{code}].')

        self.package_list.append(Package(code, label))
        self.list_changed = True

    def remove_package(self, code):
        index = next((i for i, p in enumerate(self.package_list) if p.code == code), None)
        if index == None:
            return

        self.package_list.pop(index)
        self.list_changed = True

    def remove_delivered(self, statuses):
        if 'entregue' in statuses:
            for code in statuses['entregue']:
                self.remove_package(code['cod_objeto'].replace(" ", ""))
            self.list_changed = True

    def save(self):
        if not self.list_changed:
            return

        with open(self.package_list_file_path(), 'w') as file:
            file.write('\n'.join([f"{code.code},{code.label}" for code in self.package_list]))

    def load_package_list(self):
        try:
            with open(self.package_list_file_path(), 'r') as file:
                codes = file.read().splitlines()
                return [Package(code, label) for code, label in [c.split(',') for c in codes]]
        except FileNotFoundError:
            return []

    def drop_package_list(self):
        self.package_list = []
        self.list_changed = True

    def show_packages(self):
        if len(self.package_list) > 0:
            print('These are the packages being tracked:')
            print("  +", "\n  + ".join([f"{code.code} - {code.label}" for code in self.package_list]))
        else:
            print('No packages being tracked.')

    def is_valid(self, code):
        return code != None and len(code) == 13

    def assign_statuses(self, statuses):
        for status in statuses['entregue']:
            package = next((p for p in self.package_list if p.code == status['cod_objeto_']), None)
            if package != None:
                status['status'] = 'entregue'
                package.set_status(status)

        for status in statuses['transito']:
            package = next((p for p in self.package_list if p.code == status['cod_objeto_']), None)
            if package != None:
                status['status'] = 'transito'
                package.set_status(status)

    def show_package_statuses(self):
        in_traffic = list(filter(lambda p: p.status and p.status['status'] == 'transito', self.package_list))
        delivered = list(filter(lambda p: p.status and p.status['status'] == 'entregue', self.package_list))
        if len(in_traffic) > 0:
            print('=========== Transito ===========')
            for package in in_traffic:
                self.show_single_package_status(package)

        if len(delivered) > 0:
            print('=========== Entregue ===========')
            for package in delivered:
                self.show_single_package_status(package)

    def show_event(self, event):
        city = event['unidade']['endereco']['cidade']
        state = event['unidade']['endereco']['uf']
        date = event['dtHrCriado']['date'][0:16]
        destination_city = None
        destination_state = None
        event_type = event['unidade']['tipo']
        if event['unidadeDestino']:
            destination_city = event['unidadeDestino']['endereco']['cidade']
            destination_state = event['unidadeDestino']['endereco']['uf']

        if destination_city == city and destination_state == state:
            event_type = ''
        elif destination_city and destination_state:
            event_type = f"-> {destination_city}/{destination_state}"

        print(f"  {date}")
        print(f"    {event['descricao']}: {city}/{state} {event_type}")
        print("--------------------")

    def show_event_short(self, event):
        city = event['unidade']['endereco']['cidade']
        state = event['unidade']['endereco']['uf']
        date = event['dtHrCriado']['date'][0:16]
        destination_city = None
        destination_state = None
        locale_change = f"{event['descricao']} - {state}"

        if event['unidadeDestino']:
            destination_city = event['unidadeDestino']['endereco']['cidade']
            destination_state = event['unidadeDestino']['endereco']['uf']

        if destination_state and destination_state != state:
            locale_change = f"{state} -> {destination_state}"

        elif destination_city and destination_city != city:
            locale_change  = f"{city} -> {destination_city}"

        elif destination_city and destination_state:
            locale_change = f"{event['descricao']} - {city}"

        print(f"  {date} - {locale_change} ")

    def show_single_package_status(self, package):
        status = package.status['objeto']
        print(f">>>> {package.label} {status['codObjeto']} -  Previsão: {status['dtPrevista']} - Tipo: {status['tipoPostal']['categoria']}")
        self.show_event(status['eventos'][0])
        for event in status['eventos'][1:]:
            self.show_event_short(event)

class Package:
    def __init__(self, code, label=''):
        self.code = code
        self.label = label
        self.status = None

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return f'{self.code} - {self.label}'
