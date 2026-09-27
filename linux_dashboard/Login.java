package linux_dashboard;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;

public class Login extends JFrame {
    private JTextField usernameField;
    private JPasswordField passwordField;

    public Login(ActionListener onLoginSuccess) {
        setTitle("Robot Control Center - Login");
        setSize(400, 250);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        JPanel headerPanel = new JPanel();
        headerPanel.setBackground(new Color(25, 30, 45));
        JLabel titleLabel = new JLabel("🤖 AI Robot Security Login");
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setFont(new Font("SansSerif", Font.BOLD, 16));
        headerPanel.add(titleLabel);

        JPanel formPanel = new JPanel(new GridLayout(3, 2, 10, 10));
        formPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        formPanel.add(new JLabel("Username:"));
        usernameField = new JTextField("admin");
        formPanel.add(usernameField);

        formPanel.add(new JLabel("Password:"));
        passwordField = new JPasswordField("admin123");
        formPanel.add(passwordField);

        JButton loginBtn = new JButton("Login");
        loginBtn.setBackground(new Color(40, 140, 220));
        loginBtn.setForeground(Color.WHITE);
        loginBtn.addActionListener(e -> {
            String user = usernameField.getText();
            String pass = new String(passwordField.getPassword());
            if ("admin".equals(user) && "admin123".equals(pass)) {
                dispose();
                onLoginSuccess.actionPerformed(e);
            } else {
                JOptionPane.showMessageDialog(this, "Invalid credentials", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        formPanel.add(new JLabel(""));
        formPanel.add(loginBtn);

        add(headerPanel, BorderLayout.NORTH);
        add(formPanel, BorderLayout.CENTER);
    }
}
