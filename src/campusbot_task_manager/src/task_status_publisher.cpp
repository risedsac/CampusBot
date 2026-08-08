#include <exception>
#include <memory>
#include <chrono>
#include <std_msgs/msg/string.hpp>
#include <rclcpp/rclcpp.hpp>
#include <string>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
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
   //固定为1000ms
    //lamba表达式
   // timer_ = this->create_wall_timer(std::chrono::milliseconds(1000),[this](){this->publish_status();});
   //传递参数周期或者频率
   const auto publish_period_ms = this->declare_parameter<std::int64_t>("publish_period_ms",1000);

   if(publish_period_ms <= 0 ){
       throw std::invalid_argument("publish_period_ms must be greater than 0 ");

   }

RCLCPP_INFO_STREAM(
      this->get_logger(),
      "Publish period: " << publish_period_ms << " ms");
    publisher_ = this->create_publisher<std_msgs::msg::String>("/campusbot/task_status",10);
   timer_ = this->create_wall_timer(std::chrono::milliseconds(publish_period_ms),[this](){this->publish_status();});
}
int main(int argc,char**argv){
    rclcpp::init(argc,argv);
    int exit_code=0;
    try{

    auto publisher = std::make_shared<task_status_publisher>();
    rclcpp::spin(publisher);
    }
    catch(const std::exception & error){
    //FATAL表示程序无法运行的严重错误
    RCLCPP_FATAL(rclcpp::get_logger("task_status_publisher"),"%s",error.what());
    exit_code=1;
    }
    rclcpp::shutdown();
    return exit_code;
}
