## rabbitMQ 웹 관리자 등록방법
* rabbitmqctl add_user test test
* rabbitmqctl set_user_tags test administrator
* rabbitmqctl set_permissions -p / test ".*" ".*" ".*"