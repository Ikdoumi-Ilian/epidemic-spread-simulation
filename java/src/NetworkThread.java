import java.awt.geom.Point2D;
import java.io.DataInputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.HashMap;
import java.util.List;

public class NetworkThread extends Thread {

    private final PanelSimulation panel;
    private final String host;
    private final int port;

    private Socket socket;
    private PrintWriter writer;

    private final HashMap<String, Agent> agentsGlobaux = new HashMap<>();

    public NetworkThread(PanelSimulation panel, String host, int port) {
        this.panel = panel;
        this.host = host;
        this.port = port;
    }


    public void sendSpeed(double factor) {
        try {
            if (writer != null) {
                writer.println("SPEED " + factor);
                writer.flush();
                System.out.println("✔ SPEED envoyé au Python : " + factor);
            }
        } catch (Exception e) {
            System.out.println("Erreur envoi SPEED : " + e);
        }
    }

    @Override
    public void run() {
        try {
            socket = new Socket(host, port);
            DataInputStream dis = new DataInputStream(socket.getInputStream());
            writer = new PrintWriter(socket.getOutputStream(), true);

            System.out.println("✔ Connecté au serveur Python");


            int nbLieux = dis.readInt();
            HashMap<String, Point2D.Double> lieux = new HashMap<>();

            for (int i = 0; i < nbLieux; i++) {
                int len = dis.readInt();
                byte[] data = new byte[len];
                dis.readFully(data);

                String nom = new String(data, "UTF-8");
                double x = dis.readDouble();
                double y = dis.readDouble();

                lieux.put(nom, new Point2D.Double(x, y));
            }

            panel.setLieux(lieux);


            while (true) {

                int nameLen = dis.readInt();
                byte[] bytes = new byte[nameLen];
                dis.readFully(bytes);

                String name = new String(bytes, "UTF-8");

                double x = dis.readDouble();
                double y = dis.readDouble();

                int state = dis.readUnsignedByte();

                agentsGlobaux.put(name, new Agent(name, x, y, state));


                List<Agent> liste = agentsGlobaux.values().stream().toList();
                panel.updateAgents(liste);

            }

        } catch (Exception e) {
            System.out.println("Erreur réseau : " + e);
        }
    }
}
