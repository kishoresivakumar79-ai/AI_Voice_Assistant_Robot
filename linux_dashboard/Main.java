package linux_dashboard;

import javax.swing.SwingUtilities;
import javax.swing.UIManager;

public class Main {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception ignored) {}

            Login loginFrame = new Login(e -> {
                Dashboard dashboard = new Dashboard();
                dashboard.setVisible(true);
            });
            loginFrame.setVisible(true);
        });
    }
}
