const START = Date.now();

class Logger {
    constructor() {
        this.console = document.getElementById('logs');
        this.console.addEventListener('click', () => {
            if (this.console.classList.contains('expanded')) {
                this.console.className = '';
            }
            else {
                this.console.className = 'expanded'
            }
        })
    }

    log(message) {
        const T = Date.now() - START;
        this.console.prepend('[' + T + ']' + message + '\n');
        console.log.apply(console, arguments);
    }
}

const logging = new Logger();
