// Requires Input, FreeResponseChecker

class Textbox extends Input {
    constructor(source, index) {
        super(source, index);

        this.VALID_TYPES = ['number', 'expression', 'equation', 'string'];      

        this.answer = null;
        this.type = null;
        this.width = 50;
        this.background = '';
        this.buttons = [];

        this.parse();

        this.checker = new FreeResponseChecker(this.type, this.answer); 
    }

    isValid() {
        if (!this.super.isValid()) { return false; }
        if (!this.type) { return false; }

        return true;
    }

    // Virtual method
    parseSection(section) {
        switch (section.name) {
            case 'answer': this.parseAnswer(section.data); break;
            case 'type': this.parseType(section.data); break;
            case 'width': this.parseWidth(section.data); break;
            case 'background': this.parseBackground(section.data); break;
            case 'buttons': this.parseButtons(section.data); break;
        }
    }

    parseAnswer(str) {
        this.answer = str;
    }

    parseBackground(str) {
        this.background = str;
    }

    parseWidth(str) {
        const width = this.parseInt(str);
        if (width > 0) {
            this.width = width;
        }
    }

    parseType(str) {   
        str = str.toLowerCase();
        this.type = this.VALID_TYPES.indexOf(str) >= 0 ? str : null;
    }

    parseButtons(str) {
        const BUTTONS = [
            'frac', // fraction
            'sqr', // squared 
            'exp', // exponent 
            'sub', // subscript
        
            'sqrt', // squareRoot 
            'cbrt', // cubeRoot
            'nrt', // nthRoot 
            'abs', // absoluteValue
        
            'gt', // greaterThan
            'lt', // lessThan
            'gte', // greaterThanOrEqual
            'lte', // lessThanOrEqual
        
            'ne', // notEqual 
            'pm', // plusMinus 
            'times', // times
            'cdot', // dot-times            
            'div', // divide            
        
            'cup', // union
            'cap', // intersection 
            'null', // nullSet
            'infty', // infty
        
            'and', 
            'or', 
        
            'e', // eulersNumber
            'pi', 
        
            'sin', 
            'cos', 
            'tan', 
            'csc', 
            'sec', 
            'cot', 
        
            'asin', // arcsin
            'acos', // arccos
            'atan', // arctan
            'acsc', // arccsc
            'asec', // arcsec
            'acot', // arccot
        
            'ln', 
            'log', 
            'logb', 
        
            'alpha',
            'beta', 
            'gamma', 
            'theta', 
            'phi'
        ];        

        const buttons = str.split(',');

        for(let i = 0; i < buttons.length; i++) {
            buttons[i] = buttons[i].trim().toLowerCase();
        }

        const orderedButtons = [];
        for(const button of BUTTONS) {
            if (buttons.indexOf(button) >= 0) {
                orderedButtons.push(button);
            }
        }

        this.buttons = orderedButtons;
    }
}