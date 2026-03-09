package ar.edu.itba.sds;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class CellIndexMethod {
    private double L;
    private int M;
    private double rc;
    private boolean periodic;
    private Cell[][] grid;

    public CellIndexMethod(double L, int M, double rc, boolean periodic) {
        this.L = L;
        this.M = M;
        this.rc = rc;
        this.periodic = periodic;
        this.grid = new Cell[M][M];

        for (int i = 0; i < M; i++) {
            for (int j = 0; j < M; j++) {
                grid[i][j] = new Cell(i, j);
            }
        }
    }

    public void populateGrid(List<Particle> particles) {
        double cellSize = L / M;
        for (Particle p : particles) {
            int row = (int) (p.getY() / cellSize);
            int col = (int) (p.getX() / cellSize);

            if (row == M) row = M - 1;
            if (col == M) col = M - 1;

            grid[row][col].addParticle(p);
        }
    }

    public Map<Integer, Set<Integer>> calculateNeighbors() {
        Map<Integer, Set<Integer>> neighbors = new HashMap<>();

        for (int i = 0; i < M; i++) {
            for (int j = 0; j < M; j++) {
                for (Particle p : grid[i][j].getParticles()) {
                    if (!neighbors.containsKey(p.getId())) {
                        neighbors.put(p.getId(), new HashSet<Integer>());
                    }
                }
            }
        }

        int[][] directions = {{0, 0}, {0, 1}, {1, 1}, {1, 0}, {-1, 1}};

        for (int i = 0; i < M; i++) {
            for (int j = 0; j < M; j++) {
                Cell currentCell = grid[i][j];
                List<Particle> currentParticles = currentCell.getParticles();

                for (int[] dir : directions) {
                    int neighborRow = i + dir[0];
                    int neighborCol = j + dir[1];

                    if (!periodic) {
                        if (neighborRow < 0 || neighborRow >= M || neighborCol < 0 || neighborCol >= M) {
                            continue;
                        }
                    } else {
                        neighborRow = (neighborRow % M + M) % M;
                        neighborCol = (neighborCol % M + M) % M;
                    }

                    Cell neighborCell = grid[neighborRow][neighborCol];
                    List<Particle> neighborParticles = neighborCell.getParticles();

                    for (int p1Idx = 0; p1Idx < currentParticles.size(); p1Idx++) {
                        Particle p1 = currentParticles.get(p1Idx);

                        int startP2Idx = (dir[0] == 0 && dir[1] == 0) ? p1Idx + 1 : 0;

                        for (int p2Idx = startP2Idx; p2Idx < neighborParticles.size(); p2Idx++) {
                            Particle p2 = neighborParticles.get(p2Idx);

                            double distance = p1.getEdgeToEdgeDistance(p2, L, periodic);

                            if (distance <= rc) {
                                neighbors.get(p1.getId()).add(p2.getId());
                                neighbors.get(p2.getId()).add(p1.getId());
                            }
                        }
                    }
                }
            }
        }
        return neighbors;
    }
}