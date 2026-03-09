package ar.edu.itba.sds;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;

public class Simulation {

    public static void main(String[] args) {
        List<Particle> particles = null;
        double L = 0;
        double rc = 0;
        int M = 0;
        boolean periodic = false;
        String method = "CIM";
        String baseFilename = String.valueOf(System.currentTimeMillis() / 1000);

        try {
            if (args.length == 5) {
                String staticFile = args[0];
                String dynamicFile = args[1];
                rc = Double.parseDouble(args[2]);
                M = Integer.parseInt(args[3]);
                periodic = Integer.parseInt(args[4]) == 1;

                double[] lArr = new double[1];
                particles = loadParticles(staticFile, dynamicFile, lArr);
                L = lArr[0];
                baseFilename = new File(staticFile).getName().replace(".txt", "");
            } else {
                int N = 0;
                double r = 0;

                if (args.length == 6) {
                    N = Integer.parseInt(args[0]);
                    L = Double.parseDouble(args[1]);
                    rc = Double.parseDouble(args[2]);
                    r = Double.parseDouble(args[3]);
                    M = Integer.parseInt(args[4]);
                    periodic = Integer.parseInt(args[5]) == 1;
                } else {
                    Scanner scanner = new Scanner(System.in);
                    System.out.print("N: "); N = scanner.nextInt();
                    System.out.print("L: "); L = scanner.nextDouble();
                    System.out.print("r_c: "); rc = scanner.nextDouble();
                    System.out.print("r: "); r = scanner.nextDouble();
                    System.out.print("M: "); M = scanner.nextInt();
                    System.out.print("periodic (1=si, 0=no): "); periodic = scanner.nextInt() == 1;
                    scanner.close();
                }

                particles = generateParticles(N, L, r);
                saveMapFiles(N, L, particles, baseFilename);
            }

            long startTime = System.nanoTime();
            Map<Integer, Set<Integer>> neighbors;


            CellIndexMethod cim = new CellIndexMethod(L, M, rc, periodic);
            cim.populateGrid(particles);
            neighbors = cim.calculateNeighbors();


            long endTime = System.nanoTime();
            double timeMs = (endTime - startTime) / 1000000.0;


            System.out.println("Tiempo de ejecucion: " + timeMs + " ms");
            System.out.println("Archivos generados con timestamp: " + baseFilename);


            saveOutputs(rc, neighbors, baseFilename);

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

    private static List<Particle> loadParticles(String staticPath, String dynamicPath, double[] L_out) throws FileNotFoundException {
        List<Particle> particles = new ArrayList<>();
        Scanner staticScanner = new Scanner(new File(staticPath));
        Scanner dynamicScanner = new Scanner(new File(dynamicPath));

        int N = staticScanner.nextInt();
        L_out[0] = staticScanner.nextDouble();

        List<Double> radii = new ArrayList<>();
        List<Double> properties = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            radii.add(staticScanner.nextDouble());
            properties.add(staticScanner.nextDouble());
        }

        dynamicScanner.nextDouble();

        for (int i = 0; i < N; i++) {
            double x = dynamicScanner.nextDouble();
            double y = dynamicScanner.nextDouble();
            double vx = dynamicScanner.nextDouble();
            double vy = dynamicScanner.nextDouble();
            particles.add(new Particle(i + 1, radii.get(i), properties.get(i), x, y, vx, vy));
        }

        staticScanner.close();
        dynamicScanner.close();
        return particles;
    }

    private static void saveMapFiles(int N, double L, List<Particle> particles, String baseFilename) {
        new File("data").mkdirs();
        try {
            PrintWriter staticWriter = new PrintWriter(new FileWriter("data/" + baseFilename + ".txt"));
            staticWriter.println(N);
            staticWriter.println(L);
            for (Particle p : particles) {
                staticWriter.println(p.getRadius() + " " + 1.0);
            }
            staticWriter.close();

            PrintWriter dynamicWriter = new PrintWriter(new FileWriter("data/" + baseFilename + "-Dynamic.txt"));
            dynamicWriter.println("0");
            for (Particle p : particles) {
                dynamicWriter.println(p.getX() + " " + p.getY() + " 0.0 0.0");
            }
            dynamicWriter.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void saveOutputs(double rc, Map<Integer, Set<Integer>> neighbors, String baseFilename) {
        try {
            PrintWriter outWriter = new PrintWriter(new FileWriter("data/" + baseFilename + "-rc-" + rc + "-output.txt"));
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
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
}