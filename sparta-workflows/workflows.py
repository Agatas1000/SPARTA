from aria import workflow
from aria.orchestrator.workflows.api import task
from aria.orchestrator.workflows.exceptions import TaskException
import sys
from cStringIO import StringIO
from fabric.api import run, execute, local, hide, env, put, sudo
import os

@workflow
def createmodel(ctx, graph, outputfile):
    f = open(outputfile, "w")
    f.close()
    for node in ctx.model.node.iter():
        try:
            graph.add_tasks(task.OperationTask(node, 'Sparta', 'compilebehavior'))
        except TaskException:
            pass

@workflow
def validate(ctx, graph, modelfile):
    f = open("/tmp/temp_datalog.py", "w")
    d = open(modelfile, "r")

    f.write("import logging\nfrom pyDatalog import pyDatalog\nfrom pyDatalog import pyEngine\n"
            "pyEngine.Logging = True\nlogging.basicConfig(level=logging.INFO)\n\n")
    f.write("pyDatalog.create_terms('isConnected, SecurityLabel, isUnsafe, M, N, L1, L2')\n\n")
    f.write(d.read())
    d.close()
    f.write("\nisUnsafe(M, N) <= isConnected(M, N) & SecurityLabel(M, L1) & SecurityLabel(N, L2) & (L1 > L2)\n")
    f.write("print(isUnsafe(M, N))\n")
    f.close()

    f = open("/tmp/temp_datalog.py", "r")
    datalogfile = f.read()
    f.close()

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    log = sys.stderr = StringIO()
    res = sys.stdout = StringIO()
    # TODO: security hole!
    exec(datalogfile) in locals()
    #print(log.getvalue())
    #while not log.getvalue():
    #    print("acc")
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if not res.getvalue()[:2] == "[]":
        print("\n\033[0m\033[91m**** Unsafe connections found *****\033[0m")
        print(res.getvalue())
        print("\n\n")

    u = open(modelfile + ".log", "w")
    l = 0
    for r in res.getvalue().splitlines():
        if l > 1:
            u.write(r + "\n")
        l=l+1
    u.close()

@workflow
def enforce(ctx, graph, modelfile):
    # set username and key for ssh
    env.user = "alpine"
    env.key_filename = os.path.expanduser("/aria/sparta_key")
    env.sudo_user = "root"

    log = open(modelfile + '.log', 'r')

    for l in log.read().splitlines():
        compute = l.split("|")[0].strip()  # [:-1]
        network = l.split("|")[1].strip()  # [1:]

        for node in ctx.model.node.iter():
            if compute in node.attributes['tosca_id']:
                compute_ip = node.outbound_relationships[0].target_node.attributes['ip']
                compute_ip2 = node.outbound_relationships[0].target_node.attributes['networks'][network.split('_')[0]][
                    0]

            if network in node.attributes['tosca_id']:
                network_ip = node.properties['subnet']['cidr']

        print("\033[92m{} ({}, {}) -> {} ({})\033[0m".format(compute.split('_')[0], compute_ip, compute_ip2, network.split('_')[0],
                                              network_ip))

        env.hosts = [compute_ip]
        out = execute(runLinux, compute_ip2)

    log.close()



def runLinux(ip):
    sudo("int=$(ifconfig | grep -B 1 {} | grep eth | cut -d' ' -f 1); echo \"Shutting down $int..\"; ifconfig $int down".format(ip))