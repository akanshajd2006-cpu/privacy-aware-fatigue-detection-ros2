import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class SettingsNode(Node):

    def __init__(self):
        super().__init__('settings_node')

        self.publisher_ = self.create_publisher(
            String,
            '/settings',
            10
        )

        self.timer = self.create_timer(
            2.0,
            self.publish_settings
        )

        # Privacy mode controller
        self.mode = 0

    def update_privacy_mode(self):

        # Mode 0 = Full Monitoring
        if self.mode == 0:
            self.camera_enabled = True
            self.typing_enabled = True

        # Mode 1 = Privacy Mode
        elif self.mode == 1:
            self.camera_enabled = False
            self.typing_enabled = True

        # Mode 2 = Minimal Monitoring
        elif self.mode == 2:
            self.camera_enabled = False
            self.typing_enabled = False

        # Switch modes automatically
        self.mode = (self.mode + 1) % 3

    def publish_settings(self):

        # Update privacy mode
        self.update_privacy_mode()

        msg = String()

        data = {
            "camera": self.camera_enabled,
            "typing": self.typing_enabled
        }

        msg.data = json.dumps(data)

        self.publisher_.publish(msg)

        # Privacy-aware behavior logs
        if not self.camera_enabled:
            self.get_logger().warning(
                "Camera disabled - visual fatigue tracking blocked"
            )

        if not self.typing_enabled:
            self.get_logger().warning(
                "Typing tracking disabled"
            )

        if not self.camera_enabled and not self.typing_enabled:
            self.get_logger().error(
                "Limited fatigue detection - insufficient sensor data"
            )

        self.get_logger().info(f"Publishing: {msg.data}")


def main(args=None):

    rclpy.init(args=args)

    node = SettingsNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()ain__':
    main()
