from resource_management.libraries.script import Script


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        pass


if __name__ == "__main__":
    ServiceCheck().execute()
