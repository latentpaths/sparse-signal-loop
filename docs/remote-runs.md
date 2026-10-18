# Remote runs

These helpers create paid Prime compute resources. Configure the CLI and inspect
the chosen SKU before creating a pod.

Upload an SSH public key and configure its local private-key path:

```sh
./scripts/prime_ssh_key_upload.sh ~/.ssh/id_ed25519.pub
prime config set-ssh-key-path ~/.ssh/id_ed25519
```

Create and connect to a pod:

```sh
./scripts/prime_pod.sh create
prime pods list
prime pods ssh <pod-id>
```

On the pod, bootstrap the repository and dependencies:

```sh
export SPARSE_SIGNAL_LOOP_REPO="https://github.com/latentpaths/sparse-signal-loop.git"
./scripts/prime_pod.sh bootstrap
cd ~/sparse-signal-loop
./scripts/smoke.sh --dry-run
```

Run `./scripts/smoke.sh` only when ready to make real evaluation requests.
Terminate the pod when finished:

```sh
prime pods terminate <pod-id>
```

Optional helper settings include `PRIME_POD_SKU`, `PRIME_API_BASE_URL`,
`SSH_KEY_NAME`, and `SPARSE_SIGNAL_LOOP_REPO`. Run the individual scripts with
`--help` for their supported flags.
