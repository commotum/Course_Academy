class TaskAnswers {
    constructor(task, taskAnswersDiv) {
        this.task = task;
        this.taskAnswersDiv = taskAnswersDiv;

        this.adminMode = this.isAdminMode();
    }

    isAdminMode() {
        const url = new URL(location);
        const pathParts = url.pathname.split('/');
        pathParts.shift();

        if (pathParts.length === 3 && pathParts[0] === 'tasks' && pathParts[2] === 'answers') {
            return true;
        } else {
            return false;
        }
    }

    async render() {                                   
        switch(this.task.type) {
            case 'Lesson':  
                //this.loadTaskLocalGraph();
                this.loadLessonAnswers(); 
                break;
            case 'Review': 
                //this.loadTaskLocalGraph();
                this.loadReviewAnswers(); 
                break;
            case 'Quiz': 
            case 'Exam': 
                this.loadTestAnswers(); 
                break;
            case 'Placement': 
            case 'Supplemental':                   
                this.loadTestAnswers(); 
                break;                       
            case 'Multistep': 
                this.loadMultistepAnswers(); 
                break;
        } 

        await renderLatex([this.taskAnswersDiv]);
    }

    loadTaskLocalGraph() {
        let taskDetailsDiv = document.getElementById('taskDetails-' + this.task.id + '-expanded');

        let kgDiv = Core.createDiv(taskDetailsDiv, 'taskKG-' + this.task.id, 'knowledgeGraph');
        KnowledgeGraphWidget.createInstance(kgDiv, this.task.localGraph);
    }

    async loadLessonAnswers() {
        let kpListDiv = Core.createDiv(this.taskAnswersDiv, null, 'kpList');

        for(let example of this.task.exampleAnswers) {
            let kpDiv = Core.createDiv(kpListDiv, null, 'kp');
            Core.createDiv(kpDiv, null, 'kpTitle', `<b>KP ${example.number}.</b> ${example.title}`);

            this.loadAnswers(kpDiv, example.answers);
        }
    }

    async loadReviewAnswers() {
        let answerListDiv = Core.createDiv(this.taskAnswersDiv, null, 'reviewAnswerList');

        this.loadAnswers(answerListDiv, this.task.answers, true);
    }

    async loadMultistepAnswers() {
        let answerListDiv = Core.createDiv(this.taskAnswersDiv, null, 'multistepAnswerList');

        this.loadAnswers(answerListDiv, this.task.answers, true);
    }    

    async loadTestAnswers() {
        let answerListDiv = Core.createDiv(this.taskAnswersDiv, `testAnswers-${this.task.id}`, 'testAnswers');

        this.loadAnswers(answerListDiv, this.task.answers, true);
    }

    onMouseDownAnalysisTab(event) {
        this.showTestAnalysis(this.task.id);          
    }

    onMouseDownAnswersTab(event) {
        this.showTestAnswers(this.task.id);          
    }    

    showTestAnalysis() {
        let analysisTab = $(`testAnalysisTab-${this.task.id}`);
        analysisTab.className = 'tabSelected';

        let answersTab = $(`testAnswersTab-${this.task.id}`);   
        answersTab.className = 'tab';


        let analysisDiv = $(`testAnalysis-${this.task.id}`);
        analysisDiv.style.display = 'block';

        let answersDiv = $(`testAnswers-${this.task.id}`);   
        answersDiv.style.display = 'none';    
    }

    showTestAnswers() {
        let analysisTab = $(`testAnalysisTab-${this.task.id}`);
        analysisTab.className = 'tab';

        let answersTab = $(`testAnswersTab-${this.task.id}`);   
        answersTab.className = 'tabSelected';

        let analysisDiv = $(`testAnalysis-${this.task.id}`);
        analysisDiv.style.display = 'none';

        let answersDiv = $(`testAnswers-${this.task.id}`);   
        answersDiv.style.display = 'block';    
    }    

    loadTestAnalysis(analysis) {
        let testAnalysisTable = Core.createTable(this.taskAnswersDiv, `testAnalysis-${this.task.id}`, 'testAnalysis');

        for(let course of analysis.courses) {
            for(let unit of course.units) {
                let unitRow = Core.createRow(testAnalysisTable);

                let unitCell = Core.createCell(unitRow, null, null, 'testAnalysis-unitHeader', `${unit.numeral}. ${unit.name}`);
                unitCell.colSpan = 3;

                for(let module of unit.modules) {
                    for(let topic of module.topics) {
                        let topicRow = Core.createRow(testAnalysisTable, -1, null, 'testAnalysis-topic');

                        if (topic.correct)  {
                            Core.createCell(topicRow, 0, null, 'testAnalysis-correctAnswer', 'Correct');
                        } else {
                            Core.createCell(topicRow, 0, null, 'testAnalysis-incorrectAnswer', 'Incorrect');
                        }

                        let topicNumberCell = Core.createCell(topicRow, 1, null, 'testAnalysis-topicNumber');
                        Core.createAnchor(topicNumberCell, null, null, `${module.number}.${topic.number}`, `/topics/${topic.urlSlug}-${topic.id}`); 

                        let topicNameCell = Core.createCell(topicRow, 2, null, 'testAnalysis-topicName');
                        Core.createAnchor(topicNameCell, null, null, `${topic.name}`, `/topics/${topic.urlSlug}-${topic.id}`);                        
                    }
                }
            }
        }
    }

    async loadAnswers(parentDiv, answers, includeExampleTitle) {
        for(let answer of answers) {
            let question = answer.question;
            let topic = question.topic;
            let example = question.example;            

            let questionDiv = Core.createDiv(parentDiv, `question-${question.id}`, 'question');
            questionDiv.onclick = this.onMouseDownQuestion.bind(this);

            let questionHeaderDiv = Core.createDiv(questionDiv, null, 'questionHeader');

            Core.createSpan(questionHeaderDiv, null, 'questionNumber', `${answer.number}.`);

            if (includeExampleTitle) {
                let url;
                
                if (topic.course) {
                    url = `/topics/${topic.id}?courseId=${topic.course.id}#${example.id}`;
                } else {
                    url = `/topics/${topic.id}#${example.id}`;
                }

                Core.createAnchor(questionHeaderDiv, null, 'questionKP', `${example.title}`, url);
            }


            if (!this.adminMode) {            
                let helpButton = Core.createSpan(questionHeaderDiv, null, 'helpButton', '?');
                helpButton.setAttribute('questionId', question.id);
                helpButton.onmouseover = (evt) => {
                    let helpMenu = new HelpMenu(helpButton, {
                        taskType: this.task.type,
                        taskid: this.task.id,
                        topicId: this.task.topic.id,
                        taskComplete: this.task.completed !== null,
                        type: 'question',
                        id: question.id,
                        topOffset: -100                   
                    });
                    helpMenu.show();
                }
            }

            if (question.graphic) { 
                let graphicDiv = Core.createDiv(questionDiv, null, 'questionGraphicFrame');                      
                let graphic = Core.createImg(graphicDiv, null, 'questionGraphic');
                graphic.src = `/graphics/q-${question.id}`;
            }

            let questionTextDiv = Core.createDiv(questionDiv, null, 'questionText', question.text);      
                
            switch (question.format) {
                case 'FR': this.formatFreeResponse(questionTextDiv, question); break;
                case 'SS': this.formatBody(questionDiv, question); break;
                case 'DS': this.formatBody(questionDiv, question); break;
                case 'PR': this.formatBody(questionDiv, question); break;
            }

            let answerDetailsDiv = Core.createDiv(questionDiv, null, 'answerDetails');    

            this.createDifficultyDiv(answerDetailsDiv, question);


            if (this.adminMode) {
                Core.createAnchor(answerDetailsDiv, null, 'questionId', `${question.id}`, `/topics/${question.topic.id}/questions#${question.id}`);  
                Core.createSpan(answerDetailsDiv, null, 'answerDetailsSeparator', '|');  
            }

            Core.createSpan(answerDetailsDiv, null, 'answerCreated', answer.createdStr);  
            Core.createSpan(answerDetailsDiv, null, 'answerDetailsSeparator', '|');  

            Core.createSpan(answerDetailsDiv, null, 'timeElpased', `Elapsed: ${answer.timeElapsedFormatted}`);  

            let answerResultSpan = Core.createSpan(answerDetailsDiv, null, 'answerResult', `Question ${answer.number}`);   


            if (question.format === 'DS' || question.format === 'PR') {
                if (question.health >= 1.0) {
                    answerResultSpan.innerHTML = `<span style="color: green;">Full Credit</span>`;
                } else if (question.health > 0) {
                    answerResultSpan.innerHTML = `<span style="color: green;">Partial Credit</span>`;
                } else {
                    answerResultSpan.innerHTML = `<span style="color: red;">No Credit</span>`;
                }
            } else {
                if (answer.correct) {
                    answerResultSpan.innerHTML = `<span style="color: green;">Correct</span>`;
                } else {
                    answerResultSpan.innerHTML = `<span style="color: red;">Incorrect</span>`;
                }   
            }


            let explanationDiv = Core.createDiv(parentDiv, `questionExplanation-${question.id}`, 'questionExplanation', question.explanation);

            if (!answer.correct && (question.format === 'MC' || question.format === 'FR')) {
                Core.createDiv(explanationDiv, null, 'studentAnswerHeader', 'Your Answer:');    

                let studentAnswerDiv = Core.createDiv(explanationDiv, null, 'studentAnswer');   

                if (question.format === 'MC') {
                    switch (answer.selectedChoice) {
                        case 1: studentAnswerDiv.innerHTML = question.choice1; break;
                        case 2: studentAnswerDiv.innerHTML = question.choice2; break;
                        case 3: studentAnswerDiv.innerHTML = question.choice3; break;
                        case 4: studentAnswerDiv.innerHTML = question.choice4; break;
                        case 5: studentAnswerDiv.innerHTML = question.choice5; break;
                        default: studentAnswerDiv.innerHTML = '<i>No answer</i>'; break;
                    }
                } else if (question.format === 'FR') {
                    studentAnswerDiv.innerHTML = this.formatFreeResponseAnswers(answer.freeResponse);
                }
            }                 
        }        
    }

    formatFreeResponseAnswers(str) {
        if (!str) {
            return '<i>No answer</i>';
        }
       
        try {
            const freeResponse = JSON.parse(str);
            const wrappedAnswers = freeResponse.map(answer => '$' + answer + '$');
            return wrappedAnswers.join(', ');
        } catch {
            return str;
        }
    }
 
    createDifficultyDiv(parentDiv, question) {
        let difficultyDiv = Core.createDiv(parentDiv, null, `questionDifficulty ${question.difficultyClass}`, question.difficultySymbol);  

        let tooltip;

        difficultyDiv.onmouseover = (event) => {
            tooltip = this.showTooltip(difficultyDiv, question.difficultySymbol);            
        };

        difficultyDiv.onmouseout = (event) => {
            if  (tooltip) {
                tooltip.hide();
                delete difficultyDiv.tooltip;
            }
        };

        difficultyDiv.tooltip = tooltip;
    }

    showTooltip(difficultyDiv, difficultySymbol) {
        let text;
        switch (difficultySymbol) {
            case 'E': text = 'Difficulty - Easy'; break;
            case 'M': text = 'Difficulty - Moderate'; break;
            case 'H': text = 'Difficulty - Hard'; break;
        }

        let tooltip = new Core2.Tooltip(difficultyDiv, text);

        return tooltip;
    }

    formatFreeResponse(questionTextDiv, question) {
        let parser = new FreeResponseParser();
        parser.render(question.freeAnswerChoice, questionTextDiv, 'static');
    }

    async formatBody(questionDiv, question) {
        let questionProofDiv = Core.createDiv(questionDiv, `questionBody-${question.id}`, 'questionBody');

        this.body = new QuestionBodyWidget(questionProofDiv);
        await this.body.init(question.id, question.body.segments, true);
    }

    stripEnclosingParagraphTags(str) {
        if (str && str.length > 0) {
            str = str.trim();

            let start = str.substring(0, 3);
            let end = str.substring(str.length - 4);

            if (start === '<p>' && end === '</p>') {
                str = str.substring(3, str.length - 4);
            } 
        }

        return str;
    }

    onMouseDownQuestion(event) {
        let questionDiv = Core.findEventSource(event, 'question');
        let questionId = questionDiv.id.split('-')[1];

        let explanationDiv = $(`questionExplanation-${questionId}`);
        let display = explanationDiv.style.display;

        if (display === 'block') {
            explanationDiv.style.display = 'none';
        } else {     
            explanationDiv.style.display = 'block';
        }  
    }
}