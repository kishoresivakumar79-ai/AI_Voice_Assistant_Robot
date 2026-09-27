package linux_dashboard;

import javax.swing.*;
import java.awt.*;

public class ControlPanel extends JPanel {
    public ControlPanel(ROSClient rosClient) {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createTitledBorder("🕹️ Manual Navigation Teleop"));

        JPanel btnGrid = new JPanel(new GridLayout(3, 3, 5, 5));

        JButton fwdBtn = new JButton("▲ FORWARD");
        JButton leftBtn = new JButton("◄ LEFT");
        JButton stopBtn = new JButton("█ STOP");
        JButton rightBtn = new JButton("RIGHT ►");
        JButton backBtn = new JButton("▼ BACKWARD");

        stopBtn.setBackground(new Color(220, 50, 50));
        stopBtn.setForeground(Color.WHITE);

        fwdBtn.addActionListener(e -> rosClient.sendCommand("/cmd_vel", "linear.x=0.5, angular.z=0.0"));
        backBtn.addActionListener(e -> rosClient.sendCommand("/cmd_vel", "linear.x=-0.5, angular.z=0.0"));
        leftBtn.addActionListener(e -> rosClient.sendCommand("/cmd_vel", "linear.x=0.0, angular.z=0.8"));
        rightBtn.addActionListener(e -> rosClient.sendCommand("/cmd_vel", "linear.x=0.0, angular.z=-0.8"));
        stopBtn.addActionListener(e -> rosClient.sendCommand("/cmd_vel", "linear.x=0.0, angular.z=0.0"));

        btnGrid.add(new JLabel(""));
        btnGrid.add(fwdBtn);
        btnGrid.add(new JLabel(""));
        btnGrid.add(leftBtn);
        btnGrid.add(stopBtn);
        btnGrid.add(rightBtn);
        btnGrid.add(new JLabel(""));
        btnGrid.add(backBtn);
        btnGrid.add(new JLabel(""));

        add(btnGrid, BorderLayout.CENTER);
    }
}
