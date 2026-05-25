import javax.swing.*;
import java.awt.*;

public class MainApp {

    public static void main(String[] args) {

        JFrame frame = new JFrame("Simulation Épidémie");
        frame.setSize(1000, 750);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());


        PanelSimulation panel = new PanelSimulation();
        frame.add(panel, BorderLayout.CENTER);


        JLabel statsLabel = new JLabel("Sains : 0   |   Infectés : 0   |   Guéris : 0");
        statsLabel.setForeground(Color.WHITE);
        statsLabel.setBackground(Color.DARK_GRAY);
        statsLabel.setOpaque(true);
        statsLabel.setHorizontalAlignment(SwingConstants.CENTER);
        statsLabel.setFont(new Font("Arial", Font.BOLD, 16));

        frame.add(statsLabel, BorderLayout.NORTH);


        panel.setStatsLabel(statsLabel);


        NetworkThread net = new NetworkThread(panel, "127.0.0.1", 5061);
        net.start();


        JPanel controlPanel = new JPanel();
        controlPanel.setBackground(Color.DARK_GRAY);

        JButton slower = new JButton("⟲ Ralentir");
        JButton faster = new JButton("⟳ Accélérer");

        JLabel speedLabel = new JLabel("Vitesse ×1.0");
        speedLabel.setForeground(Color.WHITE);

        final double[] speedFactor = {1.0};

        slower.addActionListener(e -> {
            speedFactor[0] = Math.max(0.2, speedFactor[0] - 0.2);
            net.sendSpeed(speedFactor[0]);
            speedLabel.setText("Vitesse ×" + speedFactor[0]);
        });

        faster.addActionListener(e -> {
            speedFactor[0] += 0.2;
            net.sendSpeed(speedFactor[0]);
            speedLabel.setText("Vitesse ×" + speedFactor[0]);
        });

        controlPanel.add(slower);
        controlPanel.add(faster);
        controlPanel.add(speedLabel);

        frame.add(controlPanel, BorderLayout.SOUTH);

        // -------------------------------------------------------------------------
        frame.setVisible(true);
    }
}
