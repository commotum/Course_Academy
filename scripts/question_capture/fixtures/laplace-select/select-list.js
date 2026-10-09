class SelectList {
    constructor(parent, containerId, questionId, config) {
        this.containerId = containerId;
        this.questionId = questionId;
        this.index = config.index;
        this.id = 'S' + this.index;
        this.config = config;

        this.correctOption = config.correctOption;

        this.sectionIndex = config.sectionIndex;
        this.locked = false;
        this.selectedOption = null;

        this.element = document.createElement('div');
        this.element.id = this.id;
        this.element.className = 'selectList';
        this.element.style.marginLeft = this.config.margin.left + 'px';
        this.element.style.marginRight = this.config.margin.right + 'px';
        this.element.style.marginTop = this.config.margin.top + 'px';
        this.element.style.marginBottom = this.config.margin.bottom + 'px';
        parent.appendChild(this.element);

        this.frame = document.createElement('div');
        this.frame.className = 'selectListFrame';
        this.frame.innerHTML = '&nbsp;';
        this.frame.onmousedown = (event) => {
            if (!this.locked) {
                this.showOptions();
            }
        };
        
        this.element.appendChild(this.frame);       

        let selectedText = document.createElement('span');
        selectedText.className = 'selectListSelectedText';
        this.frame.appendChild(selectedText);

        this.optionsDiv = document.createElement('div');
        this.optionsDiv.className = 'selectListOptions';
        this.element.appendChild(this.optionsDiv);

        this.options = [];

        for(let i = 0; i < config.options.length; i++) {
            let opt = config.options[i];

            let option = document.createElement('div');
            option.index = i;
            option.className = 'selectListOption';

            option.onmousedown = this.onMouseDownOption.bind(this);
            this.optionsDiv.appendChild(option);

            this.options.push(option);

            if (config.context === 'mathJax') {
                option.innerHTML = '$' + opt + '$';
            } else if (config.context === 'code') {
                option.innerHTML = `<span class="code">${opt}</span>`;
            } else if (this.containsCode(opt)) {
                option.innerHTML = this.formatCode(opt);
            } else {
                option.innerHTML = opt;
            }
        }

        window.addEventListener('mousedown', (event) => {
            if (event.target !== this.element && event.target !== this.frame) {
                this.hideOptions();
            }
        });  

        window.addEventListener('resize', (event) => {
            this.hideOptions();
        });  

        this.attachFrameEventHandlers();
    }

    containsCode(src) {
        let numBackTicks = 0;

        for(let i = 0; i < src.length; i++) {
            if (src[i] === '`') {
                numBackTicks++;
            }
        }

        return numBackTicks > 0 && numBackTicks % 2 === 0;
    }

    formatCode(src) {
        let output = '';
        let opening = true;
        for(let i = 0; i < src.length; i++) {
            const char = src[i];
            if (char === '`') {
                if (opening) {
                    output += '<span class="code">';
                    opening = false;
                } else {
                    output += '</span>';
                    opening = true;
                }                
            } else {
                output += char;
            }
        }
        return output;
    }

    init() {        
        this.id = 'selectList-' + this.questionId + '-' + this.index;
        this.frameId = 'selectListFrame-' + this.questionId + '-' + this.index;
        this.element.id = this.id;
        this.frame.id = this.frameId;

        let optionDivs = this.element.querySelectorAll('.selectListOption');
        for(let optionDiv of optionDivs) {
            optionDiv.onmousedown = this.onMouseDownOption.bind(this);
        }

        if (this.config.correct === true || this.config.correct === 1) {
            let multipleAttempts = this.config.answers && this.config.answers.length > 1;            
            this.setCorrect(multipleAttempts);
        } else if (this.config.correct === false || this.config.correct === 0) {
            this.setIncorrect();
        }

        if (this.config.disabled) {
            this.disable();
        }

        if (this.config.selectedIndex >= 0) {
            this.selectOption(this.config.selectedIndex);
        }     
        
        this.attchedScrollEventHandlers();
    }

    update(data) {
        this.frame = $(this.frameId);
        this.attachFrameEventHandlers();

        this.config = Object.assign(this.config, data);

        if (this.config.correct === true || this.config.correct === 1) {
            let multipleAttempts = this.config.answers && this.config.answers.length > 1;            
            this.setCorrect(multipleAttempts);
        } else if (this.config.correct === false || this.config.correct === 0) {
            this.setIncorrect();
        }

        if (this.config.disabled) {
            this.disable();
        }  
    }

    onSelect(selectList) {}

    attachFrameEventHandlers() {
        this.frame.onmouseover = (event) => {
            if (this.locked) {
                this.showTooltip();
            }
        };

        this.frame.onmouseout = (event) => {
            if (this.locked && this.tooltip) {
                this.tooltip.hide();
                delete this.tooltip;
            }
        };
    }

    attchedScrollEventHandlers() {
        this.scrollableAncestor = this.findScrollableParent();

        if (this.scrollableAncestor) {
            this.scrollableAncestor.addEventListener('scroll', (event) => {
                this.hideOptions();
            }, false);
        }              
            
        window.addEventListener('scroll', (event) => {
            this.hideOptions();
        }); 
    }

    findScrollableParent() {
        let ancestor = this.element.parentElement;

        while (ancestor) {
            let cssObj = window.getComputedStyle(ancestor, null);
            let overflow = cssObj.getPropertyValue("overflow");
            let overflowY = cssObj.getPropertyValue("overflow-y");

            if (overflow === 'auto' || overflowY === 'auto') {
                return ancestor;
            }

            ancestor = ancestor.parentElement;
        }

        return null;
    }

    showTooltip() {
        if (!this.locked) { return; }

        let text = this.getTootipText();
        if (!text) { return; }

        this.tooltip = new Core2.Tooltip(this.frame, text);
    }

    getTootipText() {
        if (this.config.answers) {
            // Dynamic-select or Proof
            if (this.config.answers.length) {
                if (this.config.correct) {
                    if (this.config.answers.length === 1) {
                        return 'Correct on first attempt';
                    } else if (this.config.answers.length === 2) {
                        return `Correct on second attempt`;
                    } else if (this.config.answers.length === 3) {
                        return `Correct on third attempt`;
                    } else if (this.config.answers.length === 4) {
                        return `Correct on fourth attempt`;
                    }
                } else {
                    if (this.config.answers.length === 1) {
                        return 'Incorrect';
                    } else if (this.config.answers.length === 2) {
                        return `Incorrect after two attempts`;
                    } else if (this.config.answers.length === 3) {
                        return `Incorrect after three attempts`;
                    } else if (this.config.answers.length === 4) {
                        return `Incorrect after four attempts`;
                    }
                }
            } else {
                return '';
            }
        } else {
            // Static-select

            if (this.config.correct) {
                return 'Correct';
            } else {
                return `Incorrect`;
            }
        }

        return '';
    }

    getPlaceholder() {
        let placeholder;

        if (this.config.context === 'mathJax') {
            let content = this.config.options[this.placeholderIndex];

            //placeholder = `\\left(${content}\\right)^{(S${this.index})}`;

            placeholder = `\\left\\{\\left(${content}\\right)_{(S${this.index})}\\right\\}`;

        } else {
            placeholder = `S${this.index}`;
        }

        return placeholder;
    }

    getSelectedIndex() {
        if (!this.selectedOption) { return -1; }
        return this.selectedOption.index;
    }

    getValue() {
        if (this.selectedOption) { return null; }

        let index = this.selectedOption.index;

        return this.config.options[index];
    }

    setValue(value) {

    }

    enable() {
        this.locked = false;
        this.frame.className = 'selectListFrame';
    }

    disable() {
        this.locked = true;

        if (this.correct === undefined) {
            this.frame.className = 'selectListFrameDisabled';
        }
    }

    setCorrect(multipleAttempts) {
        this.frame.classList.remove('incorrectSelection');

        if (multipleAttempts) {
            this.frame.classList.add('correctSelectionMultipleAttempts');
        } else {
            this.frame.classList.add('correctSelection');
        }

        this.hideOptions();

        this.correct = true;
        this.locked = true;        
    }

    setIncorrect() {

        this.frame.classList.remove('correctSelection');
        this.frame.classList.add('incorrectSelection');

        this.hideOptions();

        this.correct = false;
        this.locked = true;   
    }

    resize() {
        this.initFrameWidth();  
        this.initFrameHeight();
    }

    reset() {
        this.frame.classList.remove('correctSelection');
        this.frame.classList.remove('incorrectSelection');
        this.frame.innerHTML = '';

        if (this.selectedOption) {
            this.selectedOption.classList.remove('selected');
        }

        this.correct = false;
        this.locked = false;
        this.selectedOption = null;
    }

    showOptions(event) {
        document.body.appendChild(this.optionsDiv);
        this.optionsDiv.style.visibility = 'visible';   
        this.optionsDiv.style.zIndex = 1000;          
        
        const left = Core.findLeft(this.frame); 
        const frameTop = Core.findTop(this.frame); 
        const frameHeight = Core.getHeight(this.frame);

        const scrollTop = this.scrollableAncestor ? this.scrollableAncestor.scrollTop : 0;
        const top = frameTop + frameHeight + 1 - scrollTop;
        
        this.optionsDiv.style.left = left + 'px';
        this.optionsDiv.style.top = top + 'px';        
    }
    
    hideOptions() {
        this.optionsDiv.style.visibility = 'hidden';
        this.optionsDiv.style.zIndex = 1;        
        this.element.appendChild(this.optionsDiv);
    }

    onMouseDownOption(event) {
        let option = this.findEventSource(event, 'selectListOption');

        if (option === this.selectedOption) { return; }

        if (this.selectedOption) {
            this.selectedOption.classList.remove('selected');
        }

        option.classList.add('selected');

        this.frame.innerHTML = option.innerHTML;

        this.optionsDiv.style.visibility = 'hidden';

        this.selectedOption = option;

        this.onSelect(this);
    }

    selectOption(index) {
        let option = this.options[index];
        this.selectedOption = option;

        if (option) {
            this.frame.innerHTML = this.selectedOption.innerHTML;
        }
    }

    findEventSource(evt, className) {
        let target = evt.target;

        while (!target.classList.contains(className)) {
            target = target.parentNode;
        }
        return target;
    }

    initFrameWidth() {
        let width = this.optionsDiv.offsetWidth - 16;
        this.frame.style.width = width + 'px';
    }

    initFrameHeight() {
        let divs = this.optionsDiv.querySelectorAll('.selectListOption');

        let maxHeight = 0;
        this.placeholderIndex = 0;

        for(let i = 0; i < divs.length; i++) {
            let div = divs[i];
            let height = div.offsetHeight - 8;

            if (height > maxHeight) {
                maxHeight = height;
                this.placeholderIndex = i;
            }
        }

        this.frame.style.height = maxHeight + 'px';
        this.frame.style.lineHeight = maxHeight + 'px';

        for(let div of divs) {
            div.style.height = maxHeight + 'px';
        }
    }
}