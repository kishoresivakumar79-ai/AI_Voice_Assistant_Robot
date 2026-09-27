try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
except ImportError:
    # Graceful fallback mock Node if rclpy is not installed on system
    class Node:
        def __init__(self, name):
            self.name = name
            print(f"[ROS2 Node Mock] Created node '{name}'")
        def create_publisher(self, msg_type, topic, qos):
            print(f"[ROS2 Node Mock] Created publisher on topic '{topic}'")
            return self
        def create_subscription(self, msg_type, topic, callback, qos):
            print(f"[ROS2 Node Mock] Created subscriber on topic '{topic}'")
            return self
        def publish(self, msg):
            print(f"[ROS2 Node Mock] Published: {msg}")

from .speech_to_text import ROSSpeechToText
from .text_to_speech import ROSTextToSpeech

class VoiceNode(Node):
    """ROS2 Voice Assistant Node."""

    def __init__(self):
        super().__init__('voice_node')
        self.stt = ROSSpeechToText()
        self.tts = ROSTextToSpeech()
        self.voice_pub = self.create_publisher(String, '/voice/command', 10)
        self.voice_sub = self.create_subscription(String, '/voice/response', self.response_callback, 10)
        print("[VoiceNode] Started voice node and listening on /voice/response")

    def response_callback(self, msg):
        text = getattr(msg, 'data', str(msg))
        print(f"[VoiceNode Received Response]: {text}")
        self.tts.synthesize(text)

    def publish_command(self, text: str):
        msg = String()
        msg.data = text
        self.voice_pub.publish(msg)

def main(args=None):
    try:
        rclpy.init(args=args)
        node = VoiceNode()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()
    except Exception as e:
        print(f"[VoiceNode Standalone Demo] Node executed: {e}")
        node = VoiceNode()
        node.publish_command("Hello Jarvis move forward")

if __name__ == '__main__':
    main()
