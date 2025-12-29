provider "aws" {
  region = "eu-central-1"  
}

resource "aws_key_pair" "chatbot_key" {
  key_name   = "chatbot-ssh-key-${formatdate("YYYYMMDDhhmmss", timestamp())}"
  public_key = var.ssh_public_key
}

variable "ssh_public_key" {
  description = "SSH public key for EC2 access"
  type        = string
}

resource "aws_instance" "chatbot_server" {
  ami           = "ami-0084a47cc718c111a"  
  instance_type = "t3.micro"              
  
  key_name             = aws_key_pair.chatbot_key.key_name
  iam_instance_profile = aws_iam_instance_profile.ssm_profile.name

  vpc_security_group_ids = [aws_security_group.allow_web.id]

  tags = {
    Name = "AI-Chatbot-Server"
  }
}

resource "aws_security_group" "allow_web" {
  name = "allow-web-ssh-${formatdate("YYYYMMDDhhmmss", timestamp())}"

  lifecycle {
    create_before_destroy = true
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Add SSM role and profile
resource "aws_iam_instance_profile" "ssm_profile" {
  name = "ssm-instance-profile-${formatdate("YYYYMMDDhhmmss", timestamp())}"
  role = aws_iam_role.ssm_role.name

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role" "ssm_role" {
  name = "ssm-role-for-ec2-${formatdate("YYYYMMDDhhmmss", timestamp())}"

  lifecycle {
    create_before_destroy = true
  }

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_managed" {
  role       = aws_iam_role.ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}



output "server_ip" {
  value = aws_instance.chatbot_server.public_ip
}

output "instance_id" {
  value = aws_instance.chatbot_server.id
}