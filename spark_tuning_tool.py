
##########################################################################################
#
#   Spark Tuning Tool
#
#   Dan Zaratsian
#
##########################################################################################

import sys
import getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], 'x', ['node_count=', 'node_cores=', 'node_ram=', 'executor_cores='])
    
    node_count = [int(opt[1]) for opt in opts if opt[0]=='--node_count'][0]
    node_cores = [int(opt[1]) for opt in opts if opt[0]=='--node_cores'][0]
    node_ram   = [int(opt[1]) for opt in opts if opt[0]=='--node_ram'][0]
    try:
        executor_cores   = [int(opt[1]) for opt in opts if opt[0]=='--executor_cores'][0]
    except:
        executor_cores = 5  # ~5 or less typically and ideally is a divisor of yarn.nodemanager.resource.cpu-vcores)
except:
    print '\n\n[ USAGE ] spark_tuning_tool.py --node_count=<number> --node_cores=<number> --node_ram=<number_in_GBs> --executor_cores=<5_or_less>\n\n'
    sys.exit(1)


total_cores = node_count * node_cores
total_ram   = node_count * node_ram


yarn_nodemanager_resource_memory_mb  = (node_ram - 2) * 1024
yarn_nodemanager_resource_cpu_vcores = (node_cores - 1)      


executor_cores     = executor_cores  # ~5 or less typically and ideally is a divisor of yarn.nodemanager.resource.cpu-vcores)
executors_per_node = yarn_nodemanager_resource_cpu_vcores / executor_cores 
executor_memory    = ((yarn_nodemanager_resource_memory_mb / executors_per_node))/1024 - 2  # Subtract 2GB for buffer/extra space
num_executors      = (node_count * executors_per_node ) - 1 # Subtract 1 for Driver, since Driver will consume 1 of exector slots


# Output Summary
print '\n\n####################################################################\n' + \
    '\nNode Count:         ' + str(node_count) + \
    '\nNode Cores:         ' + str(node_cores) + \
    '\nNode RAM:           ' + str(node_ram) + ' GB' \
    '\n' + \
    '\nTotal Cores:        ' + str(total_cores) + \
    '\nTotal RAM:          ' + str(total_ram) + ' GB' \
    '\n' + \
    '\nexecutors_per_node: ' + str(executors_per_node) + \
    '\n' + \
    '\n--executor-cores:   ' + str(executor_cores) + \
    '\n--executor-memory:  ' + str(executor_memory) + ' GB' \
    '\n--num-executors:    ' + str(num_executors) + \
    '\n\n' + \
    './bin/spark-submit --master yarn --deploy-mode cluster' + ' --driver-cores ' + str(driver_cores) + ' --driver-memory ' + str(driver_memory) + 'G' + ' --executor-memory ' + str(executor_memory) + 'G' + ' --num-executors ' + str(num_executors) + ' --executor-cores ' + str(executor_cores) + \
    '\n\n####################################################################' 




#ZEND
