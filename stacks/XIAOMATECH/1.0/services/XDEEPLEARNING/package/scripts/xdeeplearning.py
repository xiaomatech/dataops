from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script

from resource_management.core.resources.system import Directory
from resource_management.core.resources.system import File
import os


def install_xdeeplearning():
    import params

    if not os.path.exists('/usr/bin/' + params.filename):
        Execute('wget ' + params.download_url + ' -O /usr/bin/' + params.filename, user=params.xlearning_user)

    File('/usr/bin/xdl_submit.py',
         mode=0755,
         content=params.xdl_submit_content)


class xdeeplearning(Script):
    def install(self, env):
        import params
        env.set_params(params)
        self.install_packages(env)
        install_xdeeplearning()

    def configure(self, env):
        import params
        env.set_params(params)
        install_xdeeplearning()
        File('/usr/bin/xdl_submit.py',
             mode=0755,
             content=params.xdl_submit_content)


if __name__ == "__main__":
    xdeeplearning().execute()
