from resource_management import *
from mongo_base import MongoBase

from resource_management.core.resources.system import File
from resource_management.core.source import InlineTemplate, Template


class MongoClient(MongoBase):
    client_config_path = "/etc/mongoclient.conf"

    def install(self, env):
        import params
        env.set_params(params)
        self.installMongo(env)
        self.configure(env)
        File('/usr/local/bin/mongok', content=Template("mongok"), mode=0755)

    def configure(self, env):
        import params
        env.set_params(params)
        self.configureMongo(env)
        File(
            self.client_config_path,
            content=Template("mongoclient.conf.j2"),
            mode=0644)


if __name__ == "__main__":
    MongoClient().execute()
