# docker
image_name=enriquez/aria-openstack
volume=~/sparta
command=docker run -it -v $(volume):/aria/ $(image_name) 

# private key
key_path=/aria/sparta_key
key_name=sparta

# openstack
username=admin
auth_url=http://10.186.37.4/identity
user_domain_name=default

# openstack project
project_name=sparta
project_id=2615a79ad84c41118829a8e82e1d9c0c

sparta-create:
	test -d $(volume)/scenario/ || mkdir $(volume)/scenario/
	cp *.yaml $(volume)/scenario/
	$(command) service-templates store /aria/scenario/sparta.yaml sparta
	$(command) services create -t sparta sparta_service -i "private_key_path=$(key_path);private_key_name=$(key_name)" -vvv

sparta-install:
	grep \"$(project_name)\" $(volume)/openstack_config.json || (read -p "$(username)@$(auth_url) password: " pass && echo "{\n\"username\": \"$(username)\",\n\"password\": \"$$pass\",\n\"project_name\": \"$(project_name)\",\n\"project_id\": \"$(project_id)\",\n\"auth_url\": \"$(auth_url)\",\n\"user_domain_name\": \"$(user_domain_name)\"\n}" > $(volume)/openstack_config.json)
	$(command) executions start install -s sparta_service -vv

sparta-uninstall:
	$(command) executions start uninstall -s sparta_service -vvv

sparta-delete:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	$(command) services delete sparta_service -f
	$(command) service-templates delete sparta

sparta-destroy: sparta-uninstall sparta-delete
