import java.awt.*;

public class Agent {


    public static final int STATE_SAIN     = 0;
    public static final int STATE_INFECTE  = 1;
    public static final int STATE_IMMUNISE = 2;

    public String name;
    public double x, y;
    public int state;

    public Agent(String name, double x, double y, int state) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.state = state;
    }

    public void draw(Graphics g, double scaleX, double scaleY) {
        int size = 12;


        switch (state) {
            case STATE_INFECTE -> g.setColor(Color.RED);
            case STATE_IMMUNISE -> g.setColor(Color.GREEN);
            default -> g.setColor(Color.CYAN);
        }

        int dx = (int) (x * scaleX);
        int dy = (int) (y * scaleY);

        g.fillOval(dx - size / 2, dy - size / 2, size, size);
    }
}
