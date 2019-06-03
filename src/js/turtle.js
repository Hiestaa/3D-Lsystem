
/**
 * Implementation of a Logo Turtle
 * Used to execute a generated fractal's code
 */
class Turtle {
    /**
     * Initialize the turtle
     * @param {Graphx} graphx - graphx instance used to add meshes to the scene
     * @param {Object} [pos] - initial position of the turtle, as a {x, y, z} object (default to the origin)
     * @param {Boolean} [debug] - enable debugging mode
     */
    constructor(graphx, debug, pos) {
        this.debug = debug;
        this.graphx = graphx;
        this.stateStack = [];
        this.stochasticFactor = 0;

        this.drawType = 'line_strip';

        this.reinit(pos);
        this.point();
    }

    setDrawType(drawType) {
        this.drawType = drawType;
    }

    randomize(value) {
        if (!this.stochasticFactor) { return value; }
        return ((Math.random() * 2 * this.stochasticFactor) - this.stochasticFactor) * value + value;
    }

    reinit(pos) {
        if (!pos) {
            this.pos = new THREE.Vector3(0, 0, 0)
        }
        else {
            this.pos = new THREE.Vector3(pos.x, pos.y, pos.z)
        }

        this.heading = new THREE.Vector3(0, 1, 0);
        this.color = new THREE.Color(0.5, 0.25, 0.0);

        this.vertexBuffers = [];
        this.vertexBufferLen = 0;
        this.vertexBufferChanged = false;
        this.vertexPositions = null;

        if (this.meshes) {
            this.meshes.forEach(m => {
                this.graphx.scene.remove(m);
            });
        }
        this.meshes = [];
    }

    /**
     * Draw the turtle path
     */
    update() {
        if (this.vertexBufferChanged) {
            this.meshes.forEach(m => {
                this.graphx.scene.remove(m);
            });

            let total = 0;
            this.meshes = [this._miniSphere()].concat(this.vertexBuffers.map(vertexBuffer => {
                total += vertexBuffer.positions.length / 3;
                // TODO: honor this.drawStyle
                const geometry = new THREE.BufferGeometry();
                geometry.addAttribute('position', new THREE.Float32BufferAttribute(vertexBuffer.positions, 3));
                geometry.addAttribute('color', new THREE.Float32BufferAttribute(vertexBuffer.colors, 3));
                const material = new THREE.LineBasicMaterial({});
                return new THREE.Line(geometry, material);
            }));

            this.vertexBufferLen = total;

            this.vertexBufferChanged = false;

            this.meshes.forEach(m => {
                this.graphx.scene.add(m);
            });
        }
    }

    /**
     * Add a point at the current position of the turtle
     * @param {Boolean} breakline - enable to prevent a line to be drawn from the previous point
     */
    point(breakline=false) {
        if (breakline || this.vertexBuffers.length === 0) {
            this.vertexBuffers.push(new VertexBuffer());
        }
        const vertexBuffer = this.vertexBuffers[this.vertexBuffers.length - 1];

        vertexBuffer.addVertex(
            [this.pos.x, this.pos.y, this.pos.z],
            [this.color.r, this.color.g, this.color.b]
        );

        this.vertexBufferLen += 1;
        this.vertexBufferChanged = true;
    }

    /**
     * Begin a command list
     * @param {Boolean} reinit - enable to reinitialize the turtule
     */
    begin(reinit=false) {
        if (this.debug) {
            logging.log("[Turtle] begin(reinit=" + reinit + ")");
        }
        this.vertexBufferChanged = false;

        if (reinit) {
            this.reinit();
        }
    }

    /**
     * Push current state (pos, heading and color) onto the state stack
     */
    push() {
        if (this.debug) {
            logging.log("[Turtle] push()");
        }
        this.stateStack.push(new TurtleState(this.pos, this.heading, this.color));
    }

    /**
     * Rollback to the last pushed state of the state stack
     */
    pop() {
        if (this.debug) {
            logging.log("[Turtle] pop()");
        }
        const state = this.stateStack.pop();
        this.color.copy(state.color);
        this.pos.copy(state.pos);
        this.heading.copy(state.heading);
    }

