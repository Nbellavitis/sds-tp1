package ar.edu.itba.sds;

import java.util.*;

public class BruteForce {
    private double L;
    private double rc;
    private boolean periodic;

    public BruteForce(double L, double rc, boolean periodic) {
        this.L = L;
        this.rc = rc;
        this.periodic = periodic;
    }

    public Map<Integer, Set<Integer>> calculateNeighbors(List<Particle> particles) {
        Map<Integer, Set<Integer>> neighbors = new HashMap<>();

        for (Particle p : particles) {
            neighbors.put(p.getId(), new HashSet<Integer>());
        }

        for (int i = 0; i < particles.size(); i++) {
            Particle p1 = particles.get(i);
            for (int j = i + 1; j < particles.size(); j++) {
                Particle p2 = particles.get(j);

                double distance = p1.getEdgeToEdgeDistance(p2, L, periodic);

                if (distance <= rc) {
                    neighbors.get(p1.getId()).add(p2.getId());
                    neighbors.get(p2.getId()).add(p1.getId());
                }
            }
        }
        return neighbors;
    }
}