import time
import hvac
from kubernetes import client, config
def main(vault_addr, unseal_keys):
    print(vault_addr)
    client = hvac.Client(url=vault_addr)
    if not client.sys.is_sealed():
        print("The vault is not sealed!")
        return
print("unsealing vault...")
    client.sys.submit_unseal_keys(keys=unseal_keys)
    time.sleep(3)
    if not client.sys.is_sealed():
        print("Vault unsealed!")
        return
if __name__ == "__main__":
    config.load_kube_config(os.getenv("KUBECONFIG"))
    v1 = client.CoreV1Api()
    ret = v1.list_namespaced_pod("<K8-namespace>",label_selector='<app label>')
    for i in ret.items:
        pod_ips = i.status.pod_ip
        print(pod_ips)
        for ip in str(pod_ips).strip().split('\n'):
            vlt_inst_ip = ip.strip()
            vault_addr = 'http://'+pod_ips+':8200'
            unseal_keys = os.getenv("UNSEAL_KEYS")
            if not unseal_keys:
                raise Exception("Unseal keys not specified!")
            unseal_keys = unseal_keys.split(",")
            main(vault_addr, unseal_keys)
