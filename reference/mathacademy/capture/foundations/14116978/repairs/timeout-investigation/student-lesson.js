var studentLesson;

window.onload = (evt) => {
    studentLesson = new StudentLesson();
    studentLesson.init();
};

MathJaxPageLoaded = () => {
    if (studentLesson) {
        studentLesson.showPage();
    }
}

class StudentLesson {
    async init() {
        const pathParts = window.location.pathname.split('/');

        this.taskId = parseInt(pathParts[2]);
        this.topicId = parseInt(pathParts[4]);  

        TaskEvent.init(this.taskId);

        this.header = $('header');
        this.stepsFrame = $('stepsFrame');
        
        this.exitButton = $('exitButton');
        this.exitButton.onmousedown = (evt) => {
            window.location.href = '/learn';
        }          

        this.progressBar = $('progressBar');

        Core.attachEventHandlers('helpButton', 'mouseover', this.onMouseOverHelpButton.bind(this));       
        Core.attachEventHandlers('continueButton', 'mousedown', this.onMouseDownContinueButton.bind(this));       

        // Guard against completeTask being interrupted (e.g. by a site restart).
        if (taskAlreadyCompleted) {
            this.lesson = {
                pointsAwarded: initialPointsAwarded,
                taskPoints: initialTaskPoints,
                passed: initialTaskPassed,
            };
            this.showFinalScreen();
            return;
        }

        this.lesson = await APISync.getTaskLessonState(this.taskId, this.topicId);

        if (this.lesson.wasRepaired) {
            let messageBox = new MessageBox('Reload Required', `Oops, something has changed. The page needs to reload before continuing.`);
            await messageBox.showSync();
            window.location.reload();
            return;
        }

        for(let step of this.lesson.steps) {
            step.type = { 't': 'tutorial', 'e': 'example', 'q': 'question' }[step.id[0]];
            step.typeId = parseInt(step.id.substr(1));
        }

        this.freeResponseParsers = {};

        this.lessonStructure = this.getLessonStructure();

        if (this.lesson.done) {    
            TaskEvent.post('task', 'onComplete', this.taskId);   
            let eventType = this.lesson.pointsAwarded > 0 ? 'onPassed' : 'onFailed';
            TaskEvent.post('task', eventType, this.taskId);      

            API.cleanupTaskData(this.taskId);                 
            this.showFinalScreen();
        } else {
            this.updateQuestionNumbers();
            await this.renderQuestions();

            let currentStep = this.findCurrentStep();
            this.selectStep(currentStep);   

            this.updateProgressBar(); 
            this.updateStepDivs(); 
            this.updateContinueButtons();
            this.updateExampleInstructions();
        }

        this.showPage();
    
        document.body.onscroll = this.updateCurrentStep.bind(this);
    }

    insertRobotAnimation(step, action) {
        // Animation size: 500 x 500

        const robotFrame = Core.createDiv(null, null, 'robotFrame');
        const canvas = Core.createElement(robotFrame, 'canvas', null, 'robot');        

        const stepDiv = $('step-' + step.id);        
        stepDiv.after(robotFrame);

        const animation = new rive.Rive({
            src: '/img/robot.riv',
            canvas,
            autoplay: true,
            stateMachines: 'RobotMain',
            onLoad: () => {
                animation.resizeDrawingSurfaceToCanvas();
            },
        });     

        stepDiv.animation = animation;

        setTimeout((evt) => {            
            const inputs = animation.stateMachineInputs('RobotMain');
            const triggerInput = inputs.find(input => input.name === action);

            if (triggerInput) {
                triggerInput.fire(); 
            }
        }, 100);
    }

    insertRobotHeadAnimation(step, action) {
        // Animation size: 150 x 120

        const stepDiv = $('step-' + step.id);

        const robotHeadFrame = Core.createDiv(null, null, 'robotHeadFrame');
        const canvas = Core.createElement(robotHeadFrame, 'canvas', null, 'robotHead');

        stepDiv.after(robotHeadFrame);        

        const animation = new rive.Rive({
            src: '/img/robot_head.riv',
            canvas,
            autoplay: true,
            stateMachines: 'Robot Head',
            onLoad: () => {
                animation.resizeDrawingSurfaceToCanvas();
            },
        });     

        stepDiv.animation = animation;        
        
        setTimeout((event) => {
            const inputs = animation.stateMachineInputs('Robot Head');
            const triggerInput = inputs.find(input => input.name === action);
    
            if (triggerInput) {
                triggerInput.fire(); // Use .value = true/false for boolean inputs
            }            
        }, 100);
    }

    showPage() {
        if (taskAlreadyCompleted) {
            return;
        }

        this.header.style.display = 'block';
        this.stepsFrame.style.display = 'block';

        if (this.step) {
            TaskEvent.post(this.step.type, 'onView', this.step.typeId);  

            this.scrollStepIntoView(false);
        }
    }

