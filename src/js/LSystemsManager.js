const L_SYSTEMS = {
    'dragon': {
        misc: {
            name: 'Dragon Curve',
            url: 'https://en.wikipedia.org/wiki/Dragon_curve',
            angle: Math.PI / 2,
            segment: 0.01,
            steps: 15,
            dna: '++FX',
            drawType: 'line_strip'
        },
        vars: {
            'F': 'forward',
            'C': 'nextColor',
            '+': 'rotZ',
            '-': 'rotZ'
        },
        params: {
            'F': 0.01,
            'C': 0.000001,
            '+': Math.PI / 2,
            '-': - Math.PI / 2
        },
        rules: {
            'X': "CX+YF",
            'Y': "CFX-Y"
        }
    },
};

const ANGLES = {
    'pi': 'Math.PI',
    'pi/2': 'Math.PI / 2',
    'pi/4': 'Math.PI / 4',
    'pi/6': 'Math.PI / 6',
    'pi/8': 'Math.PI / 8',
    'pi/12': 'Math.PI / 12',
    'pi/16': 'Math.PI / 16',
}

class LSystemsManager {
    constructor(turtle) {
        this.turtle = turtle;
        this.lsystem = null;
        this._generationComplete = false;
        this._onGenerationComplete = null;

        this._buildDOM();
        this._bindEvents();
    }

    update() {
        if (this.lsystem) {
            this.lsystem.update();
        }
    }

    /**
     * Generate lsystem code.
     * Mark `this._generationComplete` to true when generation is completed.
     * Call `this._onGenerationCopmlete` upon generation completion if set.
     * @param {string} lsystem id of the lsystem to generate
     * @param {Boolean} async generate in async mode (to avoid blocking to main thread)
     */
    generate(lsystem, async) {
        if (this.lsystem) {
            this.lsystem.interrupt();
        }
        this._generationComplete = false;
        this._onGenerationComplete = null;

        const base_specs = L_SYSTEMS[lsystem];
        const specs = Object.assign({
            misc: Object.assign({}, base_specs.misc, {
                dna: document.getElementById('dna').value,
                angle: document.getElementById('angle').value,
                segment: document.getElementById('length').value,
                steps: document.getElementById('steps').value,
                drawType: document.getElementById('draw_type').value
            }),
            vars: Object.assign({}, base_specs.vars, {

            }),
            params: Object.assign({}, base_specs.params, {

            }),
            rules: Object.assign({}, base_specs.rules, {

            })
        });
        this.lsystem = new LSystem(this.turtle, specs, false, lsystem);
        const _done = () => {
            this._generationComplete = true;
            if (this._onGenerationComplete) {
                this._onGenerationComplete();
            }
        };
        const res = this.lsystem.generate(async ? _done : undefined);
        if (!async) {
            _done();
        }
        return res;
    }

    /**
     * Draw the lsystem, generating it if necessary.
     * @param {string} lsystem - lsystem to draw - will be generated if necessary
     * @param {boolean} stepByStep - step by step drawing
     * @param {boolean} async - draw in async mode - (avoid blocking the main thread)
     */
    draw(lsystem, stepByStep, async) {
        const _done = () => {
        }
        const _draw = () => {
            this.lsystem.runTurtleRun(stepByStep, async ? _done : undefined);
            this.lsystem.autorun = true;
        }

        if (!this.lsystem || this.lsystem.id !== lsystem) {
            if (this.lsystem) {
                this.lsystem.interrupt();
            }
            if (async) {
                this.generate(lsystem, true);
                this._onGenerationComplete = _draw;
                return;
            }
            this.generate(lsystem);
            return _draw();
        }

        if (!this._generationComplete) {
            this._onGenerationComplete = _draw;
        }
        else {
            return _draw();
        }
    }

    _buildDOM() {
        for (const angle in ANGLES) {
            if (ANGLES.hasOwnProperty(angle)) {
                const valueStr = ANGLES[angle];
                document.getElementById('angle').innerHTML += '<option value="' + angle + '">' + valueStr + '</option>';
            }
        }

        for (const lsystem in L_SYSTEMS) {
            if (L_SYSTEMS.hasOwnProperty(lsystem)) {
                const lsystem_obj = L_SYSTEMS[lsystem];
                document.getElementById('lsystem').innerHTML += '<option value="' + lsystem + '">' + lsystem_obj.misc.name + '</option>';
            }
        }
        this._onSelectLSystem(document.getElementById('lsystem').value);
    }

    _bindEvents() {
        document.getElementById('lsystem').addEventListener('change', (e) => {
            this._onSelectLSystem(e.target.value);
        });
        document.getElementById('steps').addEventListener('change', (e) => {
            document.getElementById('steps-label').innerText = 'Number of steps: ' + e.target.value;
        });
        document.getElementById('keybinds').addEventListener('click', () => {
            document.getElementById('keybinds').style = 'display: none;';
        });
        document.getElementById('generate').addEventListener('click', () => {
            this.generate(
                document.getElementById('lsystem').value,
                document.getElementById('async').checked
            );
        });
        document.getElementById('draw').addEventListener('click', () => {
            this.draw(
                document.getElementById('lsystem').value,
                false,
                document.getElementById('async').checked
            )
        });
        document.getElementById('animate').addEventListener('click', () => {
            this.draw(
                document.getElementById('lsystem').value,
                true,
                document.getElementById('async').checked
            )
        });
    }

    _onSelectLSystem(system) {
        const system_obj = L_SYSTEMS[system];
        document.getElementById('dna').value = system_obj.misc.dna;
        document.getElementById('steps').value = system_obj.misc.steps;
        document.getElementById('steps-label').innerText = 'Number of steps: ' + system_obj.misc.steps;
        document.getElementById('draw_type').value = system_obj.misc.drawType;
        const angles = Object.keys(ANGLES).sort((a, b) => {
            const va = Math.abs(eval(ANGLES[a]) - system_obj.misc.angle);
            const vb = Math.abs(eval(ANGLES[b]) - system_obj.misc.angle);
            return va - vb;
        });
        document.getElementById('angle').value = angles[0];
        document.getElementById('length').value = system_obj.misc.segment.toString();
        document.getElementById('url').setAttribute('href', system_obj.misc.url);
        document.getElementById('url').innerText = system_obj.misc.url;
    };

}

