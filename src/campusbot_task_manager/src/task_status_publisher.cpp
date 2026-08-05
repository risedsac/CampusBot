#include <memory>
#include <chrono>
#include <std_msgs/msg/string.hpp>
#include <rclcpp/rclcpp.hpp>
#include <string>
#include <cstddef>
class task_status_publisher:public rclcpp::Node{
    public:
        //构造函数
        task_status_publisher();
    private:
        //时间类型
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
        std::size_t count_;
        void publish_status(){
            auto message = std_msgs::msg::String();
            message.data = "HELLO"+std::to_string(count_++);
            RCLCPP_INFO(this->get_logger(),"Publishing: '%s'",message.data.c_str());
            publisher_->publish(message);
        }
};
task_status_publisher::task_status_publisher():Node("task_status_publisher"),count_(0){
    publisher_ = this->create_publisher<std_msgs::msg::String>("/campusbot/task_status",10);
    //timer_ = this->create_wall_timer(1000ms,std::bind(&task_status_publisher::publish_status,this));
    timer_ = this->create_wall_timer(std::chrono::milliseconds(1000),[this](){this->publish_status();});
}
int main(int argc,char**argv){
    rclcpp::init(argc,argv);
    auto publisher = std::make_shared<task_status_publisher>();
    rclcpp::spin(publisher);
    rclcpp::shutdown();
    return 0;
}
