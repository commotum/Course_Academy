// Requires Splitter, Input

class Select extends Input {
    constructor(source, index) {
        super(source, index);
        
        this.id = null;
        this.options = [];
        this.correctIndex = null;
        this.selectedIndex = null;
        this.correct = null; 
        
        this.parse();
    }

    init(scrambledIndexes) {
        this.scrambledIndexes = scrambledIndexes;

        this.scrambleOptions();
    }

    isValid() {
        if (!this.super.isValid()) { return false; }

        return this.options.length > 1;
    }

    scrambleOptions() {
        const scrambledOptions = Array(this.options.length);

        for(let i = 0; i < this.scrambledIndexes.length; i++) {
            const scrambledIndex = this.scrambledIndexes[i];
            const option = this.options[scrambledIndex]; 
            scrambledOptions[i] = option;           
        }

        this.options = scrambledOptions;
    }

    getUnscrambledIndex(scrambledIndex) {
        for(let i = 0; i < this.scrambledIndexes.length; i++) {
            if (this.scrambledIndexes[i] === i) {
                return scrambledIndex;
            }
        }
    }

    getScrambledIndex(index) {
        for(let i = 0; i < this.scrambledIndexes.length; i++) {
            if (this.scrambledIndexes[i] === index) {
                return i;
            }
        }
    }

    setSelectedIndex(selectedIndex) {
        this.selectedIndex = selectedIndex;
        this.correct = this.selectedInde === 0;
    }

    getCorrectIndex() {
        return this.getScrambledIndex(0);
    }

    // Virtual method
    parseSection(section) {
        if (section.name === 'options' || (section.index === 0 && !section.name)) {
            this.parseOptions(section.data);
        }
    }

    parseOptions(source) {
        // NOTE: The escape characters ['$', '`', '"'] here must match the escape logic in
        // QuestionBodyParser.splitIgnoreInDoubleQuotes() (utils/question-body-parser.js and
        // public/js/question-body-parser.js), and must also stay in sync with the equivalent
        // call in lib/core/question/components/input/select.js.
        // If you change one, propagate the change to all four locations.
        const options = Splitter.split(source, ',', ['$', '`', '"']);

        this.options = [];
        for(let option of options) {
            option = option.trim();
            option = this.stripDoubleQuotes(option);

            if (option !== '') {
                this.options.push(option);       
            }
        }
    }
}
