const OPERATIONS = {
    frac: { latex: "\\frac{}{}", moveTo: "Up", moveFor: 1 },  
    /*sqr: { latex: "\\{}^{2}", moveTo: "Left", moveFor: 1  }, */
    exp: { latex: "\\^{}", moveTo: "Up", moveFor: 1 },  
    sub: { latex: "\\_{}", moveTo: "Down", moveFor: 1 }, 

    sqrt: { latex: "\\sqrt{}", moveTo: "Left", moveFor: 1 }, 
    cbrt: { latex: "\\sqrt[3]{}", moveTo: "Left", moveFor: 1 }, 
    nrt: { latex: "\\sqrt[{}]{}", moveTo: "Left", moveFor: 2 },
    abs: { latex: "\\left|{}\\right|", moveTo: "Left", moveFor: 1 },  

    gte: { latex: "\\geq" }, 
    lte: { latex: "\\leq" }, 
    gt: { latex: "\\gt" }, 
    lt: { latex: "\\lt" },  
    ne: { latex: "\\neq" }, 
    pm: { latex: "\\pm" },  

    cup: { latex: "\\cup" },
    cap: { latex: "\\cap" },
    null: { latex: "\\emptyset" },
    infty: { latex: "\\infty" },

    and: { latex: "\\land" },
    or: { latex: "\\lor" },

    pi: { latex: "\\pi" }, 
    e: { latex: "e" }, 

    alpha: { latex: "\\alpha" },
    beta: { latex: "\\beta" },
    gamma: { latex: "\\gamma" },
    theta: { latex: "\\theta" },
    phi: { latex: "\\phi" },         
    lambda: { latex: "\\lambda" }, 

    sin: { latex: "\\sin\\left({}\\right)", moveTo: "Left", moveFor: 1 },     
    cos: { latex: "\\cos\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    tan: { latex: "\\tan\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    sec: { latex: "\\sec\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    csc: { latex: "\\csc\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    cot: { latex: "\\cot\\left({}\\right)", moveTo: "Left", moveFor: 1 },      

    asin: { latex: "\\sin^{-1}\\left({}\\right)", moveTo: "Left", moveFor: 1 },     
    acos: { latex: "\\cos^{-1}\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    atan: { latex: "\\tan^{-1}\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    asec: { latex: "\\sec^{-1}\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    acsc: { latex: "\\csc^{-1}\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    acot: { latex: "\\cot^{-1}\\left({}\\right)", moveTo: "Left", moveFor: 1 },     

    sinh: { latex: "\\sinh\\left({}\\right)", moveTo: "Left", moveFor: 1 },     
    cosh: { latex: "\\cosh\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    tanh: { latex: "\\tanh\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    sech: { latex: "\\text{sech}\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    csch: { latex: "\\text{csch}\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    coth: { latex: "\\coth\\left({}\\right)", moveTo: "Left", moveFor: 1 },       

    ln: { latex: "\\ln\\left({}\\right)", moveTo: "Left", moveFor: 1 },  
    log: { latex: "\\log\\left({}\\right)", moveTo: "Left", moveFor: 1 }, 
    logb: { latex: "\\log_{}\\left({}\\right)" },  

    times: { latex: "\\times" }, 
    cdot: { latex: "\\cdot" },     
    div: { latex: "\\div" }, 
    degree: { latex: "\\degree" }, 
    parens: { latex: "\\left(\\right)", moveTo: "Left", moveFor: 1 }
       
};

class MathEditor {
    constructor(answerFrame, operationNames = []) {
        this.answerFrame = answerFrame;
        this.operationNames = operationNames;

        this.mathQuill = MathQuill.getInterface(2);

        let config = {
            handlers: {
              edit: function() {},
              enter: function() {}
            }
        };

        this.latex = '';

        this.answerFrame.className = 'matheditor-wrapper-answer';

        this.answerDiv = document.createElement('div');
        this.answerDiv.style.border = 'none';
        this.answerDiv.style.outline = 'none';
        this.answerFrame.appendChild(this.answerDiv);

        this.mathField = this.mathQuill.MathField(this.answerDiv, config);
        this.textarea = this.answerDiv.querySelector('textarea');

        this.textarea.onfocus = (evt) => {
            //console.log('onFocus');

            //console.log(this.answerDiv.innerHTML);
            this.printStyles(this.answerDiv);

            this.showToolbox();

            let latex = this.getLatex(true);

            //console.log('onblur: latex: ' + latex);

            this.onFocus(this, latex);
        };

        this.textarea.onblur = (evt) => {
            //console.log('onblur: this.inserting=' + this.inserting);
            
            if (this.inserting === false) {
                this.hideToolbox();
                //console.log('onBlur');                
            }

            let latex = this.getLatex(true);

            //console.log('onblur: latex: ' + latex);

            this.onBlur(latex);
        };     

        this.answerFrame.onmousedown = (evt) => {
            this.textarea.focus();
            evt.stopPropagation();
            evt.preventDefault();
        };

        this.createToolbox();




        this.inserting = false;



        setTimeout(this.checkForChange.bind(this), 500);
    }

    setEnabled(enabled) {
        this.textarea.disabled = !enabled;

        let cursor = this.answerDiv.querySelector('.mq-cursor');
        if (cursor) {
            cursor.style.visibility = 'hidden';
        }

        this.hideToolbox();
    }

    onChange(latex) {
        // Callback
    }

    onFocus(mathEditor, latex) {
        // Callback
    }

    onBlur(latex) {
        // Callback
    }

    checkForChange(evt) {
        let latex = this.getLatex();

        if (latex !== this.latex) {
            //console.log('MathEditor: ' + latex);

            if (!this.isValidLatex(latex)) {                
                this.setLatex(this.latex);
            } else {
                let cleanLatex = this.cleanLatex(latex);

                this.onChange(cleanLatex);

                this.latex = latex;
            }
        }

        setTimeout(this.checkForChange.bind(this), 200);
    }

    isValidLatex(latex) {
        if (!this.isValidExponent(latex)) { return false; }
        if (!this.isValidSubscript(latex)) { return false; }

        return true;
    }

    isValidExponent(latex) {
        // Check that we don't have two exponent operators in succession
        if (latex.indexOf('^{^') !== -1) { return false; }

        // Check that we don't have a space before the exponent 
        if (latex.indexOf('^{\\ ') !== -1) { return false; }

        // Check that we don't have an exponent at the first position
        if (latex.indexOf('^') === 0 ) { return false; }

        // Check that we don't have a space before the exponent operator
        if (latex.indexOf(' ^') !== -1) { return false; }

        return true;
    }

    isValidSubscript(latex) {
        // Check that we don't have two subscript operators in succession
        if (latex.indexOf('_{_') !== -1) { return false; }

        // Check that we don't have a space before the subscript 
        if (latex.indexOf('_{\\ ') !== -1) { return false; }

        // Check that we don't have an subscript at the first position
        if (latex.indexOf('_') === 0 ) { return false; }

        // Check that we don't have a space before the subscript operator
        if (latex.indexOf(' _') !== -1) { return false; }

        return true;
    }    

    cleanLatex(latex) {
        let cleanLatex = this.replaceAltMinusSign(latex);
        cleanLatex = this.stripEscapedSpaces(cleanLatex);       
        
        return cleanLatex;
    }

    replaceAltMinusSign(latex) {
        for(let i = 0; i < latex.length; i++) {
            let charCode = latex.charCodeAt(i);

            if (charCode === 727 || charCode === 8722) {
                latex = latex.substring(0, i) + '-' + latex.substring(i + 1);
            }
        }

        return latex;
    }

    stripEscapedSpaces(latex) {
        let chars = [];
        let prevCode;
        for(let char of latex) {
            let code =  char.charCodeAt(0);
            //console.log('char=' + char + ', code=' + code);

            if (code === 32 && prevCode === 92) {
                chars[chars.length - 1] = char;
            } else {
                chars.push(char);      
            }
            
            prevCode = code;
        }

        let clean = chars.join('');

        return clean;
    }
     
    printStyles(element) {
        //console.log('id=' + element.id + ', class=' + element.className);

        var css = window.getComputedStyle(element);
        for (var i = 0; i < css.length; i++) {
            let styleName = '' + css[i];
            if (styleName === 'border-color' || styleName === 'box-shadow') {
                //console.log('    ' + styleName + '=' + css.getPropertyValue(styleName));
            }
        }

        for(let child of element.children) {
            this.printStyles(child);
        }
    }

    createToolbox() {
        if (this.operationNames.length > 0) {
            this.toolbox = document.createElement('div');
            this.toolbox.id = 'mathEditorToolbox';

            this.toolbox.style.position = 'absolute';      
            document.body.appendChild(this.toolbox);      
            
            for(let operationName of this.operationNames) {
                this.createToolboxButton(operationName);
            }
        }

        this.hideToolbox();
    }
                    
    createToolboxButton(operationName) {
        let button = document.createElement('div');
        button.className = `mathIcon ${operationName}Icon`;
        this.toolbox.appendChild(button);

        button.onmousedown = (evt) => {
            this.inserting = true;

            clearTimeout(this.blurTimer);
        }

        button.onclick = (evt) => {
            //console.log('button.onclick: ' + operationName);

            clearTimeout(this.blurTimer);

            let operation = OPERATIONS[operationName];

            if (operation) {
                this.insertOperation(operation);
            }
        }

        this.toolbox.appendChild(button);
    }

    showToolbox() {
        if (this.toolbox) {
            let answerLeft = this.findLeft(this.answerFrame);
            let answerTop = this.findTop(this.answerFrame);
            let answerHeight = Core.getHeight(this.answerFrame);

            let left = answerLeft;
            let top = answerTop + answerHeight + 10;

            let scrollYOffset = window.pageYOffset;

            top += scrollYOffset;

            this.toolbox.style.left = left + 'px';
            this.toolbox.style.top = top + 'px';
            this.toolbox.style.zIndex = 1000;

            this.toolbox.style.visibility = 'visible';            
        }
    }

    findLeft(element) {
        return element.getBoundingClientRect().left + document.body.scrollLeft;
    }

    findTop(element) {
        return element.getBoundingClientRect().top + document.body.scrollTop;    
    }

    hideToolbox() {
        if (this.toolbox) {
            setTimeout(evt => {
                this.toolbox.style.visibility = 'hidden';

                let latex = this.getLatex();
                //console.log(latex);

            }, 100);
        }
    }

    getLatex(clean) {
        let latex = this.mathField.latex();

        if (clean) {
            latex = this.cleanLatex(latex);
        }
        return latex;
    }
    
    setLatex(latex, eventsEnabled = true) {
        if (!eventsEnabled) {
            this.latex = latex;
        }
        this.mathField.latex(latex);              
    }    

    insertOperation(operation) {
        this.inserting = true;

        //console.log(operation.latex);

        this.mathField.write(operation.latex);
        this.mathField.focus();

        for(let i = 0; i < operation.moveFor; i++) {
            this.mathField.keystroke(operation.moveTo);
        }

        setTimeout((evt) => {
            this.inserting = false;
        }, 100);
    }
}