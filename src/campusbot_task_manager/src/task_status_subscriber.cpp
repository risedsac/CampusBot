#include <rclcpp/create_subscription.hpp>
#include <memory>
#include <rclcpp/executors.hpp>
#include <rclcpp/rclcpp.hpp>
#include <rclcpp/subscription.hpp>
#include <std_msgs/msg/detail/string__struct.hpp>
#include <std_msgs/msg/string.hpp>
class task_status_subscriber:public rclcpp::Node{
    public:
        task_status_subscriber();
    private:
        //回调函数
        void subscriber_status(const std_msgs::msg::String::ConstSharedPtr msg){
            RCLCPP_INFO(this->get_logger(),"I heared '%s'",msg->data.c_str());
        }
        //消息对象本身是只读的，内容不可变
        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
};
task_status_subscriber::task_status_subscriber():Node("task_status_subscriber"){
    subscriber_ = this->create_subscription<std_msgs::msg::String>("/campusbot/task_status",10,
            [this](std_msgs::msg::String::ConstSharedPtr msg){this->subscriber_status(msg);});
}
int main(int argc,char ** argv){
    rclcpp::init(argc,argv);
    auto subscriber = std::make_shared<task_status_subscriber>();

    rclcpp::spin(subscriber);
    rclcpp::shutdown();


    return 0;
}
