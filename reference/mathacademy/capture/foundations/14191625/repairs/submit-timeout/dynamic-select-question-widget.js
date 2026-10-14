class DynamicSelectQuestionWidget extends QuestionWidget {
    constructor(container, question, config) {
        super(container, question, config);
    }

    renderHealth() {
        if (!this.question.testMode) {
            this.healthFrame = Core.createDiv(this.element, null, 'questionWidget-healthFrame');
            this.header.insertBefore(this.healthFrame, this.helpButton);
            this.healthBar = Core.createDiv(this.healthFrame, null, 'questionWidget-healthBar');
            this.healthBar.style.width = '0%';

            this.updateHealth(this.question.health);
        }
    }

    async renderBody() { 
        this.body = new QuestionBodyWidget(this.textDiv);
        await this.body.init(this.question.id, this.question.body.segments);
        
        this.body.onSelect = (questionBody, select) => { 
            TaskEvent.post('question', 'onSelectOption', this.question.id);

            let answers = this.body.getAnswers();

            if (answers.length === this.body.selects.length) {
                this.enableSubmitButton(this.question.id);
            } else {
                this.disableSubmitButton(this.question.id);
            }  
        };

        //this.updateSegments();
    }

    updateHealth(health) {
        if (health > 0) {
            health = Math.min(health, 1.0);
            this.healthBar.style.width = (100 * health).toFixed(0) + '%';
        } else if (health === 0) {
            this.healthBar.style.width = '3px';
            this.healthBar.style.background = 'red';
        }
    }

    async update(response) {
        if (!this.question.testMode) {
            this.updateHealth(response.question.health);
        }
        
        if (response.question.answer) {
            let startIndex = this.question.body.segments.length;
            let newSegments = response.question.body.segments.slice(startIndex);

            if (newSegments.length > 0) {
                await this.body.update(newSegments);
            }

            this.question.body.segments = response.question.body.segments;

            this.updateSegments();

            this.clearMessage();
        } else {

            let startIndex = this.question.body.segments.length;
            let newSegments = response.question.body.segments.slice(startIndex);

            if (newSegments.length > 0) {
                await this.body.update(newSegments);

                this.question.body.segments = response.question.body.segments;

                this.updateSegments();

                this.clearMessage();
            } else {
                this.showTryAgainMessage();

                this.enableCurrentSection();
            }
        }
    }

    updateSegments() {
        for(let segment of this.question.body.segments) {
            if (segment.select) {
                let select = segment.select;
                let selectWidget = this.getSelectWidgetById(select.id);
                selectWidget.update(select);
            }
        }                  
    }

    clearMessage() {
        if (this.feedbackDiv) {
            this.element.removeChild(this.feedbackDiv);
            delete this.feedbackDiv;
        }
    }

    showTryAgainMessage() {
        this.updateFeedback("Oops, that's not quite right. Please try again.");
    }

    updateFeedback(message) {
        if (!this.feedbackDiv) {
            this.feedbackDiv = document.createElement('div');
            this.feedbackDiv.className = 'questionWidget-feedback';
            this.element.insertBefore(this.feedbackDiv, this.buttonBar);        
        }

        this.feedbackDiv.innerHTML = message;
    }
    
    disable() {
        this.body.disable();
    }

    getStudentAnswer() {
        let inputAnswers = [];

        let currentSectionIndex = this.getCurrentSectionIndex();
        for(let select of this.body.selects) {
            if (this.question.testMode || select.sectionIndex === currentSectionIndex) {
                inputAnswers.push({
                    inputId: select.config.id,
                    selectedIndex: select.getSelectedIndex()
                });
            }
        }

        return {
            questionId: this.question.id,
            taskId: this.question.taskId,
            inputAnswers
        };
    }

    enableCurrentSection() {
        let currentSectionIndex = this.getCurrentSectionIndex();

        for(let select of this.body.selects) {
            if (select.sectionIndex === currentSectionIndex) {
                select.enable();
            }
        }
    }

    getCurrentSectionIndex() {
        let selects = this.body.selects;
        let lastSelect = selects[selects.length - 1];
        let currentSectionIndex = lastSelect.sectionIndex;

        return currentSectionIndex;
    }

    markExistingSectionsCorrect() {
        for(let select of this.body.selects) {
            select.setCorrect();
        }
    }

    renderResult() {
        this.resultDiv = Core.createDiv(this.element, null, 'questionWidget-result');  

        if (this.question.answer.correct) {
            let creditText = this.question.health >= 1.0 ? 'Correct' : 'Partial Credit';

            Core.createDiv(this.resultDiv, null, 'questionWidget-correctIncorrectIcon', '<img src="/img/green-checkmark.png"/>');
            Core.createDiv(this.resultDiv, null, 'questionWidget-correctText', creditText);

        } else {
            Core.createDiv(this.resultDiv, null, 'questionWidget-correctIncorrectIcon', '<img src="/img/incorrect-answer.png"/>');
            Core.createDiv(this.resultDiv, null, 'questionWidget-incorrectText', 'Incorrect');
        }    
    }

    getSelectWidgetById(id) {
        for(let i = 0; i < this.body.selects.length; i++) {
            let select = this.body.selects[i];

            if (parseInt(select.config.id) === parseInt(id)) {
                return select;
            }
        }
        return null;
    }
}
