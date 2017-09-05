output "public_ip" {
    value = ["${aws_instance.node.*.public_ip}"]
}

output "private_ip" {
    value = ["${aws_instance.node.*.private_ip}"]
}

output "tags" {
    value = ["${aws_instance.node.*.tags.Name}"]
}

