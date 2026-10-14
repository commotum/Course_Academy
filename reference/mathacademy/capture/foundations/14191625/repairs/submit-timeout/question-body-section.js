class QuestionBodySection {
    constructor(index, segments) {
        this.index = index;
        this.segments = segments;
    }

    init() {
        this.initSelects();
        this.initStatus();
        this.updateInputs();
    }

    initSelects() {
        this.inputs = [];
        for(const segment of this.segments) {
            if (segment.select) {
                this.inputs.push(segment.select); 
            } else if (segment.textbox) {
                this.inputs.push(segment.textbox); 
            }
        }
    }

    initStatus() {
        this.complete = true;
        for(const input of this.inputs) {
            if (!input.correct) { 
                this.complete = false; 
                break; 
            }
        }
    }

    updateInputs() {
        for(const input of this.inputs) {
            input.disabled = this.complete;

            if (!this.complete) {
                input.correct = null;
                input.correctIndex = null;
            }
        }
    }
}