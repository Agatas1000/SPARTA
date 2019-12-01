from aria import workflow
from aria.orchestrator.workflows.api import task
from aria.orchestrator.workflows.exceptions import TaskException
import sys
from cStringIO import StringIO

@workflow
def createmodel(ctx, graph, outputfile):
    f = open(outputfile, "w")
    f.close()
    for node in ctx.model.node.iter():
        try:
            graph.add_tasks(task.OperationTask(node, 'Sparta', 'createmodel'))
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
        print("\n**** Unsafe connection found *****")
        print(res.getvalue())
        print("\n\n")