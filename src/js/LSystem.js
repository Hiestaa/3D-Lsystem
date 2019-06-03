
/**
 * Implement Mechanism for Lindenmayer System generation.
 * The rules and variables are specified in a concrete class
 * Inherit this class to implement a new L-System]
 */
class LSystem {
    /**
     *
     * @param {Turtle} turtle turtle instance for drawing the generated fractal
     * @param {Object} lsSpecs l-system specifications object. This should have the fields
     *  * misc: L-System misc details as an object with the fields:
     *      * name: name of the fractal
     *      * url: url to a wikipedia or other webpage containing fractal description
     *      * angle: default angle applied to rotations
     *      * segment: default segment length applied to forward or backward steps
     *      * steps: default number of steps (when not specified by the user)
     *      * dna: starting code
     *      * drawType: the way the fractal should be rendered
     *                  ('lines', 'line_strip', 'triangles', 'triangle_strip', etc...)
     * * vars: L-System variables, as an object with a field for all symbols specified
     *         in the fractal dna except rules. Values should be the name of the turtle's method.
     *         Symbols not specified as variables will be ignored when drawing.
     * * params: L-System variable parameters, distance / angle / change amount for all
     *           symbols specified in the variables set
     * * rules: L-System replacement rules, indicates what string should a symbol be replaced
     *          with during the fractal's iteration.
     * @param {Boolean} debug debug mode, will print generated fractal code
     */
    constructor(turtle, lsSpecs, debug, id) {
        this.turtle = turtle;
        const {
            misc,
            vars,
            params,
            rules
        } = lsSpecs;
        this.lsSpecs = lsSpecs;

        this.id = id;
        this.LSName = misc.name || 'Undefined (set lsSpecs.misc.name)';
        this.LSSteps = misc.steps || 7;
        this.LSDNA = misc.dna || 'F';
        this.LSDrawType = misc.drawType || 'line_strip';
        this.LSDrawType = this.LSDrawType.toLowerCase();

        this.LSRules = rules || {};
        this.LSVars = vars || {};
        this.LSParams = params || {};

        this.LSStochastic = false;
        this.LSStochRange = 0.01;

        this.LSVertexShader = "";
        this.LSPixelShader = "";

        this.currentStep = 0;
        this.currentMaxStep = 0;
        this.autorun = false;
        this.autorunStep = 5;
        this.stepByStep = false;
        this.LSCode = this.LSDNA;

        this.debug = debug;
        this._lastLog = 0;
        this._generationStart = 0;
        this._turtleRunStart = 0;
        this._interrupt = false;
        this._bindEvents();
    }

    /**
     * Interrupt whichever operation the lsystem is currently performing.
     * Useful if willing to interrupt an on-going async generation
     */
    interrupt() {
        this._interrupt = true;
    }

    /**
     * Run one step of the update loop. Called before every frame rendering.
     */
    update() {
        if (this.stepByStep) {

            this.turtle.begin();

            if (this.autorun) {
                this.incrementMaxStep(this.autorunStep);
            }
            this._executionLoopStepByStep();

            this.turtle.end();
        }
    }

    /**
     * Override default number of steps defined by the constructor.
     * @param {Integer|Float} n number of steps
     */
    setSteps(n) {
        this.LSSteps = n;
        if (this.LSSteps < 1) {
            this.LSSteps = 1;
        }
    }

    /**
     * Generate the code of the fractal from rules and DNA.
     * @param {Function} [done] - done callback. If provided, generation will be asynchroneous
     *      to avoid blocking the main thread. Done willbe called when generation is complete.
     */
    generate(done) {
        this._generationStart = Date.now();
        this._interrupt = false;
        this.LSCode = this.LSDNA;
        logging.log("[LSystem] Generation Started");
        logging.log("[LSystem] Fractal Name: " + this.LSName);
        logging.log("[LSystem] Precision: " + this.LSSteps);
        if (this.LSStochastic) {
            logging.log("[LSystem] Stochastic Factor: " + this.LSStochRange);
        }
        logging.log("[LSystem] Initial Axiom (DNA): " + this.LSDNA);
        logging.log("[LSystem] Rules: ");
        for (const rule in this.LSRules) {
            if (this.LSRules.hasOwnProperty(rule)) {
                const replacement = this.LSRules[rule];
                logging.log('    ' + rule + ' => ' + replacement);
            }
        }

        if (done) {
            this._runGenerationLoopsAsync(() => {
                const t = Date.now() - this._generationStart;
                logging.log("[LSystem] Async Generation Complete (l=" + this.LSCode.length + " t=" + t + "ms)!");
                if (!this._interrupt) { done(); };
            });
        }
        else {
            this._runGenerationLoops();
            const t = Date.now() - this._generationStart;
            logging.log("[LSystem] Generation Complete (l=" + this.LSCode.length + " t=" + t + "ms)!");
        }

    }

