package linux_dashboard;

import javax.swing.*;
import java.awt.*;

public class CameraPanel extends JPanel {
    public CameraPanel() {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createTitledBorder("🎥 Live Vision & Face Tracking"));

        JPanel displayArea = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                g.setColor(new Color(15, 20, 25));
                g.fillRect(0, 0, getWidth(), getHeight());
                
                // Draw camera grid overlay simulation
                g.setColor(new Color(0, 255, 120));
                g.drawRect(50, 40, getWidth() - 100, getHeight() - 80);
                g.drawString("[CAM01 - 1080p 60FPS]", 60, 60);

                // Simulated face detection box
                g.setColor(Color.CYAN);
                int fx = getWidth() / 2 - 40;
                int fy = getHeight() / 2 - 40;
                g.drawRect(fx, fy, 80, 80);
                g.drawString("User (ID: 01)", fx, fy - 5);
            }
        };

        add(displayArea, BorderLayout.CENTER);
    }
}
