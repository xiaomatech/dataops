#!/usr/bin/env python

from __future__ import print_function
from resource_management import *
from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute, File
from resource_management.core.source import InlineTemplate, Template
from resource_management.libraries.functions.format import format


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)
        seeds = params.seed_provider_parameters_seeds[1:-1].split(",")
        host = seeds[0]
        cmdfile = format("/tmp/cmds")
        File(
            cmdfile,
            mode=0600,
            content=InlineTemplate(
                "CREATE KEYSPACE IF NOT EXISTS smokedemotest WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };\n"
                "Use smokedemotest;\n"
                "CREATE TABLE IF NOT EXISTS smokeusers (firstname text,lastname text,age int,email text,city text,PRIMARY KEY (lastname));\n"
                "INSERT INTO smokeusers (firstname, lastname, age, email, city) VALUES ('John', 'Smith', 46, 'johnsmith@email.com', 'Sacramento');\n"
                "DROP TABLE smokedemotest.smokeusers;\n"
                "DROP KEYSPACE smokedemotest;\n\n"))
        Execute(format("cqlsh {host} {native_transport_port} -f {cmdfile}"))


if __name__ == "__main__":
    ServiceCheck().execute()
