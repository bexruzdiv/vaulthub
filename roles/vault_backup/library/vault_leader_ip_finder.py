#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess
import os

def find_leader_ip(vault_addr, vault_token):
    try:
        env_vars = os.environ.copy()
        env_vars["VAULT_ADDR"] = vault_addr
        env_vars["VAULT_TOKEN"] = vault_token

        output = subprocess.check_output(["vault", "operator", "raft", "list-peers"], universal_newlines=True, env=env_vars)
        lines = output.strip().split('\n')[2:]  # Skip the header
        for line in lines:
            fields = line.split()
            if len(fields) >= 3 and fields[2] == "leader":
                # Extract the IP address from the address field
                leader_ip = fields[1].split(':')[0]
                return leader_ip
    except subprocess.CalledProcessError as e:
        # Handle subprocess error if the command fails
        return None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_addr=dict(required=True, type='str', env_var='VAULT_ADDR'),
            vault_token=dict(required=True, type='str', no_log=True, env_var='VAULT_TOKEN')
        )
    )

    vault_addr = module.params['vault_addr']
    vault_token = module.params['vault_token']
#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess
import os

def find_leader_ip(vault_addr, vault_token):
    try:
        env_vars = os.environ.copy()
        env_vars["VAULT_ADDR"] = vault_addr
        env_vars["VAULT_TOKEN"] = vault_token

        output = subprocess.check_output(["vault", "operator", "raft", "list-peers"], universal_newlines=True, env=env_vars)
        lines = output.strip().split('\n')[2:]  # Skip the header
        for line in lines:
            fields = line.split()
            if len(fields) >= 3 and fields[2] == "leader":
                # Extract the IP address from the address field
                leader_ip = fields[1].split(':')[0]
                return leader_ip
    except subprocess.CalledProcessError as e:
        # Handle subprocess error if the command fails
        return None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_addr=dict(required=True, type='str', env_var='VAULT_ADDR'),
            vault_token=dict(required=True, type='str', no_log=True, env_var='VAULT_TOKEN')
        )
    )

    vault_addr = module.params['vault_addr']
    vault_token = module.params['vault_token']

    leader_ip = find_leader_ip(vault_addr, vault_token)
    if leader_ip:
        module.exit_json(changed=False, leader_ip=leader_ip)
    else:
        module.fail_json(msg="Failed to find leader IP")

if __name__ == '__main__':
    main()

    leader_ip = find_leader_ip(vault_addr, vault_token)
    if leader_ip:
        print(leader_ip)
    else:
        module.fail_json(msg="Failed to find leader IP")

if __name__ == '__main__':
    main()
