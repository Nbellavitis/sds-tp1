package ar.edu.itba.sds;

import java.util.Objects;

public class Particle {
    private int id;
    private double radius;
    private double property;
    private double x;
    private double y;
    private double vx;
    private double vy;

    public Particle(int id, double radius, double property, double x, double y, double vx, double vy) {
        this.id = id;
        this.radius = radius;
        this.property = property;
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
    }

    public double getEdgeToEdgeDistance(Particle other, double L, boolean periodic) {
        double dx = Math.abs(this.x - other.x);
        double dy = Math.abs(this.y - other.y);

        if (periodic) {
            if (dx > L / 2) dx = L - dx;
            if (dy > L / 2) dy = L - dy;
        }

        double centerDistance = Math.sqrt(dx * dx + dy * dy);

        return centerDistance - this.radius - other.radius;
    }

    public int getId() { return id; }
    public double getRadius() { return radius; }
    public double getX() { return x; }
    public double getY() { return y; }
    public double getVx() { return vx; }
    public double getVy() { return vy; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Particle particle = (Particle) o;
        return id == particle.id;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}