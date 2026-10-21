var studentReference;

window.onload = (evt) => {
    studentReference = new StudentReference();
    studentReference.init();
};

class StudentReference {
    constructor() {
        this.answers = {};
        this.steps = {};
        this.activeStep = null;      
        
        this.topicId = this.getTopicId();
    }

    async init() {
        this.lesson = await APISync.getReferenceLesson(this.topicId);
        this.taskId = this.lesson.taskId;

        TaskEvent.init(this.taskId);

        // Init steps
        let stepDivs = document.getElementsByClassName('step');
    
        let exampleStep;
        for(let i = 0; i < stepDivs.length; i++) {
            let stepDiv = stepDivs[i];
    
            let step = {
                number: i + 1,
                id: stepDiv.getAttribute('stepId'),
                type: stepDiv.getAttribute('stepType'),
                contentId: stepDiv.getAttribute('contentId')
            };
    
            if (step.type === 'example') {
                exampleStep = step;
            } else if (step.type === 'question') {
                step.exampleStep = exampleStep;
            }
    
            this.steps[step.id] = step;
        }

        let sectionLinks = document.getElementsByClassName('sectionLink');
        for(let sectionLink of sectionLinks) {
            sectionLink.onmousedown = this.onMouseDownSectionLink.bind(this);
        }
    
        this.renderLesson();

        Core.attachEventHandlers('helpButton', 'mouseover', this.onMouseOverHelpButton.bind(this));

        document.body.onscroll = this.updateActiveStep.bind(this);      

        this.updateActiveStep();
    }

    onMouseDownSectionLink(event) {
        let sectionLink = event.target || event.srcElement;
        let stepId = parseInt(sectionLink.getAttribute('stepId'));

        let stepDiv = $(`step-${stepId}`);
        stepDiv.scrollIntoView();
    }

    onMouseOverHelpButton(event) {
        let menuButton = Core.findEventSource(event, `helpButton`);
        let stepId = parseInt(menuButton.getAttribute('stepId'));
        let step = this.getStepById(stepId);

        let helpMenu = new HelpMenu(menuButton, {
            taskType: 'Reference',
            taskid: this.taskId,
            topicId: this.topicId,
            type: step.type,
            title: step.tutorial ? step.tutorial.title : step.example.title,
            topOffset: -100
        });
        helpMenu.show();
    }

    getStepById(stepId) {
        for(let step of this.lesson.steps) {
            if (step.id === stepId) { return step; }
        }
        return null;
    }

    getQuestionById(questionId) {
        for(let step of this.lesson.steps) {
            if (step.question && step.question.id == questionId) {
                return step.question;
            }
        }
    }

    getTopicId() {
        let pathParts = window.location.pathname.split('/');
        let topicPart = pathParts[pathParts.length - 1];

        let topicId;

        if (topicPart.indexOf('-') === -1) {
            topicId = topicPart;
        } else {
            // Handle case where the topic is a slug with an id appended and not just an id
            let slugParts = topicPart.split('-');
            topicId = slugParts[slugParts.length - 1];
        }

        return topicId;
    }

    showPage() {
        this.header.style.display = 'block';
        this.stepsFrame.style.display = 'block';

        //if (this.step) {
        //    this.scrollStepIntoView(false);
        //}
    }

    renderLesson() {
        for(let step of this.lesson.steps) {
            switch(step.type) {
                //case 'tutorial': this.renderTutorial(step); break;
                //case 'example': this.renderExample(step); break;
                case 'question': this.renderQuestion(step); break;
            }
        }
    }

    async renderQuestion(step) {
        let question = step.question;

        let questionDiv = document.getElementById('question-' + question.id);
        if (!questionDiv) {
            return;
        }

        question.widget = new QuestionWidget.create(questionDiv, question, {
            taskType: 'Reference',
            taskId: this.taskId,
            topicId: this.topicId,
            submitButton: true
        });

        question.widget.show();
        question.widget.deactivate();
    }
    
    
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Step scrolling

    updateCurrentStep(event) {
        let step = this.findVisibleStep();

        this.setCurrentStep(step);
        this.updateStepButtons(); 
    }

    findVisibleStep() {
        let stepDivs = document.getElementsByClassName('step');

        let visibleStep;
        let maxPercent = 0;
        for(let i = 0; i < stepDivs.length; i++) {
            let stepDiv = stepDivs[i];                  
            if (stepDiv.style.display === 'block') { 
                let percent = this.getPercentOfView(stepDiv);
    
                if (percent >= maxPercent) {
                    visibleStep = this.lesson.steps[i];
                    maxPercent = percent;
                }
            }
        }

        return visibleStep;
    }

    getPercentOfView(element) {
        const viewTop = window.pageYOffset;
        const viewBottom = viewTop + window.innerHeight;
        const rect = element.getBoundingClientRect();
        const elementTop = rect.top + viewTop;
        const elementBottom = elementTop + rect.height;
    
        if (elementTop >= viewBottom || elementBottom <= viewTop) {
            // Heigher or lower than viewport
            return 0;
        } else if (elementTop <= viewTop && elementBottom >= viewBottom) { 
            // Element is completely in viewport and bigger than viewport
            return 100;
        } else if (elementBottom <= viewBottom) {
            if (elementTop < viewTop) {
                // Intersects viewport top
                return Math.round((elementBottom - viewTop) / window.innerHeight * 100);
            } else {
                // Completely inside viewport
                return Math.round((elementBottom - elementTop) / window.innerHeight * 100);;
            }
        } else {
            // Intersects viewport bottom
            // elementBottom >= viewBottom && elementTop <= viewBottom
            return Math.round((viewBottom - elementTop) / window.innerHeight * 100);
        }
    }
    
    findCurrentStep() {
        for(let step of this.lesson.steps) {
            if (step.current) { return step; }
        }

        // Fail safe
        let lastVisitedStep = this.lesson.steps[0];
        for(let step of this.lesson.steps) {
            if (step.visited) { 
                lastVisitedStep = step; 
            }
        }
        return lastVisitedStep;
    }

    updateActiveStep(event) {
        let step = this.findVisibleStep();
    
        if (step !== this.activeStep) {
            TaskEvent.post(step.type, 'onView', step.id);            

            if (this.activeStep && this.activeStep.question && this.activeStep.question.widget) {
                this.activeStep.question.widget.deactivate();
            }        
            this.activeStep = step;    
            if (this.activeStep.question && this.activeStep.question.widget) {
                this.activeStep.question.widget.activate();
            }

            let sectionLinks = document.getElementsByClassName('sectionLink');
            for(let sectionLink of sectionLinks) {
                sectionLink.style.color = null;;
            }

            let sectionLink;
            if (step.type === 'question') {
                let question = step.question;
                let exampleStep = this.findExampleStep(question.example.id);
                sectionLink = $('sectionLink-' + exampleStep.id);
            } else {
                sectionLink = $('sectionLink-' + step.id);
            }
    
            sectionLink.style.color = 'rgb(64, 64, 64)';            
        }
    }

    findExampleStep(exampleId) {
        for(let step of this.lesson.steps) {
            if (step.example && step.example.id === exampleId) {
                return step;
            }
        }
        return null;
    }
    
    scrollToTop() {    
        window.scrollTo(0, 0);
    }
}