variable "domain_name" {
  type = "string"
}

module "digital-ocean-nemo" {
  source = "git::https://github.com/poseidon/typhoon//digital-ocean/container-linux/kubernetes?ref=v1.10.5"

  providers = {
    digitalocean = "digitalocean.default"
    local = "local.default"
    null = "null.default"
    template = "template.default"
    tls = "tls.default"
  }

  # Digital Ocean
  cluster_name = "nemo"
  region       = "fra1"
  dns_zone     = "${var.domain_name}"

  # configuration
  ssh_fingerprints = ["d6:89:e8:4c:1c:40:ab:41:3f:94:94:0d:0e:7f:fc:44"]
  asset_dir        = "pathexpand(~/.secrets/clusters/nemo)"

  # optional
  worker_count = 1
  worker_type  = "s-1vcpu-1gb"
}

