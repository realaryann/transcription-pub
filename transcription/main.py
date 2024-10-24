import rclpy
import sys
import os.path
import time
from rclpy.node import Node
from std_msgs.msg import String
from . import voskcall as v


class ScriptPublisher(Node):

    def __init__(self):
        super().__init__('script_publisher')
        self.publisher_ = self.create_publisher(String, 'data_stream', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.creation  = time.ctime(os.path.getctime('/home/csrobot/vosktest/input_saver/recordings/recording.wav'))

    def timer_callback(self):
        if (self.creation != time.ctime(os.path.getctime('/home/csrobot/vosktest/input_saver/recordings/recording.wav'))):
            msg = String()
            filename = "/home/csrobot/vosktest/input_saver/recordings/recording.wav"
            model_path = "/home/csrobot/vosktest/models/vosk-model-en-us-0.22"
            print("INFO: Transcribing audio file now")
            transcriber = v.Transcriber(model_path)
            transcription = transcriber.transcribe(filename)
            for i in transcription:
                msg.data=msg.data+' '+i
            self.creation = time.ctime(os.path.getctime('/home/csrobot/vosktest/input_saver/recordings/recording.wav'))
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    script_publisher = ScriptPublisher()

    rclpy.spin(script_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    script_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()