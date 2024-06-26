from options import options


class Package:
    def __init__(self, code, label="", delivered=False):
        self.code = code
        self.label = label
        self.status = None
        self.delivered = delivered if delivered else False

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return f"{self.code} - {self.label}"


class PackageManager:
    def __init__(self):
        self.package_list_file = "mailman_packages.csv"
        self.basedir = "."  # '~/.config/mailman'
        self.package_list = self.load_package_list()
        self.list_changed = False

    def package_list_file_path(self) -> str:
        return f"{self.basedir}/{self.package_list_file}"

    def add_package(self, code: str, label="") -> None:
        if not self.is_valid(code):
            raise ValueError(f"Invalid Tracking code [{code}].")

        self.package_list.append(Package(code, label))
        self.list_changed = True

    def remove_package(self, code: str) -> None:
        index = next(
            (i for i, p in enumerate(self.package_list) if p.code == code), None
        )
        if index is None:
            return

        self.package_list.pop(index)
        self.list_changed = True

    def remove_delivered(self, statuses: list) -> None:
        if "entregue" in statuses and len(statuses["entregue"]):
            for code in statuses["entregue"]:
                self.remove_package(code["cod_objeto"].replace(" ", ""))
            self.list_changed = True

    def mark_delivered(self, statuses: list) -> None:
        if "entregue" in statuses and len(statuses["entregue"]):
            for code in statuses["entregue"]:
                package = next(
                    (
                        p
                        for p in self.package_list
                        if p.code == code["cod_objeto"].replace(" ", "")
                    ),
                    None,
                )
                if package is not None:
                    package.delivered = True
                    self.list_changed = True

    def save(self) -> None:
        if not self.list_changed:
            return

        with open(self.package_list_file_path(), "w") as file:
            file.write(
                "\n".join(
                    [
                        f"{package.code},{package.label},{package.delivered}"
                        for package in self.package_list
                    ]
                )
            )

    def load_package_list(self) -> list:
        try:
            with open(self.package_list_file_path(), "r") as file:
                packages = file.read().splitlines()
                return [
                    Package(code, label, delivered)
                    for code, label, delivered in [p.split(",") for p in packages]
                ]
        except FileNotFoundError:
            return []

    def drop_package_list(self) -> None:
        self.package_list = []
        self.list_changed = True

    def show_packages(self, show_delivered=False) -> None:
        package_list = [p for p in self.package_list if p.delivered == "False"]
        if show_delivered:
            package_list = self.package_list

        if len(package_list) > 0:
            print("These are the packages being tracked:")
            print(
                "  +",
                "\n  + ".join(
                    [
                        f"{package.code} - {package.label} {' [Entregue]' if package.delivered == 'True' else ''}"
                        for package in package_list
                    ]
                ),
            )
        else:
            print("No packages being tracked.")

    def is_valid(self, code: str) -> bool:
        return code is not None and len(code) == 13

    def assign_statuses(self, statuses: list) -> None:
        # Use cod_objeto here because cod_objeto_ is not always present
        for status in statuses["entregue"]:
            package = next(
                (
                    p
                    for p in self.package_list
                    if p.code == status["cod_objeto"].replace(" ", "")
                ),
                None,
            )
            if package is not None:
                status["status"] = "entregue"
                package.set_status(status)

        for status in statuses["transito"]:
            package = next(
                (
                    p
                    for p in self.package_list
                    if p.code == status["cod_objeto"].replace(" ", "")
                ),
                None,
            )
            if package is not None:
                status["status"] = "transito"
                package.set_status(status)

    def show_package_statuses(self) -> None:
        in_traffic = list(
            filter(
                lambda p: p.status and p.status["status"] == "transito",
                self.package_list,
            )
        )
        delivered = list(
            filter(
                lambda p: p.status and p.status["status"] == "entregue",
                self.package_list,
            )
        )
        print("\n")
        if len(in_traffic) > 0:
            print("============ Em Transito ============")
            for package in in_traffic:
                self.show_single_package_status(package)
            print("\n")

        if len(delivered) > 0 and options.show_delivered:
            print("============ Já Entregue ============")
            for package in delivered:
                self.show_single_package_status(package)
            print("\n")

    def show_event(self, event) -> None:
        city = event["unidade"]["endereco"]["cidade"]
        state = event["unidade"]["endereco"]["uf"]
        date = event["dtHrCriado"]["date"][0:16]
        destination_city = None
        destination_state = None
        event_type = event["unidade"]["tipo"]
        if event["unidadeDestino"]:
            destination_city = event["unidadeDestino"]["endereco"]["cidade"]
            destination_state = event["unidadeDestino"]["endereco"]["uf"]

        if destination_city == city and destination_state == state:
            event_type = ""
        elif destination_city and destination_state:
            event_type = f"-> {destination_city}/{destination_state}"

        print(f"  {date}")
        print(f"    {event['descricao']}: {city}/{state} {event_type}")
        print("  --------------------")

    def show_event_short(self, event: dict) -> None:
        city = event["unidade"]["endereco"]["cidade"]
        state = event["unidade"]["endereco"]["uf"]
        date = event["dtHrCriado"]["date"][0:16]
        destination_city = None
        destination_state = None
        locale_change = f"{event['descricao']} - {state}"

        if event["unidadeDestino"]:
            destination_city = event["unidadeDestino"]["endereco"]["cidade"]
            destination_state = event["unidadeDestino"]["endereco"]["uf"]

        if destination_state and destination_state != state:
            locale_change = f"{state} -> {destination_state}"

        elif destination_city and destination_city != city:
            locale_change = f"{city} -> {destination_city}"

        elif destination_city and destination_state:
            locale_change = f"{event['descricao']} - {city}"

        print(f"  > {date} - {locale_change} ")

    def show_single_package_status(self, package: Package) -> None:
        if not "objeto" in package.status:
            print(f">>>> {package.label} {package.code}")
            print(f"        - {package.status['mensagem_h']}")
            print("")
            return

        status = package.status["objeto"]
        print(f">>>> {package.label} {package.code}")
        print(f"  - Previsão: {status['dtPrevista']}")
        print(f"  - Tipo: {status['tipoPostal']['categoria']}")
        self.show_event(status["eventos"][0])
        if options.detailed:
            for event in status["eventos"][1:]:
                self.show_event_short(event)
            print("")
