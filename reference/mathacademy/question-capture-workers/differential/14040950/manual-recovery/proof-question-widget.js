class ProofQuestionWidget extends DynamicSelectQuestionWidget {
    constructor(container, question, config) {
        super(container, question, config);
    }

    async renderBody() {
        this.bodyDiv = document.createElement('div');
        this.bodyDiv.className = 'questionWidget-body';
        Core.insertAfter(this.textDiv, this.bodyDiv);


        this.body = new QuestionBodyWidget(this.bodyDiv);
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

    async renderExplanation() {
        let explanationHeader = Core.createDiv(this.element, null, 'questionWidget-explanationHeader', 'EXPLANATION');  

        let explanation = this.question.explanation + this.getCompleteProof();

        this.explanationDiv = Core.createDiv(this.element, null, 'questionWidget-explanation', explanation);  

        await renderLatex([this.explanationDiv]);   
    }

    getCompleteProof() {
        let arr = [];
        for(let segment of this.question.body.segments) {
            if (segment.text) {
                arr.push(segment.text);
            } else if (segment.mathJax) {
                arr.push(segment.mathJax);
            } else if (segment.select) {
                let select = segment.select;

                if (select.options.length > 0) {
                    let correctOption = select.options[select.correctIndex];
                    arr.push(correctOption);
                }
            } else if (segment.newParagraph) {
                arr.push('<p>');
            }
        }

        let html = '<div class="questionWidget-proofHeader">PROOF</div>' + arr.join('');

        return html;        
    }
}