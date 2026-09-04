class Shape {
    calculateArea() {
        return 0;
    }
}

class Circle extends Shape {
    constructor(radius) {
        super();
        this.radius = radius;
    }

    calculateArea() {
        return Math.PI * this.radius * this.radius;
    }
}

class Triangle extends Shape {
    constructor(base, height) {
        super();
        this.base = base;
        this.height = height;
    }

    calculateArea() {
        return 0.5 * this.base * this.height;
    }
}

const circle = new Circle(5);
console.log("Circle Area:", circle.calculateArea());

const triangle = new Triangle(10, 6);
console.log("Triangle Area:", triangle.calculateArea());
