import os
from resource_management.core.resources.system import Directory, Execute, File
from resource_management.libraries.resources.xml_config import XmlConfig
from resource_management.core.source import Template, InlineTemplate
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


def install_angel():
    import params
    Directory(
        [params.angel_conf_dir, params.angel_log_dir, params.angel_run_dir],
        owner=params.angel_user,
        group=params.user_group,
        mode=0775,
        create_parents=True)
    if not os.path.exists(Script.get_stack_root() + '/' + params.version_dir) or not os.path.exists(
            params.install_dir):
        Execute('rm -rf %s' % Script.get_stack_root() + '/' + params.version_dir)
        Execute('rm -rf %s' % params.install_dir)
        Execute(
            'wget ' + params.download_url + ' -O /tmp/' + params.filename,
            user=params.angel_user)
        Execute('tar -zxf /tmp/' + params.filename + ' -C  ' + Script.get_stack_root())
        Execute('ln -s ' + Script.get_stack_root() + '/' + params.version_dir + ' ' + params.install_dir)
        Execute('cp -r ' + params.install_dir + '/conf/* ' +
                params.angel_conf_dir + ' ; rm -rf ' + params.install_dir +
                '/conf')
        Execute('ln -s ' + params.angel_conf_dir + ' ' + params.install_dir +
                '/conf')
        Execute("echo 'export PATH=%s/bin:$PATH'>/etc/profile.d/angel.sh" %
                params.install_dir)
        Execute('chown -R %s:%s %s/%s' %
                (params.angel_user, params.user_group, params.stack_root, params.version_dir))
        Execute('chown -R %s:%s %s' % (params.angel_user, params.user_group,
                                       params.install_dir))
        Execute('/bin/rm -f /tmp/' + params.filename)


def angel():
    import params

    Directory(
        params.angel_conf_dir,
        owner=params.angel_user,
        group=params.user_group,
        mode=0755,
        create_parents=True)

    XmlConfig(
        "angel-site.xml",
        conf_dir=params.angel_conf_dir,
        configurations=params.config['configurations']['angel-site'],
        configuration_attributes=params.config['configuration_attributes']
        ['angel-site'],
        owner=params.angel_user,
        group=params.user_group,
        mode=0664)

    XmlConfig(
        "angel-default.xml",
        conf_dir=params.angel_conf_dir,
        configurations=params.config['configurations']['angel-default'],
        configuration_attributes=params.config['configuration_attributes']
        ['angel-default'],
        owner=params.angel_user,
        group=params.user_group,
        mode=0664)

    angel_env_file_path = os.path.join(params.angel_conf_dir, "angel-env.sh")
    File(
        angel_env_file_path,
        owner=params.angel_user,
        content=InlineTemplate(params.angel_env_sh_template),
        mode=0555)
