class Graphx {
    constructor(canvas) {
        this.canvas = canvas;

        this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);

        this.camera = this.makeCamera(this.canvas);
        this.controls = this.makeControls(this.camera);
        // this.camera.position.z = 5;

        this.scene = new THREE.Scene();
        this.scene.add(this.makeBaseMesh());
        this.makeAxisLines().forEach(l => this.scene.add(l));

        const ambientLight = new THREE.AmbientLight(0x222222);
        this.scene.add(ambientLight);

        this.stats = new Stats();
        document.body.appendChild(this.stats.dom);
    }

    makeBaseMesh() {
        const geometry = new THREE.BufferGeometry();
        // const vertices = new Float32Array([
        //     2.0, -1.5, 2.0,
        //     -2.0, -1.5, 2.0,
        //     -2.0, -1.5, -2.0,
        //     2.0, -1.5, -2.0
        // ]);
        const vertices = new Float32Array([
            100.0, -10.0, 100.0,
            -100.0, -10.0, 100.0,
            -100.0, -10.0, -100.0,

            // could be indexed
            // 1.0, 1.0, 1.0,
            -100.0, -10.0, -100.0,

            100.0, -10.0, -100.0,

            // could be indexed
            100.0, -10.0, 100.0
        ]);
        const vertices2 = [];
        for (let index = vertices.length - 1; index >= 0; index--) {
            vertices2.push(vertices[index]);
        }
        // const indexes = new Uint8Array([
        //     0, 1, 2,
        //     2, 3, 0
        // ]);
        geometry.addAttribute('position', new THREE.BufferAttribute(new Float32Array(vertices2), 3));
        // geometry.setIndex(new THREE.BufferAttribute(indexes, 3))
        const material = new THREE.MeshBasicMaterial({
            color: 0x666666,
            side: THREE.DoubleSide});
        return new THREE.Mesh(geometry, material);
    }

    makeAxisLines() {
        return [0, 1, 2].map(axis => {
            const geometry = new THREE.BufferGeometry();
            const vertices = [0, 0, 0, 0, 0, 0].map((zero, _axis) => _axis == axis ? 1.0 : 0.0 );
            const color = 'rgb(' + [0, 0, 0].map((zero, _axis) => _axis == axis ? 255 : 0).join(', ') + ')';
            geometry.addAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
            const material = new THREE.LineBasicMaterial({ color: new THREE.Color(color) });
            return new THREE.Line(geometry, material);
        });
    }
    makeCamera(canvas) {

        const [width, height] = [canvas.clientWidth, canvas.clientHeight];
        // camera = new THREE.PerspectiveCamera(
        //     75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
        const camera = new THREE.PerspectiveCamera(45, width / height, 0.01, 1000);
        camera.lookAt(0, 0, 0);
        // camera = new THREE.OrthographicCamera(width / - 200, width / 200, height / 200, height / - 200, 1, 1000);
        camera.position.set(0, 10, 20);
        return camera
    }
    makeControls(camera) {
        const controls = new THREE.TrackballControls(this.camera, this.renderer.domElement);
        controls.rotateSpeed = 1.0;
        controls.zoomSpeed = 1.2;
        controls.panSpeed = 0.8;

        controls.noZoom = false;
        controls.noPan = false;

        controls.staticMoving = true;
        controls.dynamicDampingFactor = 0.3;

        controls.keys = [65, 83, 68];
        controls.update();
        return controls
    }

    /**
     * Render the scene on screen.
     *
     * Should be called via `window.requestAnimationFrame(...)`.
     */
    render() {
        // this.cube.rotation.x += 0.01;
        // this.cube.rotation.y += 0.01;
        this.controls.update();
        this.stats.update();
        this.renderer.render(this.scene, this.camera);
    }
}