from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Directory, Execute, File, Link
import os
from resource_management.core.source import StaticFile, Template, InlineTemplate
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status


def install_alluxio():
    import params
    Directory([
        params.log_dir, params.hdd_dirs, params.journal_dir,
        params.underfs_addr, params.pid_dir
    ],
              owner=params.alluxio_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.alluxio_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('rm -rf %s' % params.install_dir + '/conf')
        Execute('ln -s ' + params.conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute('chown -R %s:%s %s/%s' % (params.alluxio_user, params.user_group, Script.get_stack_root(),params.version_dir))
        Execute('chown -R %s:%s %s' % (params.alluxio_user, params.user_group,
                                       params.install_dir))


def config_alluxio():
    import params
    # alluxio-env.sh
    File(
        params.conf_dir + "/alluxio-env.sh",
        owner=params.alluxio_user,
        group=params.user_group,
        mode=0755,
        content=InlineTemplate(params.alluxio_site_content))

    # alluxio-site.properties
    File(
        params.conf_dir + "/alluxio-site.properties",
        owner=params.alluxio_user,
        group=params.user_group,
        mode=0755,
        content=InlineTemplate(params.alluxio_site_content))

    # masters
    File(
        params.conf_dir + "/masters",
        owner=params.alluxio_user,
        group=params.user_group,
        mode=0755,
        content=Template('masters.j2', conf_dir=params.conf_dir))
    # workers
    File(
        params.conf_dir + "/workers",
        owner=params.alluxio_user,
        group=params.user_group,
        mode=0755,
        content=Template('workers.j2', conf_dir=params.conf_dir))


class Master(Script):
    def install(self, env):
        import params
        self.install_packages(env)
        env.set_params(params)

    def configure(self, env):
        import params
        env.set_params(params)
        config_alluxio()

    def start(self, env):
        import params
        env.set_params(params)
        install_alluxio()
        self.configure(env)

        Execute(params.start_script + ' master')

        cmd = "echo `ps -A -o pid,command | grep -i \"[j]ava\" | grep AlluxioMaster | awk '{print $1}'`> " + params.pid_dir + "/AlluxioMaster.pid"
        Execute(cmd)

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(params.stop_script + ' master')

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.pid_dir + "/AlluxioMaster.pid")


if __name__ == "__main__":
    Master().execute()
