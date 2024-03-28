
#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
    os.environ["HOME"] = "/tmp"

def vault_leader_ip_finder(vault_address, vault_token):
    import os
    os.environ["HOME"] = "/tmp"
    cmd = ["vault", "operator", "raft", "list-peers", "--address={}".format(vault_address)]
    env = {"VAULT_TOKEN": vault_token}
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return False, "Failed to execute vault command: {}".format(stderr.decode())

        for line in stdout.decode().splitlines():
            if "leader" in line:
                return True, line.split()[1].split(':')[0]  # Extract and return IP

        return False, "Vault leader not found"
    
    except Exception as e:
        return False, "Error occurred while executing vault command: {}".format(str(e))

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_address=dict(type='str', required=True),
            vault_token=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    vault_address = module.params['vault_address']
    vault_token = module.params['vault_token']
    
    is_success, result = vault_leader_ip_finder(vault_address, vault_token)

    if is_success:
        module.exit_json(changed=False, leader_ip=result)
    else:
        module.fail_json(msg=result)

if __name__ == '__main__':
    main()

#!/usr/bin/python

# from ansible.module_utils.basic import AnsibleModule
# import subprocess
# import json

# def vault_leader_ip_finder(vault_address, vault_token):
#     cmd = ["vault", "operator", "raft", "list-peers", "--address={}".format(vault_address)]
#     env = {"VAULT_TOKEN": vault_token}
#     try:
#         process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
#         stdout, stderr = process.communicate()
#         if process.returncode != 0:
#             return False, stderr.decode()
        
#         for line in stdout.decode().splitlines():
#             if "leader" in line:
#                 return True, line.split()[1].split(':')[0]  # Extract and return IP
#         return False, "Leader not found"
#     except Exception as e:
#         return False, str(e)

# def main():
#     module = AnsibleModule(
#         argument_spec=dict(
#             vault_address=dict(type='str', required=True),
#             vault_token=dict(type='str', required=True),
#         ),
#         supports_check_mode=True
#     )

#     vault_address = module.params['vault_address']
#     vault_token = module.params['vault_token']
    
#     is_success, result = vault_leader_ip_finder(vault_address, vault_token)

#     if is_success:
#         module.exit_json(changed=False, leader_ip=result)
#     else:
#         module.fail_json(msg=result)

# if __name__ == '__main__':
#     main()
