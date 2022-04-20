FROM registry.access.redhat.com/ubi8/python-38

# # Add application sources with correct permissions for OpenShift
USER 0
ADD src .
RUN chown -R 1001:0 ./
USER 1001

CMD [ "/bin/python3", "-u", "app.py" ]