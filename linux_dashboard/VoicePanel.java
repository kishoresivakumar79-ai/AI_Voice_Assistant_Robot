package linux_dashboard;

import javax.swing.*;
import java.awt.*;

public class VoicePanel extends JPanel {
    private JTextArea logArea;
    private JTextField inputField;

    public VoicePanel(ROSClient rosClient) {
        setLayout(new BorderLayout());
        setBorder(BorderFactory.createTitledBorder("🎙️ Voice & AI Assistant Terminal"));

        logArea = new JTextArea();
        logArea.setEditable(false);
        logArea.setBackground(new Color(20, 24, 33));
        logArea.setForeground(new Color(0, 230, 180));
        logArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
        logArea.setText("🤖 Voice System Active.\n[System]: Listening for wake word ('Hello Jarvis')...\n");

        JScrollPane scrollPane = new JScrollPane(logArea);

        JPanel inputPanel = new JPanel(new BorderLayout());
        inputField = new JTextField();
        JButton sendBtn = new JButton("Send Voice Command");

        sendBtn.addActionListener(e -> {
            String text = inputField.getText().trim();
            if (!text.isEmpty()) {
                logArea.append("[User]: " + text + "\n");
                rosClient.sendCommand("/voice/command", text);
                inputField.setText("");
            }
        });

        inputPanel.add(inputField, BorderLayout.CENTER);
        inputPanel.add(sendBtn, BorderLayout.EAST);

        add(scrollPane, BorderLayout.CENTER);
        add(inputPanel, BorderLayout.SOUTH);
    }
}
