package ar.edu.itba.sds;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class VariationM {
    public static void main(String[] args) {
        try {
            int N = Integer.parseInt(args[0]);
            double L = Double.parseDouble(args[1]);
            double rc = Double.parseDouble(args[2]);
            double r = Double.parseDouble(args[3]);
            boolean periodic = Integer.parseInt(args[4]) == 1;

            List<Particle> particles = generateParticles(N, L, r);

            int maxM = (int) (L / (rc + 2 * r));

            for (int m = 1; m <= maxM; m++) {
                long start = System.nanoTime();

                CellIndexMethod cim = new CellIndexMethod(L, m, rc, periodic);
                cim.populateGrid(particles);
                cim.calculateNeighbors();

                long end = System.nanoTime();
                double timeMs = (end - start) / 1000000.0;

                System.out.println(m + " " + timeMs);
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static List<Particle> generateParticles(int N, double L, double r) {
        List<Particle> particles = new ArrayList<>();
        Random rand = new Random();

        while (particles.size() < N) {
            double x = r + (L - 2 * r) * rand.nextDouble();
            double y = r + (L - 2 * r) * rand.nextDouble();
            boolean overlap = false;

            for (Particle p : particles) {
                double dx = Math.abs(x - p.getX());
                double dy = Math.abs(y - p.getY());
                double dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < (r + p.getRadius())) {
                    overlap = true;
                    break;
                }
            }

            if (!overlap) {
                double vx = (rand.nextDouble() * 2 - 1);
                double vy = (rand.nextDouble() * 2 - 1);
                particles.add(new Particle(particles.size() + 1, r, 1.0, x, y, vx, vy));
            }
        }
        return particles;
    }
}