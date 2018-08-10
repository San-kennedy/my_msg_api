variable "access_key" {}
variable "secret_key" {}
variable "region" {
  default = "ap-south-1"
}
variable "bootstrap_path" {
  default = "bootstrap.sh"
}
variable "publickey" {}
variable "privatekey" {}

provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = "${var.publickey}"
}

resource "aws_security_group" "appsec" {
  name = "my_msg_api"

  ingress {
    from_port   = 22
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "my_msg_api" {
  ami           = "ami-d783a9b8"
  instance_type = "t2.micro"
  key_name      = "${aws_key_pair.deployer.key_name}"
  user_data     = "${file("${var.bootstrap_path}")}"
  vpc_security_group_ids = ["${aws_security_group.appsec.id}"]

  provisioner "file" {
    source      = "docker-compose.yml"
    destination = "/home/ec2-user/docker-compose.yml"
    connection {
    user        = "ec2-user"
    private_key = "${var.privatekey}"
    }
  }


  provisioner "remote-exec" {

    inline = ["sleep 150","sudo /usr/local/bin/docker-compose -f /home/ec2-user/docker-compose.yml up -d"]
    connection {
    user        = "ec2-user"
    private_key = "${var.privatekey}"
    }
  }
}
output "endpoint hostname" {
    value = "${aws_instance.my_msg_api.public_dns}"
}
