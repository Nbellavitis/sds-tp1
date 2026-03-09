package ar.edu.itba.sds;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;


public class Simulation {
    public static void main(String[] args) {
        int N = 0;
        double L = 0;
        double rc = 0;
        double r = 0;
        int M = 0;
        boolean periodic = false;
        String method = "CIM";

        if (args.length >= 7) {
            N = Integer.parseInt(args[0]);
            L = Double.parseDouble(args[1]);
            rc = Double.parseDouble(args[2]);
            r = Double.parseDouble(args[3]);
            M = Integer.parseInt(args[4]);
            periodic = Integer.parseInt(args[5]) == 1;
            method = args[6];
        } else {
            Scanner scanner = new Scanner(System.in);
            System.out.print("N: ");
            N = scanner.nextInt();
            System.out.print("L: ");
            L = scanner.nextDouble();
            System.out.print("r_c: ");
            rc = scanner.nextDouble();
            System.out.print("r: ");
            r = scanner.nextDouble();
            System.out.print("M: ");
            M = scanner.nextInt();
            System.out.print("periodic (1 para activar, 0 para desactivar): ");
            periodic = scanner.nextInt() == 1;
            scanner.close();
        }

        List<Particle> particles = generateParticles(N, L, r);

        long startTime = System.nanoTime();
        Map<Integer, Set<Integer>> neighbors;

        if (method.equals("BF")) {
            BruteForce bf = new BruteForce(L, rc, periodic);
            neighbors = bf.calculateNeighbors(particles);
        } else {
            CellIndexMethod cim = new CellIndexMethod(L, M, rc, periodic);
            cim.populateGrid(particles);
            neighbors = cim.calculateNeighbors();
        }

        long endTime = System.nanoTime();

        if (args.length >= 7) {
            System.out.println(((endTime - startTime) / 1000000.0));
        } else {
            System.out.println("Tiempo de ejecucion: " + ((endTime - startTime) / 1000000.0) + " ms");
            saveOutputs(N, L, rc, periodic, particles, neighbors);
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

    private static void saveOutputs(int N, double L, double rc, boolean periodic, List<Particle> particles, Map<Integer, Set<Integer>> neighbors) {
        long ts = System.currentTimeMillis() / 1000;
        new File("data").mkdirs();

        try {
            PrintWriter staticWriter = new PrintWriter(new FileWriter("data/" + ts +  ".txt"));
            staticWriter.println(N);
            staticWriter.println(L);
            for (Particle p : particles) {
                staticWriter.println(p.getRadius() + " " + 1.0);
            }
            staticWriter.close();

            PrintWriter dynamicWriter = new PrintWriter(new FileWriter("data/" + ts + "-Dynamic.txt"));
            dynamicWriter.println("0");
            for (Particle p : particles) {
                dynamicWriter.println(p.getX() + " " + p.getY() + " 0.0 0.0");
            }
            dynamicWriter.close();

            String periodicSuffix = periodic ? "-periodic" : "";
            PrintWriter outWriter = new PrintWriter(new FileWriter("data/" + ts + "-rc-" + rc + periodicSuffix + "-output.txt"));
            for (Map.Entry<Integer, Set<Integer>> entry : neighbors.entrySet()) {
                outWriter.print("[" + entry.getKey());
                List<Integer> sortedNeighbors = new ArrayList<>(entry.getValue());
                sortedNeighbors.sort(Integer::compareTo);
                for (Integer neighbor : sortedNeighbors) {
                    outWriter.print(" " + neighbor);
                }
                outWriter.println("]");
            }
            outWriter.close();

            System.out.println("\nSimulacion finalizada. Archivos generados con timestamp: " + ts);

        } catch (IOException e) {
            System.out.println("Error al guardar los archivos: " + e.getMessage());
        }
    }
}