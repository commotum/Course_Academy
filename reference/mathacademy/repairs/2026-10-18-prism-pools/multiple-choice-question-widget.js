class MultipleChoiceQuestionWidget extends QuestionWidget {
    constructor(element, question, config) {
        super(element, question, config);

        this.selectedChoice = null;

        if (!this.question.answer) {
            this.element.onclick = (evt) => {
                if (!this.answerSubmitted) {
                    this.unselectChoices();
                    this.disableSubmitButton();
                }
            }         
        }
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Virtual functions

    reset() {
        this.unselectChoices();
        this.disableSubmitButton();
    }

    enable() {
        window.addEventListener('keydown', this.onKeyDown.bind(this));     
    }

    disable() {
        window.removeEventListener('keydown', this.onKeyDown.bind(this));     
    }

    renderBody() { 
        let choicesTable = Core.createTable(this.element, null, 'questionWidget-choicesTable');

        this.renderChoice('a', this.question.choice1, choicesTable);
        this.renderChoice('b', this.question.choice2, choicesTable);
        this.renderChoice('c', this.question.choice3, choicesTable);
        this.renderChoice('d', this.question.choice4, choicesTable);
        this.renderChoice('e', this.question.choice5, choicesTable);

        if (this.question.answer) {
            let letter = ['a','b','c', 'd', 'e'][this.question.answer.selectedChoice - 1];
            let letterDiv = this.getLetterChoiceDiv(letter);
            letterDiv.style.background = 'rgb(64, 64, 64)';
            letterDiv.style.color = 'white';
        }
    }

    getStudentAnswer() {
        return {
            questionId: this.question.id,
            taskId: this.question.taskId,
            selectedChoice: this.question.selectedChoice
        };
    }

    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    renderChoice(letter, choiceText, choicesTable) {
        let row = Core.createRow(choicesTable, choicesTable.rows.length);
        let letterCell = Core.createCell(row, 0, null, 'questionWidget-choiceLetter');
        
        let letterDiv = Core.createDiv(letterCell, 'questionWidget-choiceLetterCircle-' + this.question.id + '-' + letter, 'questionWidget-choiceLetterCircle', letter);

        if (!this.question.answer) {
            letterDiv.onclick = this.onClickChoice.bind(this, letter); 
        }

        let textCell = Core.createCell(row, 1, null, 'questionWidget-choiceText', choiceText);        

        if (!this.question.answer) {
            textCell.onclick = this.onClickChoice.bind(this, letter);         
        }
    }

    onClickChoice(letter, event) {
        Core.killEvent(event);
        if (this.answerSubmitted) { return; }
        this.selectChoice(letter);        
    }
    
    onKeyDown(event) {    
        if (__modalDialog) { return; }
        if (this.answerSubmitted) { return; }
        if (this.question.answer) { return; }
        if (!this.active) { return; }

        switch (event.key) {
            case 'Escape':
                this.unselectChoices();
                this.disableSubmitButton();
                break;
            case 'A':
            case 'a': 
                this.selectChoice('a'); 
                break;
            case 'B':             
            case 'b': 
                this.selectChoice('b'); 
                break;
            case 'C': 
            case 'c': 
                this.selectChoice('c'); 
                break;
            case 'D': 
            case 'd': 
                this.selectChoice('d'); 
                break;
            case 'E': 
            case 'e': 
                this.selectChoice('e'); 
                break;                                                                
        }
    } 

    getLetterChoiceDiv(letter) {
        let letterDiv = $('questionWidget-choiceLetterCircle-' + this.question.id + '-' + letter);
        return letterDiv;
    }
    
    selectChoice(letter) {
        TaskEvent.post('question', 'onSelectChoice', this.question.id);

        this.unselectChoices();
        this.enableSubmitButton();        

        let letterDiv = this.getLetterChoiceDiv(letter);
        letterDiv.style.background = 'rgb(64, 64, 64)';
        letterDiv.style.color = 'white';

        this.question.selectedChoice = this.getSelectedChoice(letter);    
    }

    getSelectedChoice(letter) {
        if (letter === 'a') { return 1; }
        else if (letter === 'b') { return 2; }
        else if (letter === 'c') { return 3; }
        else if (letter === 'd') { return 4; }
        else { return 5; }
    }
    
    unselectChoices() {
        this.unselectChoice('a');
        this.unselectChoice('b');
        this.unselectChoice('c');
        this.unselectChoice('d');
        this.unselectChoice('e');
    }
        
    unselectChoice(letter) {
        let letterDiv = this.getLetterChoiceDiv(letter);

        if (!letterDiv) {
            let letterDiv2 = this.getLetterChoiceDiv(letter);
        }

        letterDiv.style.background = null;
        letterDiv.style.color = null;

        this.question.selectedChoice = null;
    }
}