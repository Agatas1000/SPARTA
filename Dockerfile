FROM enriquez/aria-openstack

WORKDIR /root
RUN rm .aria
RUN ln -s .aria.ORIG .aria
ADD sparta-plugin/ /root/sparta-plugin/
RUN patch /usr/local/lib/python2.7/site-packages/aria_extension_tosca/profiles/tosca-simple-1.0/nodes.yaml < sparta-plugin/tosca_nodes.patch
RUN patch /usr/local/lib/python2.7/site-packages/aria/orchestrator/workflow_runner.py < sparta-plugin/workflow_runner.patch
RUN wagon create sparta-plugin/
RUN aria plugins install sparta_plugin-1.0-py27-none-linux_x86_64.wgn
RUN cp sparta-plugin/sparta-plugin.yaml .aria/
RUN rm -Rf sparta-plugin/
ADD sparta-workflows/*.py /usr/local/lib/python2.7/site-packages/aria/orchestrator/workflows/sparta/
RUN rm .aria
RUN ln -s /aria/ .aria