    /**
     * Run the turtle over the generated fractal to build the 3D fractal
     * @param {Boolean} stepByStep - step-by-step mode will draw the fractal as it is being generated
     * @param {Function} done - done callback. If provided the running of the turtle will be async
     *      This should avoid blocking the main thred when generating a large fractal.
     */
    runTurtleRun(stepByStep, done) {
        this._turtleRunStart = Date.now();
        this.turtle.reinit();

        this.stepByStep = stepByStep;
        this.turtle.setDrawType(this.LSDrawType);

        if (this.stepByStep) {
            this.currentStep = 0;
            this.currentMaxStep = 0;
            this.incrementMaxStep();
        }

        this.turtle.begin();

        const _done = () => {
            this.turtle.end();
            if (!this.stepByStep) {
                this._turtleLogCompleted(!!done);
            }
            if (done && !this._interrupt) {
                return done();
            }
        }

        if (this.stepByStep) {
            if (done) {
                return this._executionLoopStepByStep(_done);
            }
            this._executionLoopStepByStep();
            return _done();
        }
        if (done) {
            return this._executionLoop(_done);
        }
        this._executionLoop();
        return _done();
    }

    _turtleLog(count, force) {
        if (force || this.turtle.vertexBufferLen > 1 && new Date() - this._lastLog > 1000) {
            const pc = count * 100 / this.LSCode.length
            const _pc = Math.round(pc * 1000) / 1000;
            const t = Date.now() - this._turtleRunStart;
            logging.log("[LSYSTEM][" + t + "ms] > Turtle is running [" + _pc + '%], [' + this.turtle.vertexBufferLen + '] vertex');
            this._lastLog = new Date();
        }
    }

    _turtleLogCompleted(async) {
        this.stepByStep = false;
        const l = this.turtle.vertexBufferLen;
        const t = Date.now() - this._turtleRunStart;
        logging.log("[LSYSTEM] " + (async ? 'Async t' : 'T') + "urtle run completed (l=" + l + ", t=" + t + "ms)!")
    }

    _runGenerationLoops() {
        let rplc_list = [];
        let la = 0;
        let newCode = '';
        for (let step = 0; step < this.LSSteps; step++) {
            rplc_list = [];
            la = 0;

            while (la < this.LSCode.length) {
                const {
                    replacement,
                    laInc
                } = this._applyRule(la);
                rplc_list.push(replacement);
                la += laInc;
            }

            newCode = rplc_list.join('');

            this._generationLog(step, rplc_list);
            if (this.debug) {
                console.log(newCode);
            }
            this.LSCode = newCode;
        }
        this._generationLog(this.LSSteps, [], true);
    }

    _runGenerationLoopsAsync(done) {
        let step = 0
        let look_ahead = 0;
        let rplc_list = [];
        const BATCH_SIZE = 100000;

        const runOneStep = () => {
            rplc_list = [];
            look_ahead = 0;

            if (!this._interrupt) {
                return runBatchTokens();
            }
        }

        const runBatchTokens = () => {
            for (let index = 0; index < BATCH_SIZE; index++) {
                const {
                    replacement,
                    laInc
                } = this._applyRule(look_ahead);
                rplc_list.push(replacement);
                look_ahead += laInc;

                this._generationLog(step, rplc_list);

                if (look_ahead >= this.LSCode.length) { break; }
            }

            this._generationLog(step, rplc_list);

            if (look_ahead < this.LSCode.length) {
                if (!this._interrupt) {
                    return runBatchTokens();
                }
            }
            else {
                if (!this._interrupt) {
                    return completeStep();
                }
            }
        }

        const completeStep = () => {
            const newCode = rplc_list.join('');

            if (this.debug) {
                console.log(newCode);
            }
            this.LSCode = newCode;

            if (step < this.LSSteps) {
                step += 1;
                if (!this._interrupt) {
                    return setTimeout(runOneStep, 0)
                }
            }
            else {
                this._generationLog(step, [], true);
                if (done && !this._interrupt) {
                    done();
                }
            }
        }

        return runOneStep();
    }

    _generationLog(step, rplc_list, force) {
        if (force || Date.now() - this._lastLog > 1000) {
            this._lastLog = Date.now();
            const duration = Date.now() - this._generationStart;
            const len = rplc_list.reduce((acc, s) => acc + s.length, 0);
            const size = Math.max(this.LSCode.length, len);
            logging.log("[LSystem][" + duration + "ms] > Generation [" + step + "], size=" + size);
        }
    }


    _applyRule(la) {
        const char = this.LSCode[la];
        const r = this._getFullRuleKey(char);

        // if rule is set, we need to find the parameter given to the rule
        if (r) {
            const {arg, laInc} = this._findArg(la);
            if (!arg) {
                return {
                    replacement: this.LSRules[r],
                    laInc
                };
            }
            const param = this._findParam(r);
            return {
                replacement: this.LSRules[r].split(param).join(arg),
                laInc
            };
        }
        else {
            return {
                replacement: char,
                laInc: 1
            };
        }
    }