    /**
     * Move forward (and draw a point)
     * @param {Float} step distance
     */
    forward(step) {
        if (this.debug) {
            logging.log('[Turtle] forward(' + step + ')');
        }
        this.pos.add(this.heading.clone().multiplyScalar(this.randomize(step)));
        this.point();
    }

    /**
     * Rotation around the X axis
     * @param {Float} angle in radians
     */
    rotX(angle) {
        if (this.debug) {
            logging.log('[Turtle] rotX(' + angle + ')');
        }
        angle = this.randomize(angle);
        this.heading.set(
            this.heading.x,
            this.heading.y * Math.cos(angle) - this.heading.z * Math.sin(angle),
            this.heading.y * Math.sin(angle) + this.heading.z * Math.cos(angle)
        );
    }

    /**
     * Rotation around the Y axis
     * @param {Float} angle in radians
     */
    rotY(angle) {
        if (this.debug) {
            logging.log('[Turtle] rotY(' + angle + ')');
        }
        angle = this.randomize(angle);
        this.heading.set(
            this.heading.x * Math.cos(angle) + this.heading.z * Math.sin(angle),
            this.heading.y,
            - this.heading.x * Math.sin(angle) + this.heading.z * Math.cos(angle));
    }

    /**
     * Rotation around the Z axis
     * @param {Float} angle in radians
     */
    rotZ(angle) {
        if (this.debug) {
            logging.log('[Turtle] rotZ(' + angle + ')');
        }
        angle = this.randomize(angle);
        this.heading.set(
            this.heading.x * Math.cos(angle) - this.heading.y * Math.sin(angle),
            this.heading.x * Math.sin(angle) + this.heading.y * Math.cos(angle),
            this.heading.z
        );
    }

    /**
     * Set the color
     * @param {Object} color - {r, g, b} color object
     */
    setColor(color) {
        if (this.debug) {
            logging.log('[Turtle] setColor(' + color + ')');
        }
        this.color.setRGB(
            color.r,
            color.g,
            color.b
        );
    }

    /**
     * Get to the next color, by order of hue
     * @param {Float} step - step by which to increase the hue
     */
    nextColor(step) {
        if (this.debug) {
            logging.log('[Turtle] nextColor(' + step + ')');
        }
        const hsl = this.color.clone().getHSL({});
        let newH = hsl.h + step;
        if (newH >= 1.0) {
            newH -= 1.0;
        }
        this.color.setHSL(
            newH,
            hsl.s,
            hsl.l
        );
    }

    /**
     * End a command sequence
     */
    end() {
    }

    /**
     * Move backward (and draw a point)
     * @param {Float} step distance
     */
    backward(step) {
        return this.forward(-step)
    }

    /**
     * Inverted rotation around the X axis
     * @param {Float} angle in radians
     */
    iRotX(angle) {
        return this.rotX(-angle);
    }

    /**
     * Inverted rotation around the Y axis
     * @param {Float} angle in radians
     */
    iRotY(angle) {
        return this.rotY(-angle);
    }

    /**
     * Inverted rotation around the Z axis
     * @param {Float} angle in radians
     */
    iRotZ(angle) {
        return this.rotZ(-angle);
    }



    _miniSphere() {
        return new THREE.Mesh(
            new THREE.SphereBufferGeometry(0.01, 8, 4),
            new THREE.MeshBasicMaterial({ color: this.color.clone() })
        );
    }
}

class VertexBuffer {
    constructor() {
        this.positions = [];
        this.colors = [];
    }

    addVertex(position, color) {
        for (const component of position) {
            this.positions.push(component);
        }
        for (const component of color) {
            this.colors.push(component);
        }
    }
}

/**
 * Represents a state of the turtle, for push and pop operations
 */
class TurtleState {
    /**
     * Initialize a state of the turtle
     * @param {THREE.Vector3} pos - position of the turtle, THREE.Vector3 object
     * @param {THREE.Vector3} heading - heading of the turtle, THREE.Vector3 object
     * @param {THREE.Color} color - color of the turtle, as a THREE.Color object
     */
    constructor(pos, heading, color) {
        this.pos = pos.clone();
        this.heading = heading.clone();
        this.color = color.clone();
    }
}
