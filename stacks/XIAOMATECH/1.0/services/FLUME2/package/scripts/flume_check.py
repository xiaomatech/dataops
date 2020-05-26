from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.format import format
from resource_management.core.resources.system import Execute


class FlumeServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        if params.security_enabled:
            Execute(
                format(
                    "{kinit_path_local} -kt {smoke_user_keytab} {smokeuser_principal}"
                ),
                user=params.smokeuser)

        Execute(
            format('env JAVA_HOME={java_home} {flume_bin} version'),
            user=params.smokeuser,
            logoutput=True,
            tries=3,
            try_sleep=20)


if __name__ == "__main__":
    FlumeServiceCheck().execute()
