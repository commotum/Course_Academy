class StaticSelectQuestionWidget extends QuestionWidget {
    constructor(container, question, config) {
        super(container, question, config);
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

        this.updateSegments();
    }

    async update(response) {
        let inputs = response.question.inputs;

        let inputIndex = 0;
        for(let segment of this.question.body.segments) {
            if (segment.select) {
                let select = segment.select;

                select.selectedIndex = inputs[inputIndex].selectedIndex;
                select.correct = inputs[inputIndex].correct;
                select.disabled = true;

                inputIndex++;
            }
        }

        this.updateSegments();
    }

    updateSegments() {
        for(let segment of this.question.body.segments) {
            if (segment.select) {
                let select = segment.select;
                let selectWidget = this.body.selects[select.index];

                if (select.correct === true || select.correct === 1) {
                    selectWidget.setCorrect();
                } else if (select.correct === false || select.correct === 0) {
                    selectWidget.setIncorrect();
                }

                if (select.disabled) {
                    selectWidget.disable();
                }

                if (select.selectedIndex >= 0) {
                    selectWidget.selectOption(select.selectedIndex);
                }
            }
        }                  
    }

    disable() {
        this.body.disable();
    }

    getStudentAnswer() {
        return {
            questionId: this.question.id,
            taskId: this.question.taskId,
            selectedOptions: this.body.getAnswers()
        };
    }
}

