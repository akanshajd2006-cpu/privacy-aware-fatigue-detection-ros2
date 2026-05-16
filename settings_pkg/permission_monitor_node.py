import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class PermissionMonitorNode(Node):

    def __init__(self):
        super().__init__('permission_monitor_node')

        self.subscription = self.create_subscription(
            String,
            '/settings',
            self.settings_callback,
            10
        )

        self.get_logger().info(
            '[SYSTEM] Permission monitor active'
        )

    def settings_callback(self, msg):

        data = json.loads(msg.data)

        camera = data["camera"]
        typing = data["typing"]
        mode = data["mode"]
        self.get_logger().info(
            f"[MODE] Current Privacy Mode: {mode}"
        )

        self.get_logger().info(
            f"Received Settings: {data}"
        )
        self.get_logger().info(
            f"Received Settings: {data}"
        )

        if not camera:
            self.get_logger().warning(
                '[ACCESS CONTROL] Camera access denied'
            )

        if not typing:
            self.get_logger().warning(
                '[ACCESS CONTROL] Typing analysis disabled'
            )

        if camera and typing:

            self.get_logger().info(
                '[SYSTEM] Full fatigue monitoring active'
            )

            self.get_logger().info(
                '[CONFIDENCE] Fatigue detection confidence: HIGH'
            )

        elif not camera and typing:

            self.get_logger().warning(
                '[PRIVACY MODE] Visual monitoring disabled'
            )

            self.get_logger().info(
                '[SYSTEM] Switching to typing-only analysis'
            )

            self.get_logger().warning(
                '[CONFIDENCE] Fatigue detection confidence: MEDIUM'
            )

        elif not camera and not typing:

            self.get_logger().error(
                '[SYSTEM] Limited fatigue detection mode'
            )

            self.get_logger().error(
                '[CONFIDENCE] Fatigue detection confidence: LOW'
            )


def main(args=None):

    rclpy.init(args=args)

    node = PermissionMonitorNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
