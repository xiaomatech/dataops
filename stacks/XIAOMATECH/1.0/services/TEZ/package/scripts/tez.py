import os

# Local Imports
from resource_management.core.resources.system import Directory, File
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.libraries.functions.format import format
from resource_management.core.source import InlineTemplate
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.copy_tarball import copy_to_hdfs


def install_tez():
    import params
    Directory([params.config_dir],
              owner=params.tez_user,
              group=params.user_group,
              mode=0775,
              create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.tez_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute(' rm -rf ' + params.install_dir + '/conf')
        Execute('ln -s ' + params.config_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/tez.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' % (params.tez_user, params.user_group,
                                          params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.tez_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)
        copy_to_hdfs(
            "hive",
            params.user_group,
            params.tez_user,
            custom_source_file=params.stack_root + '/tez/share/tez.tar.gz',
            custom_dest_file='/apps/tez/tez.tar.gz')
        params.HdfsResource(None, action="execute")


def tez(config_dir):
    """
    Write out tez-site.xml and tez-env.sh to the config directory.
    :param config_dir: Which config directory to save configs to, which is different during rolling upgrade.
    """
    import params

    # ensure that matching LZO libraries are installed for Tez

    if config_dir is None:
        config_dir = params.config_dir

    Directory(params.tez_etc_dir, mode=0755)

    Directory(
        config_dir,
        owner=params.tez_user,
        group=params.user_group,
        create_parents=True)

    XmlConfig(
        "tez-site.xml",
        conf_dir=config_dir,
        configurations=params.tez_site_config,
        configuration_attributes=params.config['configurationAttributes']
        ['tez-site'],
        owner=params.tez_user,
        group=params.user_group,
        mode=0664)

    tez_env_file_path = os.path.join(config_dir, "tez-env.sh")
    File(
        tez_env_file_path,
        owner=params.tez_user,
        content=InlineTemplate(params.tez_env_sh_template),
        mode=0555)
