spark-submit --jars "C:\jars\mysql-connector-j-8.1.0.jar" --conf "spark.executor.extraJavaOptions=-Dlog4jspark.root.logger=ERROR,console" --conf "spark.driver.extraJavaOptions=-Dlog4jspark.root.logger=ERROR,console" %1