    _findParam(rule) {
        let opening_bracket = 0;
        let closing_bracket = 0;
        for (let k = 0; k < rule.length; k++) {
            if (rule[k] == '(') { opening_bracket = k; }
            if (rule[k] == ')') { closing_bracket = k; }
        }

        if (opening_bracket === 0 || closing_bracket === 0) {
            return null;
        }
        return rule.slice(opening_bracket, closing_bracket);
    }

    _findArg(la) {
        let laInc = 1;
        if (la + laInc > this.LSCode.length) {
            return {laInc, arg: null};
        }
        if (this.LSCode[la + laInc] != '(') {
            return {laInc, arg: null};
        }
        while (this.LSCode[la + laInc] != ')') {
            laInc += 1;
        }

        // la is on the first letter of f(...)
        // la + laInc points to the closing bracket
        const res = this.LSCode.slice(la + 2, la + laInc)

        return {
            arg: null,
            laInc: laInc + 1
        };
    }

    _getFullRuleKey(char) {
        for (const rule in this.LSRules) {
            if (this.LSRules.hasOwnProperty(rule)) {
                // rule name can only have 1 character
                if (rule[0] === char) {
                    return rule;
                };
            }
        }
        return null;
    }

    incrementMaxStep(by=1) {
        if (this.currentMaxStep < this.LSCode.length) {
            this.currentMaxStep += by;
            // increment to the next drawing action
            while (this.currentMaxStep < this.LSCode.length
                   && this.LSVars[this.LSCode[this.currentMaxStep]] != 'forward'
                   && this.LSVars[this.LSCode[this.currentMaxStep]] != 'backward'
                   && this.LSVars[this.LSCode[this.currentMaxStep]] != 'point') {
                this.currentMaxStep += 1;
            }
        }
        if (this.currentMaxStep >= this.LSCode.length) {
            this.currentMaxStep = this.LSCode.length;
        }
    }

    _executionLoopStepByStep(done) {
        while (this.currentStep < this.currentMaxStep) {
            this.currentStep = this._execute(this.currentStep);
            this._turtleLog(this.currentStep);
        }
        if (this.currentStep >= this.LSCode.length - 1) {
            this._turtleLog(this.currentStep, true);
            this._turtleLogCompleted();
        }
        // in step-by step mode, async execution isn't necessary
        if (done) {
            done();
        }
    }

    _executionLoop(done) {
        let count = 0
        const BATCH_SIZE = 100000;

        const _executeBatchAsync = () => {
            for (let index = 0; index < BATCH_SIZE; index++) {
                count = this._execute(count);
                this._turtleLog(count);
                if (count >= this.LSCode.length || this._interrupt) { break; }
            }
            if (count < this.LSCode.length && !this._interrupt) {
                return setTimeout(_executeBatchAsync, 0);
            }
            this._turtleLog(count, true);
            if (!this._interrupt) {
                return done();
            }
        }
        if (done) {
            if (!this._interrupt) {
                return _executeBatchAsync();
            }
        }
        else {
            while (count < this.LSCode.length) {
                count = this._execute(count);
                this._turtleLog(count);
            }
            this._turtleLog(count, true);
        }
    }

    _execute(position) {
        var debug = position;
        const char = this.LSCode[position];
        if (position + 1 < this.LSCode.length && this.LSCode[position + 1] == '(') {
            let {
                arg,
                laInc
            } = this._findArg(position);
            if (arg === null) {
                console.error("Error: No argument found for instruction `" + char + " in: ",
                              this.LSCode.slice(debug, position + 10));
            }

            // if we're executing a parametized rule, replace each variable
            // by its value in the params array
            for (const param of this.LSParams) {
                if (arg.indexOf(param) >= 0) {
                    arg = arg.split(param).join(this.LSParams[param])
                }
            }
            const res = eval(arg);

            if (this.LSVars[char]) {
                this.turtle[this.LSVars[char]](res);
            }

            return position + laInc;
        }
        else {
            if (this.LSVars[char]) {
                this.turtle[this.LSVars[char]](this.LSParams[char]);
            }
            return position + 1;
        }
    }

    _bindEvents() {
        window.addEventListener('keydown', (e) => {
            if (this.currentMaxStep >= this.LSCode.length) {
                return;
            }

            if (e.key === 'n') {
                this.incrementMaxStep();
            }
            if (e.key === 's') {
                this.incrementMaxStep();
            }
            if (e.key === 'r') {
                this.autorun = !this.autorun;
            }
            if (e.key === '+') {
                this.autorunStep *= 10;
            }
            else if (e.key === '-') {
                this.autorunStep /= 10;
            }
        })
    }
}