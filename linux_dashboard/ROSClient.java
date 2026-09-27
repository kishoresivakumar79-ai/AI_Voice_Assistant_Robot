package linux_dashboard;

import java.io.*;
import java.net.*;

public class ROSClient {
    private String host;
    private int port;
    private boolean connected;

    public ROSClient(String host, int port) {
        this.host = host;
        this.port = port;
        this.connected = false;
    }

    public boolean connect() {
        System.out.println("[ROSClient] Connecting to ROS2 Bridge at " + host + ":" + port + "...");
        this.connected = true; // Simulated successful connection
        return true;
    }

    public void sendCommand(String topic, String commandPayload) {
        if (!connected) {
            System.out.println("[ROSClient Warning] Not connected to ROS2 bridge.");
            return;
        }
        System.out.println("[ROSClient] Sent to " + topic + ": " + commandPayload);
    }

    public boolean isConnected() {
        return connected;
    }
}
