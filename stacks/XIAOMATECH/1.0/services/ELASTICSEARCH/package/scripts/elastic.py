from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script
from resource_management.core.logger import Logger
from resource_management.libraries.functions.check_process_status import check_process_status

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate
from resource_management.core.source import StaticFile
from resource_management.libraries.functions.default import default

download_url_base = default("/configurations/cluster-env/download_url_base",
                            'http://assets.example.com/')


def elastic():
    import params

    directories = [params.log_dir, params.pid_dir, params.conf_dir]

    Directory(
        params.mounts,
        create_parents=True,
        mode=0755,
        owner=params.elastic_user,
        group=params.elastic_group)

    Directory(
        directories,
        create_parents=True,
        mode=0755,
        owner=params.elastic_user,
        group=params.elastic_group)

    File(
        "{0}/elastic-env.sh".format(params.conf_dir),
        owner=params.elastic_user,
        group=params.elastic_group,
        content=InlineTemplate(params.elastic_env_sh_template))

    File(
        format(params.conf_dir + "/elasticsearch.yml"),
        content=InlineTemplate(params.master_content),
        mode=0755,
        owner=params.elastic_user,
        group=params.elastic_group)

    File(
        format(params.conf_dir + "/jvm.options"),
        content=InlineTemplate(params.jvm_content),
        mode=0755,
        owner=params.elastic_user,
        group=params.elastic_group)

    File(
        "/etc/sysconfig/elasticsearch",
        owner=params.elastic_user,
        group=params.elastic_group,
        mode=0777,
        content=InlineTemplate(params.sysconfig_template))


class Elasticsearch(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        Execute('echo "* soft nproc 8192" > /etc/security/limits.d/es.conf')
        Execute(
            'mkdir -p /etc/sysctl.d && echo "vm.max_map_count=655360" > /etc/sysctl.d/11-es.conf '
        )
        Execute(
            "/usr/share/elasticsearch/bin/elasticsearch-plugin install --batch "
            + download_url_base + "/es/repository-hdfs.zip")
        Execute(
            "/usr/share/elasticsearch/bin/elasticsearch-plugin install --batch "
            + download_url_base + "/es/analysis-smartcn.zip")
        params.HdfsResource(
            params.hdfs_backup_dir,
            type="directory",
            action="create_on_execute",
            owner='elasticsearch',
            mode=0755)
        params.HdfsResource(None, action="execute")

    def configure(self, env):
        import params
        env.set_params(params)
        elastic()

    def stop(self, env):
        import params
        env.set_params(params)
        stop_cmd = "source " + params.conf_dir + "/elastic-env.sh; service elasticsearch stop"
        Execute(stop_cmd)

    def start(self, env):
        import params
        env.set_params(params)

        self.configure(env)
        start_cmd = "source " + params.conf_dir + "/elastic-env.sh;service elasticsearch start"
        Execute(start_cmd)

    def status(self, env):
        import params
        env.set_params(params)
        check_process_status(params.elastic_pid_file)

    def restart(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        restart_cmd = "source " + params.conf_dir + "/elastic-env.sh;service elasticsearch restart"
        Execute(restart_cmd)

    def init(self, env):
        import params
        env.set_params(params)
        Execute(
            "curl -XPUT 'http://" + params.hostname +
            ":9200/_template/index_template' -H 'Content-Type: application/json' -d '"
            + params.index_template_content + "'")
        Execute(
            "curl -XPUT 'http://" + params.hostname +
            ":9200/_ilm/policy/hot-warm-cold-delete-60days' -H 'Content-Type: application/json' -d '"
            + params.policy_content + "'")

        File('/tmp/license.json', mode=0755, content=StaticFile('license.json'))

        Execute(
            "curl -XPUT -u admin:admin -H 'Content-Type: application/json' 'http://"
            + params.hostname +
            ":9200/_xpack/license?acknowledge=true' -d @/tmp/license.json")

        Execute(
            "curl -XPUT 'http://" + params.hostname +
            ":9200/_snapshot/hdfs_backup' -H 'Content-Type: application/json' -d '"
            + InlineTemplate(params.hdfs_backup_content) + "'")


if __name__ == "__main__":
    Elasticsearch().execute()
