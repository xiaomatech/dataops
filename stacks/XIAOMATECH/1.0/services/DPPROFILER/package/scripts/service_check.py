from resource_management import *
from ambari_commons import OSConst
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl


class DPProfilerServiceCheck(Script):
    def service_check(self, env):
        pass


if __name__ == "__main__":
    DPProfilerServiceCheck().execute()
