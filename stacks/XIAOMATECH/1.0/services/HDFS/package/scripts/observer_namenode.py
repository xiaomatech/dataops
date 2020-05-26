from resource_management.libraries.script.script import Script

from hdfs import hdfs, install_hadoop

from resource_management.core.logger import Logger
from utils import service
from resource_management.core.resources.system import Directory, File
from resource_management.core.source import Template
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.generate_logfeeder_input_config import generate_logfeeder_input_config


def observer_namenode(action=None, format=False):
    if action == "configure":
        import params
        for fs_checkpoint_dir in params.fs_checkpoint_dirs:
            Directory(
                fs_checkpoint_dir,
                create_parents=True,
                cd_access="a",
                mode=0755,
                owner=params.hdfs_user,
                group=params.user_group)
        File(
            params.exclude_file_path,
            content=Template("exclude_hosts_list.j2"),
            owner=params.hdfs_user,
            group=params.user_group)
        if params.hdfs_include_file:
            File(
                params.include_file_path,
                content=Template("include_hosts_list.j2"),
                owner=params.hdfs_user,
                group=params.user_group)
        generate_logfeeder_input_config(
            'hdfs',
            Template("input.config-hdfs.json.j2", extra_imports=[default]))
    elif action == "start" or action == "stop":
        import params
        service(
            action=action,
            name="observernamenode",
            user=params.hdfs_user,
            create_pid_dir=True,
            create_log_dir=True)
    elif action == "status":
        import status_params
        check_process_status(status_params.snamenode_pid_file)


class ObserverNameNode(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_hadoop()

    def configure(self, env):
        import params
        env.set_params(params)
        hdfs("observernamenode")
        observer_namenode(action="configure")

    def save_configs(self, env):
        import params
        env.set_params(params)
        hdfs("observernamenode")

    def reload_configs(self, env):
        import params
        env.set_params(params)
        Logger.info("RELOAD CONFIGS")

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        install_hadoop()
        observer_namenode(action="start")

    def stop(self, env):
        import params
        env.set_params(params)
        observer_namenode(action="stop")

    def status(self, env):
        import status_params
        env.set_params(status_params)
        observer_namenode(action="status")

    def get_log_folder(self):
        import params
        return params.hdfs_log_dir

    def get_user(self):
        import params
        return params.hdfs_user

    def get_pid_files(self):
        import status_params
        return [status_params.observer_namenode_pid_file]


if __name__ == "__main__":
    ObserverNameNode().execute()