    onMouseOverHelpButton(event) {
        let menuButton = Core.findEventSource(event, `helpButton`);
        let stepId = menuButton.getAttribute('stepId');
        let step = this.getStepById(stepId);

        let helpMenu = new HelpMenu(menuButton, {
            taskType: 'Lesson',
            taskId: this.taskId,
            topicId: this.topicId,
            type: step.type,
            title: step.tutorial ? step.tutorial.title : step.example.title,
            topOffset: -100
        });
        helpMenu.show();
    }

    updateCurrentStep(event) {
        let step = this.findVisibleStep();

        if (step !== this.step) {
            TaskEvent.post(step.type, 'onView', step.typeId);
        }

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

    getLessonStructure() {
        let steps = []
        for(let step of this.lesson.steps) {
            steps.push(step.id);           
        }

        return steps;
    }

    updateStepDivs() {        
        let stepDivs = document.getElementsByClassName('step');
        for(let i = 0; i < this.lesson.steps.length; i++) {
            let step = this.lesson.steps[i];
            let stepDiv = stepDivs[i];

            if (step.current || step.visited) { 
                stepDiv.style.display = 'block';
            } else {
                stepDiv.style.display = 'none';   
            }
        }
    }

    updateContinueButtons() {
        let continueButtons = document.getElementsByClassName('continueButton');
        for(let continueButton of continueButtons) {
            continueButton.style.display = 'none';  
        }

        let maxVisitedStep = this.getMaxVisitedStep();

        if (!maxVisitedStep.question || maxVisitedStep.question.answer) {
            let continueButton = $('continueButton-' + maxVisitedStep.id);
            continueButton.style.display = 'block';            
        }
    }

    updateExampleInstructions() {
        let divs = document.getElementsByClassName('exampleInstructions');
        for(let div of divs) {
            div.style.display = 'none';  
        }

        let prevStep;
        for(let step of this.lesson.steps) {
            if (step.question && step.visited && prevStep && prevStep.example) {
                let div = $('exampleInstructions-' + prevStep.id);
                if (div) {
                    div.style.display = 'block';
                }
            }

            prevStep = step;
        }
    }

    getMaxVisitedStep() {
        let maxVisitedStep = null;
        for(let i = 0; i < this.lesson.steps.length; i++) {
            let step = this.lesson.steps[i];
            if (step.visited) {
                maxVisitedStep = step;
            }
        }

        return maxVisitedStep;
    }

    async selectStep(step, autoScroll = true) {
        if (step.unlocked && step !== this.step) {

            this.setCurrentStep(step);

            this.stepDiv = $('step-' + this.step.id);
            this.stepDiv.style.display = 'block'; 
            
            this.updateQuestionNumbers();
            this.updateContinueButtons();
            this.updateExampleInstructions();

            if (step.question) {
                if (!step.question.answer) {
                    step.questionWidget.onComplete = this.onQuestionComplete.bind(this);    
                }

                step.questionWidget.show();                
            }

            if (autoScroll) {
                this.scrollStepIntoView();
            }
    
            this.updateProgressBar();              

            let question = this.step.question;
            let currentQuestionId = (question && !question.answer) ? question.id : null;

            let response = await APISync.selectLessonStep(this.taskId, this.topicId, this.lessonStructure, this.step.number, currentQuestionId);

            if (response.taskLocked) {
                let messageBox = new MessageBox('Under Maintenance', `This topic is currently under maintenance and will be available again shortly.`);
                await messageBox.showSync();

                window.location.href = '/learn';
            } else if (response.reload) {
                let messageBox = new MessageBox('Reload Required', `Oops, something has changed. The page needs to reload before continuing.`);
                await messageBox.showSync();

                window.location.reload();
            }
        }   
    }

    setCurrentStep(step) {
        this.step = step;

        for(let s of this.lesson.steps) {
            s.current = false;
        }

        this.step.current = true;
        this.step.visited = true;
    }

    updateProgressBar() {
        this.progressBar.innerHTML = '';

        this.progressBarPrevioustButton = Core.createDiv(this.progressBar, 'progressBarPreviousButton');
        this.progressBarPrevioustButton.className = 'progressBarPreviousButtonEnabled';
        this.progressBarPrevioustButton.onmousedown = this.onMouseDownPreviousButton.bind(this);

        for(let i = 0; i < this.lesson.steps.length; i++) {
            let step = this.lesson.steps[i];               
            let stepButton = document.createElement('div');

            this.progressBar.appendChild(stepButton);

            stepButton.id = 'stepButton-' + step.id;
            stepButton.className = 'stepButton';

            if (step.number) {
                if (step.current) {
                    stepButton.classList.add('current');
                } 

                if (!step.current && step.visited) {
                    stepButton.classList.add('visited');          
                }
            } else {
                stepButton.style.display = 'none';
            }

            stepButton.onmousedown = this.onMouseDownStepButton.bind(this);
        } 

        this.progressBarNextButton = Core.createDiv(this.progressBar, 'progressBarNextButton');      
        this.progressBarNextButton.className = 'progressBarNextButtonEnabled';          
        this.progressBarNextButton.onmousedown = this.onMouseDownNextButton.bind(this);    
    }

    updateStepButtons() {
        if (this.progressBarPrevioustButton) {
            if (this.step.number > 1) {
                this.progressBarPrevioustButton.className = 'progressBarPreviousButtonEnabled';
            } else {
                this.progressBarPrevioustButton.className = 'progressBarPreviousButtonDisabled';
            }
        }

        let stepIndex = this.step.number - 1;
        let nextStep = this.lesson.steps[stepIndex + 1]; 

        if (this.progressBarNextButton) {
            if (nextStep && nextStep.unlocked) {
                this.progressBarNextButton.className = 'progressBarNextButtonEnabled';
            } else {
                this.progressBarNextButton.className = 'progressBarNextButtonDisabled';
            }
        }

        let stepButtons = document.getElementsByClassName('stepButton');

        for(let i = 0; i < this.lesson.steps.length; i++) {
            let step = this.lesson.steps[i];
            let stepButton = stepButtons[i];

            if (step.current) {
                stepButton.className = 'stepButton current';
            }  else if (step.visited) {
                stepButton.className = 'stepButton visited';      
            } else {
                stepButton.className = 'stepButton';
            }
        } 
    }

    scrollStepIntoView(transition = true) {
        this.stepDiv = $('step-' + this.step.id);
        this.stepDiv.style.display = 'block';

        let stepTop = Core.findTop(this.stepDiv);

        window.scroll({
            left: 0,
            top: stepTop - 110,
            behavior: transition ? 'smooth'  : 'auto'
        });
    }

    onMouseDownStepButton(event) {
        let stepButton = Core.getEventSource(event);
        let stepId = stepButton.id.split('-')[1];
        let step = this.getStepById(stepId);

        if (step !== this.step) {
            this.selectStep(step);   
        }     
    }

    getStepById(stepId) {
        for(let step of this.lesson.steps) {
            if (step.id === stepId) { return step; }
        }
        return null;
    }

    onMouseDownPreviousButton(event) {
        this.movePrevious();
    }

    onMouseDownNextButton(event) {
        this.moveNext();
    }

    movePrevious() {
        if (this.step.number == 1) { return; }

        let stepIndex = this.step.number - 1;
        for(let i = (stepIndex - 1); i >= 0; i--) {
            let step = this.lesson.steps[i];
            if (step.visible) {
                this.selectStep(step);
                break;
            }
        }        
    }

    moveNext() {
        let stepIndex = this.findStepIndex(this.step);
        for(let i = (stepIndex + 1); i < this.lesson.steps.length; i++) {                
            let step = this.lesson.steps[i];

            if (step.unlocked) {
                this.selectStep(step);
                return;
            }
        }

        if (this.lesson.done) {
            API.cleanupTaskData(this.taskId);
            this.showFinalScreen();
        }
    }

    findStepIndex(step) {
        for(let i = 0; i < this.lesson.steps.length; i++) {   
            if (this.lesson.steps[i].id === step.id) { 
                return i; 
            }
        }
        return -1;
    }

    updateQuestionNumbers() {
        let questionNumber = 0;
        for(let step of this.lesson.steps) {
            if (step.question) {
                if (step.visible) {
                    step.question.number = ++questionNumber;
                }
            }
        }
    }

    async renderQuestions() {
        for(let step of this.lesson.steps) {
            if (step.question) {
                await this.renderQuestion(step);
            }
        }
    }

    async renderQuestion(step) {
        let question = step.question;
        let questionDiv = document.getElementById('step-' + step.id);

        let questionWidget = new QuestionWidget.create(questionDiv, question, {
            taskType: 'Lesson', 
            taskId: this.taskId, 
            topicId: this.topicId,
            lessonStructure: this.lessonStructure,
            submitButton: true
        });

        if (step.question.answer || step.visited || step.unlocked) {
            await questionWidget.show();
            
            if (step.unlocked && !step.question.answer) {
                questionWidget.onComplete = this.onQuestionComplete.bind(this);            
            }
        }

        step.questionWidget = questionWidget;
    }

    onQuestionComplete(event) {
        let step = this.getStepById('q' + event.question.id);

        // This handles the case where the student scrolls away to a different step before the explanation is returned
        if (step.id !== this.step.id) {
            this.selectStep(step, false);
            this.updateProgressBar();
        }

        let task = event.task;
        let lessonState = task.lessonState;
            
        this.lesson.done = task.done;
        this.lesson.passed = task.passed;
        this.lesson.taskPoints = task.taskPoints;
        this.lesson.pointsAwarded = task.pointsAwarded;

        if (this.lesson.done) {
            TaskEvent.post('task', 'onComplete', this.taskId);   
            let eventType = this.lesson.pointsAwarded > 0 ? 'onPassed' : 'onFailed';
            TaskEvent.post('task', eventType, this.taskId);                
        }

        for(let i = 0; i < this.lesson.steps.length; i++) {
            let step = this.lesson.steps[i];
            let stepState = lessonState.steps[i];

            step.number = stepState.number;
            step.visited = stepState.visited;
            step.visible = stepState.visible;
            step.current = stepState.current;
            step.unlocked = stepState.unlocked;
        }
                
        this.updateProgressBar();   
        this.updateContinueButtons(); 
    }

    onMouseDownContinueButton(event) {
        if (this.step) {
            TaskEvent.post(this.step.type, 'onContinue', this.typeId);
        }

        setTimeout((evt) => {
            this.moveNext();
        }, 10);
    }    

    //////////////////////////////////////////////////////////////////////////////////////////////////////
    // Final Screen

    showFinalScreen() {
        TaskEvent.post('endScreen', 'onView');   


        let completionMessageDiv = $('finalScreen-completionMessage');
        let pointsMessageDiv = $('finalScreen-pointsMessage');

        let buttonBar = $('finalScreen-buttonBar');
        buttonBar.style.display = 'block';

        this.doneButton = $('finalScreen-doneButton');

        this.doneButton = $('finalScreen-doneButton');
        this.doneButton.onmousedown = async (evt) => {
            await TaskEvent.postSync('task', 'onExit', this.taskId);
            window.location.href = '/learn';               
        };          

        if (this.lesson.pointsAwarded < 0) {
            
            completionMessageDiv.innerHTML = `This lesson has been halted due to poor performance and has been assigned a penalty.`;  
            completionMessageDiv.style.color = 'red';    

            pointsMessageDiv.innerHTML = `You've been assigned a penalty of <b>${this.lesson.pointsAwarded}</b> XP for this task.
                <p>A penalty can be the result of extremely poor performance on a single task or it can be due to a pattern of poor performance across a series of tasks. 
                The worse or more consistent the underperformance, the greater the penalty.`;
                
        } else if (this.lesson.pointsAwarded === 0) {

            completionMessageDiv.innerHTML = `This lesson has been halted due to poor performance.`;  
            pointsMessageDiv.innerHTML = `No XP were awarded.`;

        } else if (!this.lesson.passed && this.lesson.pointsAwarded < this.lesson.taskPoints) {

            completionMessageDiv.innerHTML = `You didn't pass the lesson, however, you were awarded a limited amount of XP for the progress you made.`;   
            completionMessageDiv.style.color = 'green';           
            pointsMessageDiv.innerHTML = `You've been awarded <b>${this.lesson.pointsAwarded}</b> of the task's ${this.lesson.taskPoints} XP.`;

        } else if (this.lesson.pointsAwarded < this.lesson.taskPoints) {

            completionMessageDiv.innerHTML = `Congratulations! You've completed the lesson.`;      
            completionMessageDiv.style.color = 'green';         
            pointsMessageDiv.innerHTML = `You've been awarded <b>${this.lesson.pointsAwarded}</b> of the task's ${this.lesson.taskPoints} XP.`;

        } else if (this.lesson.pointsAwarded === this.lesson.taskPoints) {

            completionMessageDiv.innerHTML = `Congratulations! You've completed the lesson.`;   
            completionMessageDiv.style.color = 'green';         
            pointsMessageDiv.innerHTML = `You've been awarded all of the task's <b>${this.lesson.taskPoints}</b> XP.`;

        } else if (this.lesson.pointsAwarded > this.lesson.taskPoints) {

            let bonusPoints = this.lesson.pointsAwarded - this.lesson.taskPoints;

            completionMessageDiv.innerHTML = `Congratulations! You've completed the lesson.`; 
            completionMessageDiv.style.color = 'green';                        
            pointsMessageDiv.innerHTML = `You've been awarded all of the task's <b>${this.lesson.taskPoints}</b> XP, plus a bonus of <b>${bonusPoints}</b> XP for answering every question correctly.`;
        }

        $('header').style.display = 'none';
        $('stepsFrame').style.display = 'none';
        $('finalScreen').style.display = 'block';

        window.scrollTo(0, 0);
    }
}