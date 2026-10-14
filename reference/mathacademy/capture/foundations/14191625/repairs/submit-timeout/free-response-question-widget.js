class FreeResponseQuestionWidget extends QuestionWidget {
    constructor(element, question, config) {
        super(element, question, config);
    }

    async renderBody() {
        let answers = null;
        if (this.question.answer) {
            answers = this.question.answer.freeResponse;
        }

        const mode = answers ? 'static' : 'live';

        const parser = new FreeResponseParser();
        parser.render(this.question.freeAnswerChoice, this.textDiv, mode, answers);

        parser.onAnswersEntered = (answers) => {
            TaskEvent.postDelay('question', 'onUpdateAnswer', this.question.id);

            if (answers.length === parser.editors.length) {
                this.enableSubmitButton(this.question.id);
            } else {
                this.disableSubmitButton(this.question.id);
            }
        };

        this.freeResponseParser = parser;
    }

    async renderQuestion() {
        await super.renderQuestion();

        // Prevent MathJax containers from being selected by the tab key.
        // This can be annoying when tabbing between multiple free-response textboxes.
        // Must run after super.renderQuestion() so MJX-CONTAINER elements exist.
        const mjxContainers = this.textDiv.getElementsByTagName('MJX-CONTAINER');
        for (let mjxContainer of mjxContainers) {
            mjxContainer.setAttribute('tabindex', -1);
        }
    }


    disable() {
        this.freeResponseParser.disable();
    }

    getStudentAnswer() {
        return {
            questionId: this.question.id,
            taskId: this.question.taskId,
            freeResponseAnswers: this.freeResponseParser.getEnteredAnswers()
        };
    }
}