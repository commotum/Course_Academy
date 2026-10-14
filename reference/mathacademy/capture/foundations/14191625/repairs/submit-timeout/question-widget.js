class QuestionWidget {
    constructor(element, question, config = {}) {
        this.element = element;
        this.question = question;
        this.config = config;

        this.element.classList.add('questionWidget')
        this.element.style.display = 'none';

        this.active = true;
        this.answerSubmitted = false;       

        // Reskin from your own brand tokens.
        CalcWidget.registerSkin('edu-square', {
            'title-font': '"Trebuchet MS", sans-serif',
            'title-size': '15px',
            'key-font': '"Trebuchet MS", sans-serif',
            'key-size': '20px',
            'num-weight': 100
        });
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Events

    onSubmitEnabled(event) {}
    onSubmitAnswer(event) {}
    onComplete(event) {}

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Virtual methods to be overridden by subclasses
    
    renderBody() {}
    renderHealth() {}
    renderGrading(grading) {}
    async update(response) {}
    reset() {}
    disable() {}
    enable() {}
    getStudentAnswer() {}

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    activate() {
        this.active = true;
    }

    deactivate() {
        this.active = false;
    }

    async show() {        
        if (!this.rendered) {
            await this.renderQuestion(); 

            if (this.question.answer) {
                this.renderResult();
                this.renderExplanation();
            } else {
                this.renderButtonBar();
                this.renderSpinner();
                this.enable();
            }
        }

        this.element.style.display = 'block';
    }  

    hide() {
        this.element.style.display = 'none';
    }

    async showAnswer() {
        this.buttonBar.style.display = 'none';

        if (this.explanationDiv) {
            this.explanationDiv.style.display = 'block';
        } else {
            this.renderResult();
            await this.renderExplanation();
    
            window.scrollTo(0, document.body.scrollHeight); 
        }
    }

    async renderQuestion() {
        this.element.innerHTML = '';

        this.renderHeader();
        this.renderCalculatorInstructions();
        this.renderGraphic();
        this.renderText();
        await this.renderBody();
        this.renderHealth();

        await renderLatex([this.element]);       

        this.rendered = true;
    }

    renderHeader() {
        this.header = Core.createDiv(this.element, null, 'questionWidget-header');     
        
        this.titleDiv = Core.createDiv(this.header, null, 'questionWidget-title', 'Question ' + this.question.number);            
        
        this.createCalculatorIcon();

        this.helpButton = Core.createDiv(this.header, null, 'questionWidget-helpButton', '?');  

        this.helpButton.onmouseover = this.showHelpMenu.bind(this);
    }

    createCalculatorIcon() {
        if (this.question.group.calculator === 'None') { return; }

        this.calculatorIcon = Core.createDiv(this.header, null, 'questionWidget-calculatorIcon');
        this.calculatorIcon.innerHTML = this.getCalculatorSvg();
        this.calculatorIcon.onmousedown = this.showCalculator.bind(this);       

        this.calculatorIcon.onmouseover = (event) => {
            const tooltipText = this.question.group.calculator + ' calculator';

            this.calculatorIcon.tooltip = new Core2.Tooltip(this.calculatorIcon, tooltipText);    
        };

        this.calculatorIcon.onmouseout = (event) => {
            if  (this.calculatorIcon.tooltip) {
                this.calculatorIcon.tooltip.hide();
                delete this.calculatorIcon.tooltip;
            }
        };
    }

    showCalculator() {
        switch (this.question.group.calculator) {
            case 'Standard':
                if (!this.standardCalculator) {
                    this.standardCalculator = new CalcWidget({
                        trigger: '#open-calc',
                        skin: 'edu-square', 
                        density: 'compact',
                        mode: 'basic',
                        title: 'Calculator'
                    }); 
                }
                if (!this.standardCalculator.isOpen) {
                    this.standardCalculator.open();   
                }
                break;
            case 'Scientific':
                if (!this.scientificCalculator) {
                    this.scientificCalculator = new CalcWidget({
                        trigger: '#open-calc',
                        skin: 'edu-square', 
                        density: 'compact',
                        mode: 'scientific',
                        title: 'Calculator'
                    }); 
                }
                if (!this.scientificCalculator.isOpen) {
                    this.scientificCalculator.open();   
                }
                break;
            case 'Graphing':        
                if (!this.graphingCalculator) {
                    this.graphingCalculator = new CalcWidget({
                        trigger: '#open-calc',
                        skin: 'edu-square', 
                        density: 'compact',
                        mode: 'graphing',
                        title: 'Calculator'
                    }); 
                }
                if (!this.graphingCalculator.isOpen) {
                    this.graphingCalculator.open();   
                }            
                break;
        } 
    }

    showHelpMenu(evt) {
        let helpMenu = new HelpMenu(this.helpButton, {
            taskType: this.config.taskType,
            taskId: this.config.taskId,
            topicId: this.config.topicId,
            type: 'question',
            id: this.question.id,
            topOffset: -100
        });
        helpMenu.show();
    }

    renderCalculatorIcon() {
        //const goldThunderbolt = Core.createImg(timeElapsedDiv, null, 'questionWidget-timeElapsedIcon', '/img/thunderbolt-gold.svg');

        //let icon = Core.createImg(this.header, null, 'questionWidget-calculatorIcon', '/img/calculator-1.svg');

        let div = Core.createDiv(this.header, null, 'questionWidget-calculatorIcon');
        div.innerHTML = this.getCalculatorSvg();
    }    

    getCalculatorSvg() {
        return `<svg enable-background="new 0 0 128 128" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg"><g><path d="m102.11.5h-76.22c-5.75 0-10.43 4.68-10.43 10.43v106.14c0 5.75 4.68 10.43 10.43 10.43h76.22c5.75 0 10.43-4.68 10.43-10.43v-106.14c0-5.75-4.68-10.43-10.43-10.43zm6.43 116.57c0 3.55-2.88 6.43-6.43 6.43h-76.22c-3.55 0-6.43-2.88-6.43-6.43v-106.14c0-3.55 2.88-6.43 6.43-6.43h76.22c3.55 0 6.43 2.88 6.43 6.43z"/><path d="m93.96 12.83h-59.92c-2.76 0-5 2.24-5 5v16.57c0 2.76 2.24 5 5 5h59.92c2.76 0 5-2.24 5-5v-16.57c0-2.76-2.25-5-5-5zm1 21.57c0 .55-.45 1-1 1h-59.92c-.55 0-1-.45-1-1v-16.57c0-.55.45-1 1-1h59.92c.55 0 1 .45 1 1z"/><path d="m43.86 45.14h-9.82c-2.76 0-5 2.24-5 5v9.82c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-9.82c0-2.76-2.24-5-5-5zm1 14.82c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-9.82c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/><path d="m68.91 45.14h-9.82c-2.76 0-5 2.24-5 5v9.82c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-9.82c0-2.76-2.24-5-5-5zm1 14.82c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-9.82c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/><path d="m93.96 45.14h-9.82c-2.76 0-5 2.24-5 5v9.82c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-9.82c0-2.76-2.25-5-5-5zm1 14.82c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-9.82c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/><path d="m43.86 70.7h-9.82c-2.76 0-5 2.24-5 5v9.82c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-9.82c0-2.76-2.24-5-5-5zm1 14.82c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-9.82c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/><path d="m68.91 70.7h-9.82c-2.76 0-5 2.24-5 5v9.82c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-9.82c0-2.76-2.24-5-5-5zm1 14.82c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-9.82c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/><path d="m43.86 96.26h-9.82c-2.76 0-5 2.24-5 5v9.82c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-9.82c0-2.76-2.24-5-5-5zm1 14.82c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-9.82c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/><path d="m68.91 96.26h-9.82c-2.76 0-5 2.24-5 5v9.82c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-9.82c0-2.76-2.24-5-5-5zm1 14.82c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-9.82c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/><path d="m93.96 70.7h-9.82c-2.76 0-5 2.24-5 5v35.38c0 2.76 2.24 5 5 5h9.82c2.76 0 5-2.24 5-5v-35.38c0-2.76-2.25-5-5-5zm1 40.38c0 .55-.45 1-1 1h-9.82c-.55 0-1-.45-1-1v-35.38c0-.55.45-1 1-1h9.82c.55 0 1 .45 1 1z"/></g></svg>`;
    }

    renderCalculatorInstructions() {
        switch (this.question.group.calculator) {
            case 'Graphing': 
                Core.createDiv(this.element, null, 'questionWidget-calculatorInstructions', `A graphing calculator is required to answer this question.`);               
                break;
        }
    }

    renderGraphic() {
        if (this.question.graphic) {
            Core.createDiv(this.element, null, 'questionWidget-graphic', `<img src="/graphics/q-${this.question.id}"/>`);
        }
    }

    getRenderedField(field, mathdownType) {
        let value = this.question[field];
        if (!this.question.rendered) {
            value = mathdown.process(value, mathdownType);
        }
        return value;
    }

    renderText() {
        const questionText = this.getRenderedField('text', true);
        this.textDiv = Core.createDiv(this.element, null, 'questionWidget-text', questionText);
    }

    renderButtonBar() {
        if (!this.config.submitButton) { return; }

        this.buttonBar = Core.createDiv(this.element, null, 'questionWidget-buttonBar');      

        if (this.config.skipButton) {
            this.skipButton = Core.createDiv(this.buttonBar, null, 'questionWidget-skipButton', 'Don\'t Know');    

            if (this.skipButton) {
                this.skipButton.onmousedown = this.onMouseDownSkipButton.bind(this);
            }            
        }

        this.submitButton = Core.createDiv(this.buttonBar, null, 'questionWidget-submitButton disabledButton', 'Submit');     
        this.submitButton.onmousedown = this.onMouseDownSubmitButton.bind(this);

        this.disableSubmitButton();
    }

    renderSpinner() {
        this.spinnerFrame = Core.createDiv(this.element, null, 'questionWidget-spinnerFrame');  
        this.spinner = Core.createDiv(this.spinnerFrame, null, 'questionWidget-spinner');  
    }

    renderResult(skipped) {
        if (this.resultDiv) { return; }

        this.resultDiv = Core.createDiv(this.element, null, 'questionWidget-result');  

        const answer = this.question.answer;

        if (answer.correct) {
            Core.createDiv(this.resultDiv, null, 'questionWidget-correctIncorrectIcon', '<img src="/img/correct-answer.svg"/>');            
            Core.createDiv(this.resultDiv, null, 'questionWidget-correctText', 'Correct');

            if (answer.speedBonusAvailable) {
                this.renderTimeElapsed();            
            }
        } else {      
            Core.createDiv(this.resultDiv, null, 'questionWidget-incorrectIcon', '<img src="/img/incorrect-answer.svg"/>');                        

            if (skipped) {
                Core.createDiv(this.resultDiv, null, 'questionWidget-incorrectText', 'Skipped Question');
            } else {
                Core.createDiv(this.resultDiv, null, 'questionWidget-incorrectText', 'Incorrect');
            }
        }        
    }

    renderTimeElapsed() {
        const timeElpasedStr = this.formatTimeElapsed(this.question.answer.timeElapsed);

        const timeElapsedDiv = Core.createDiv(this.resultDiv, null, 'questionWidget-timeElapsed');
        const timeElapsedText = Core.createSpan(timeElapsedDiv, null, 'questionWidget-timeElapsedText');        

        Core.createSpan(timeElapsedText, null, 'questionWidget-timeElapsedLabel', 'Elapsed: ');
        Core.createSpan(timeElapsedText, null, 'questionWidget-timeElapsedSeconds', timeElpasedStr);      
        
        if (this.question.answer.speedBonus) {
            const goldThunderbolt = Core.createImg(timeElapsedDiv, null, 'questionWidget-timeElapsedIcon', '/img/thunderbolt-gold.svg');

            goldThunderbolt.onmouseover = this.onMouseOverGoldThunderbold.bind(this);
            goldThunderbolt.onmouseout = this.onMouseOutGoldThunderbold.bind(this);            
        } else {
            const greyThunderbolt = Core.createImg(timeElapsedDiv, null, 'questionWidget-timeElapsedIcon', '/img/thunderbolt-grey.svg');

            greyThunderbolt.onmouseover = this.onMouseOverGreyThunderbold.bind(this);
            greyThunderbolt.onmouseout = this.onMouseOutGreyThunderbold.bind(this);               
        }
    }

    onMouseOverGoldThunderbold(event) {
        const target = event.currentTarget;
        const timeLimitSeconds = (this.question.answer.speedBonusTimeLimit / 1000).toFixed(0);

        this.tooltip = new Core2.Tooltip(target, `You earned an XP speed bonus! The speed bonus time limit for this question is ${timeLimitSeconds} seconds.`);
    }

    onMouseOutGoldThunderbold(event) {
        if (this.tooltip) {
            this.tooltip.hide();
            this.tooltip = null;
        }
    } 

    onMouseOverGreyThunderbold(event) {
        const target = event.currentTarget;
        const timeLimitSeconds = (this.question.answer.speedBonusTimeLimit / 1000).toFixed(0);

        this.tooltip = new Core2.Tooltip(target, `Sorry, you didn't earn an XP speed bonus. The speed bonus time limit for this question is ${timeLimitSeconds} seconds.`);
    }

    onMouseOutGreyThunderbold(event) {
        if (this.tooltip) {
            this.tooltip.hide();
            this.tooltip = null;
        }
    } 

    formatTimeElapsed(totalMilliseconds) {
        const totalSeconds = Math.round(totalMilliseconds / 1000).toFixed(0);

        return totalSeconds === 1 ? '1 second' : totalSeconds +  ' seconds';
    }

    async renderExplanation() {
        if (this.explanationDiv) { return; }

        let explanationHeader = Core.createDiv(this.element, null, 'questionWidget-explanationHeader', 'EXPLANATION');  
        const explanationText = this.getRenderedField('explanation');
        this.explanationDiv = Core.createDiv(this.element, null, 'questionWidget-explanation', explanationText);

        await renderLatex([this.explanationDiv]);     
    }  

    enableSubmitButton() {
        if (this.submitButton) {
            this.submitButton.className = 'questionWidget-submitButton enabledButton';
            this.submitButton.disabled = false;
        }
        this.onSubmitEnabled({ questionId: this.question.id });
    }

    disableSubmitButton() {
        if (this.submitButton) {
            this.submitButton.className = 'questionWidget-submitButton disabledButton';        
            this.submitButton.disabled = true;
        }
    }    

    async onMouseDownSkipButton(event) {
        TaskEvent.post('question', 'onDontKnow', this.question.id);

        Core.killEvent(event);       
        this.reset()             
        this.submitAnswer(true);
    }

    async onMouseDownSubmitButton(event) {   
        Core.killEvent(event);
        if (this.submitButton.disabled) { return; }         
        await this.submitAnswer();
    }
    
    async submitAnswer(skipped = false) {               
        this.answerSubmitted = true;   
        this.disable();

        this.disableSubmitButton();

        this.onSubmitAnswer({ question: this.question });     

        this.spinner.style.display = 'block';

        let studentAnswer = this.getStudentAnswer();

        let requested = new Date();

        let response = await this._submitAnswer(studentAnswer);

        if (!response) {
            alert("There is currently no Internet connection.");
            this.answerSubmitted = false;
            this.enable();
            this.enableSubmitButton();
            return;
        }

        if (response.taskLocked) {
            let messageBox = new MessageBox('Under Maintenance', `This topic is currently under maintenance and will be available again shortly.`);
            await messageBox.showSync();

            window.location.href = '/learn';
            return;
        } else if (response.reload) {
            let messageBox = new MessageBox('Reload Required', `Something has changed that requires the page to reload.`);
            await messageBox.showSync();

            window.location.reload();
            return;
        } else if (response.error) {
            this.answerSubmitted = false;
            this.enable();
            this.enableSubmitButton();
            return;
        }

        let requestReceived = new Date();
        let requestTime = requestReceived - requested;
        let processingTime = response.processingTime;


        let rendered = new Date();
        let renderTime = rendered - requestReceived;

        APISync.submitRequestProfile({
            page: this.config.taskType,
            answerId: null, 
            requestTime, 
            renderTime, 
            processingTime
        });

        await this.update(response);

        if (response.question.answer) {
            this.question.health = response.question.health;
            this.question.answer = response.question.answer;            
            this.question.explanation = response.question.explanation;

            if (this.skipButton) {
                this.skipButton.style.display = 'none'; 
            }
            if (this.submitButton) {
                this.submitButton.style.display = 'none';
            }

            this.renderResult(skipped);
            await this.renderExplanation();

            this.onComplete({
                question: this.question,
                task: response.task
            });
        }
    }

    async _submitAnswer(studentAnswer) {
        TaskEvent.post('question', 'onSubmitAnswer', this.question.id);

        if (!studentAnswer) {
            studentAnswer = {};
        }

        studentAnswer.protocolVersion = 2;
        studentAnswer.taskId = this.config.taskId;
        studentAnswer.lessonStructure = this.config.lessonStructure;
        studentAnswer.questionId = this.question.id;

        switch (this.config.taskType) {
            case 'Lesson': return await APISync.submitLessonAnswer(this.question.id, this.config.topicId, studentAnswer); 
            case 'Diagnostic': return await APISync.submitDiagnosticAnswer(this.question.id, studentAnswer);                         
            case 'Reference': return await APISync.submitReferenceAnswer(this.question.id, studentAnswer);                     
            case 'Review': return await APISync.submitReviewAnswer(this.question.id, studentAnswer);               
            default: return null; 
        }
    }
}

QuestionWidget.create = function(container, question, config) {
    switch(question.format) {
        case 'MC': return new MultipleChoiceQuestionWidget(container, question, config);
        case 'FR': return new FreeResponseQuestionWidget(container, question, config);
        case 'SS': return new StaticSelectQuestionWidget(container, question, config);
        case 'DS': return new DynamicSelectQuestionWidget(container, question, config);
        case 'PR': return new ProofQuestionWidget(container, question, config);
        case 'CO': return new CodeQuestionWidget(container, question, config);        
        default: return null;
    }
}