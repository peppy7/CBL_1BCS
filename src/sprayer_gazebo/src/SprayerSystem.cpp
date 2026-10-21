#include <gz/sim/System.hh>
#include <gz/plugin/Register.hh>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp/executors/single_threaded_executor.hpp>
#include <sprayer_interfaces/msg/sprayer_pressure.hpp>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <memory>

namespace sprayer_gazebo
{
class SprayerSystem:
    public gz::sim::System,
    public gz::sim::ISystemConfigure,
    public gz::sim::ISystemPreUpdate
{
public:
    void Configure(
        const gz::sim::Entity &,
        const std::shared_ptr<const sdf::Element> &,
        gz::sim::EntityComponentManager &,
        gz::sim::EventManager &) override
    {
        ros_context = std::make_shared<rclcpp::Context>();
        ros_context->init(0, nullptr);

        rclcpp::NodeOptions options;
        options.context(ros_context);

        ros_node = std::make_shared<rclcpp::Node>(
            "gazebo_sprayer", options);

        rclcpp::ExecutorOptions executor_options;
        executor_options.context = ros_context;

        executor =
            std::make_shared<rclcpp::executors::SingleThreadedExecutor>(
                executor_options);

        executor->add_node(ros_node);

        target_subscription =
            ros_node->create_subscription<
                sprayer_interfaces::msg::SprayerPressure>(
                "/target_sprayer_pressure",
                10,
                [this](
                    sprayer_interfaces::msg::SprayerPressure::ConstSharedPtr msg)
                {
                    if (!std::isfinite(msg->pressure))
                    {
                        RCLCPP_WARN(
                            ros_node->get_logger(),
                            "Ignoring non-finite target pressure");
                        return;
                    }

                    target_pressure =
                        std::clamp(msg->pressure, 0.0, 2.0);
                });

        pressure_publisher =
            ros_node->create_publisher<
                sprayer_interfaces::msg::SprayerPressure>(
                "/sprayer_pressure", 10);
    }

    void PreUpdate(
        const gz::sim::UpdateInfo &info,
        gz::sim::EntityComponentManager &) override
    {
        executor->spin_some();

        if (info.paused)
        {
            return;
        }

        current_pressure = target_pressure;

        const double sim_time =
            std::chrono::duration<double>(info.simTime).count();

        if (last_publish_time >= 0.0 &&
            sim_time >= last_publish_time &&
            sim_time - last_publish_time < 0.1)
        {
            return;
        }

        sprayer_interfaces::msg::SprayerPressure msg;
        msg.time = sim_time;
        msg.pressure = current_pressure;

        pressure_publisher->publish(msg);
        last_publish_time = sim_time;
    }

private:
    double target_pressure = 0.0;
    double current_pressure = 0.0;

    std::shared_ptr<rclcpp::executors::SingleThreadedExecutor> executor;
    double last_publish_time = -1.0;

    rclcpp::Context::SharedPtr ros_context;
    rclcpp::Node::SharedPtr ros_node;

    rclcpp::Subscription<
        sprayer_interfaces::msg::SprayerPressure
    >::SharedPtr target_subscription;

    rclcpp::Publisher<
        sprayer_interfaces::msg::SprayerPressure
    >::SharedPtr pressure_publisher;
};
}

GZ_ADD_PLUGIN(
    sprayer_gazebo::SprayerSystem,
    gz::sim::System,
    sprayer_gazebo::SprayerSystem::ISystemConfigure,
    sprayer_gazebo::SprayerSystem::ISystemPreUpdate
)