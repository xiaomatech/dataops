from resource_management.libraries.script import Script


class BeaconServiceCheck(Script):
    def service_check(self, env):
        pass


if __name__ == "__main__":
    BeaconServiceCheck().execute()
