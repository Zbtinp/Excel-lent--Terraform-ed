provider "aws" {
 region = "us-east-2" 
 access_key = "AKIAJHF5CKDUXX3CBIPQ" 
 secret_key = "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" 
 } 

 
resource "tls_private_key" "key1" { 
 algorithm = RSA
 rsa_bits = 4096
 } 
 
resource "aws_key_pair" "genkey1" { 
 key_name = SSH-Key
 public_key = "${tls_private_key.key1.public_key_openssh}" 
 } 
 
resource "aws_security_group" "ubuntu_allow_http_ssh" { 
 name = "ubuntu_allow_http_ssh" 
 description = "Allow�HTTP�and�SSH�inbound�traffic" 
 
 ingress { 
  type = "ingress" 
  description = "ssh" 
  from_port = "22" 
  to_port = "22" 
  protocol = "tcp" 
  cidr_blocks = "0.0.0.0/0" 
  } 
 
ingress { 
  type = "ingress" 
  description = "https" 
  from_port = "443" 
  to_port = "443" 
  protocol = "tcp" 
  cidr_blocks = "0.0.0.0/0" 
  } 
 
ingress { 
  type = "ingress" 
  description = "http" 
  from_port = "80" 
  to_port = "80" 
  protocol = "tcp" 
  cidr_blocks = "0.0.0.0/0" 
  } 
 
egress { 
  type = "egress" 
  description = "egress" 
  from_port = "0" 
  to_port = "0" 
  protocol = "-1" 
  cidr_blocks = "0.0.0.0/0" 
  } 
 
} 
 
