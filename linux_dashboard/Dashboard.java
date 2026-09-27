package linux_dashboard;

import javax.swing.*;
import java.awt.*;

public class Dashboard extends JFrame {
    private ROSClient rosClient;

    public Dashboard() {
        rosClient = new ROSClient("localhost", 9090);
        rosClient.connect();

        setTitle("🤖 AI Voice Assistant Robot — Master Dashboard");
        setSize(1000, 650);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        // Header Status Bar
        JPanel header = new JPanel(new FlowLayout(FlowLayout.LEFT));
        header.setBackground(new Color(30, 35, 45));
        JLabel statusLabel = new JLabel("STATUS: ONLINE | ROS2: CONNECTED | BATTERY: 95% | MODE: VOICE/AUTO");
        statusLabel.setForeground(Color.GREEN);
        statusLabel.setFont(new Font("Monospaced", Font.BOLD, 13));
        header.add(statusLabel);

        // Center Split Layout
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        splitPane.setLeftComponent(new CameraPanel());

        JPanel rightContainer = new JPanel(new GridLayout(2, 1));
        rightContainer.add(new VoicePanel(rosClient));
        rightContainer.add(new ControlPanel(rosClient));
        splitPane.setRightComponent(rightContainer);
        splitPane.setDividerLocation(520);

        add(header, BorderLayout.NORTH);
        add(splitPane, BorderLayout.CENTER);
    }
}
