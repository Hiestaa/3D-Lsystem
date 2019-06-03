class Main {
    constructor() {
        this.graphx = new Graphx(document.getElementById('canvas'));
        this.turtle = new Turtle(this.graphx);
        this.lsystemsManager = new LSystemsManager(this.turtle);
    }

    render() {
        window.requestAnimationFrame(this.render.bind(this));
        this.turtle.update();
        this.lsystemsManager.update();
        this.graphx.render();
    }
}

const main = new Main()
main.render();
