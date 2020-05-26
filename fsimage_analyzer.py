from pyspark.sql.types import StringType
from pyspark.sql.types import ArrayType
from pyspark.sql.functions import udf
from pyspark.sql.functions import explode
from pyspark.sql import SparkSession
import datetime

spark = SparkSession.builder.getOrCreate()
current_date = str(datetime.date.today())

hdfs_path = '/fsimage/'
db_name = 'default'
table_name = 'fsimage_tbl'

tsv_path = hdfs_path + 'fsimage_' + current_date + '.tsv'
tsv_df = spark.read.option('header', 'true').csv(tsv_path, sep='\t')
tsv_df = tsv_df.select('Path', 'Replication', 'PreferredBlockSize',
                       'BlocksCount', 'FileSize').filter('BlocksCount != 0')


def split_path(path):
    index = 1
    paths = []
    while (index > 0):
        paths.append(path[:index])
        index = path.find('/', index + 1)
    return paths


split_path_udf = udf(split_path, ArrayType(StringType(), False))

explode_paths = tsv_df.withColumn('Path',
                                  explode(split_path_udf(tsv_df['Path'])))
explode_paths.createOrReplaceTempView('explodedpaths')

small_blocklist_df = spark.sql(
    "SELECT Path, sum(FileSize)/sum(BlocksCount)/1048576 as avgblocksize, sum(FileSize)/1048576 as TotalSize, sum(BlocksCount) as totalblocks, "
    + " sum(FileSize)/avg(PreferredBlockSize) as idealblocks, " +
    " sum(BlocksCount)-sum(FileSize)/avg(PreferredBlockSize) as blockreduction, "
    + " cast(current_date as string) as extract_dt " +
    " from explodedpaths GROUP BY path ORDER BY blockreduction DESC")

filtered_paths = small_blocklist_df.filter(
    "path not like '/user/oozie%'").filter("path not like '/solr%'").filter(
    "path not like '/hbase%'").filter("path not like '/tmp%'")
filtered_paths.repartition(1).write.mode('append').format(
    'parquet').saveAsTable(
    db_name + '.' + table_name,
    partitionBy='extract_dt',
    compression='snappy')
