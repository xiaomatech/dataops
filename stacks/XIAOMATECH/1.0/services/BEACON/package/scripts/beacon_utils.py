# create hdfs directory
def create_hdfs_directory(directory, owner, mode):
    import params
    params.HdfsResource(directory,
                        type="directory",
                        action="create_on_execute",
                        owner=owner,
                        mode=mode,
                        dfs_type=params.default_fs)
