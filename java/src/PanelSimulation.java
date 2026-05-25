import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.geom.Point2D;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;

public class PanelSimulation extends JPanel {

    private final List<Agent> agents = new ArrayList<>();
    private final HashMap<String, Point2D.Double> lieux = new HashMap<>();


    private int nbSains = 0;
    private int nbInfectes = 0;
    private int nbImmunises = 0;


    private JLabel statsLabel;

    public PanelSimulation() {

        new Timer(33, e -> repaint()).start();
    }

    public synchronized void updateAgents(List<Agent> newAgents) {
        agents.clear();
        agents.addAll(newAgents);
    }

    public synchronized void setLieux(HashMap<String, Point2D.Double> lieux) {
        this.lieux.clear();
        this.lieux.putAll(lieux);
    }

    public void setStatsLabel(JLabel label) {
        this.statsLabel = label;

        this.statsLabel.setFont(new Font("Arial", Font.BOLD, 16));
    }

    @Override
    protected synchronized void paintComponent(Graphics g) {
        super.paintComponent(g);
        setBackground(Color.BLACK);

        if (agents.isEmpty() && lieux.isEmpty()) return;

        double maxX = 1, maxY = 1;

        for (Agent a : agents) {
            if (a.x > maxX) maxX = a.x;
            if (a.y > maxY) maxY = a.y;
        }

        for (Point2D.Double p : lieux.values()) {
            if (p.x > maxX) maxX = p.x;
            if (p.y > maxY) maxY = p.y;
        }

        double scaleX = getWidth() / (maxX + 1);
        double scaleY = getHeight() / (maxY + 1);


        for (String nom : lieux.keySet()) {
            Point2D.Double p = lieux.get(nom);
            int lx = (int) (p.x * scaleX);
            int ly = (int) (p.y * scaleY);


            int r = (int) (3 * scaleX);
            g.setColor(new Color(255, 255, 0, 70));
            g.fillOval(lx - r, ly - r, 2 * r, 2 * r);


            int rd = (int) (0.5 * scaleX);
            g.setColor(new Color(255, 0, 0, 120));
            g.fillOval(lx - rd, ly - rd, 2 * rd, 2 * rd);


            g.setColor(Color.YELLOW);
            g.fillOval(lx - 6, ly - 6, 12, 12);

            g.setColor(Color.WHITE);
            g.drawString(nom, lx + 12, ly - 6);
        }


        for (Agent a : agents) {
            a.draw(g, scaleX, scaleY);
        }


        nbSains = 0;
        nbInfectes = 0;
        nbImmunises = 0;

        for (Agent a : agents) {
            if (a.state == Agent.STATE_INFECTE) nbInfectes++;
            else if (a.state == Agent.STATE_IMMUNISE) nbImmunises++;
            else nbSains++;
        }

        if (statsLabel != null) {
            statsLabel.setText(
                    "Sains : " + nbSains +
                            "   |   Infectés : " + nbInfectes +
                            "   |   Guéris : " + nbImmunises
            );
        }
    }
}
